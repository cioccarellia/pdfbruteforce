import os
import time
from concurrent.futures import ThreadPoolExecutor
from random import shuffle
import logging

import PyPDF2
from PyPDF2.errors import FileNotDecryptedError


def current_milli_time():
    return round(time.time() * 1000)


param_verbose_output = False
param_remove_file_after_decryption = False


const_mode_rb = 'rb'
const_mode_wb = 'wb'
const_pdf_ext = '.pdf'

def decrypt_pdf(input_path, output_path, generator):
    # Open pdf file
    with open(input_path, const_mode_rb) as (file, error):
        if error:
            logging.error(f"[{input_path}]: File not found or not readable")
        else:
            # File exists and we can read it
            initial_time_ms = current_milli_time()

            # Open file with PyPDF
            pdf_reader = PyPDF2.PdfReader(file)

            # Make sure it is encrypted
            if pdf_reader.is_encrypted:
                # Explore guess space
                for guess in generator:

                    if param_verbose_output:
                        print(guess, end='\r')

                    try:
                        # Attempt to decrypt PDF with the current guess
                        pdf_reader.decrypt(str(guess))
                        pdf_writer = PyPDF2.PdfWriter()

                        # Save all pages
                        for page_num in range(len(pdf_reader.pages)):
                            pdf_writer.add_page(pdf_reader.pages[page_num])

                        new_filename = output_path + "." + str(guess) + const_pdf_ext

                        # Create new decrypted file
                        with open(new_filename, const_mode_wb) as decrypted_file:
                            pdf_writer.write(decrypted_file)

                        # with open('decrypted.txt', 'a') as decrypted_list:
                        #    decrypted_list.write(f"{output_path} -> {guess}\n")

                        # Remove the original encrypted file
                        if param_remove_file_after_decryption:
                            os.remove(input_path)

                        # Calculate elapsed time
                        elapsed_ms = current_milli_time() - initial_time_ms

                        logging.info(f"[{input_path}]: Decryption successful, password={guess}. Decrypted file saved as {new_filename}. Took {elapsed_ms / 1000}s")
                        return
                    except FileNotDecryptedError as unsuccessful_decryption:
                        if param_verbose_output:
                            logging.warning(f"--> Decryption attempt unsuccessful: guess={guess}")
                        continue
                    except Exception as generic_exception:
                        logging.error(f"--> Unknown error: {generic_exception}")
                        return

                logging.error(f"[{input_path}]: Decryption unsuccessful, password was not in the guess space")
                return
            else:
                logging.error(f"[{input_path}]: File not encrypted.")
                return


param_multidecrypt_randomize_dirlist = False
param_multidecrypt_multithreaded = False


# Function to decrypt each PDF file in the directory
def decrypt_files_in_directory(directory, generator):
    # Get all files in directory
    dir_files_all = os.listdir(directory)

    # Filter for just PDF files
    dir_files_pdfs = filter(lambda f: f.endswith(const_pdf_ext), dir_files_all)

    # Randomize file list
    if param_multidecrypt_randomize_dirlist:
        shuffle(dir_files_pdfs)

    if param_multidecrypt_multithreaded:
        # Create a ThreadPoolExecutor with as many threads as there are pdf files for parallel decryption
        with ThreadPoolExecutor(max_workers=len(dir_files_pdfs)) as executor:
            # Use the executor to submit tasks for each file
            futures = {
                executor.submit(
                    decrypt_pdf,
                    os.path.join(directory, filename_pdf),
                    os.path.join(directory, f"pypbf_decrypted_{filename_pdf}"),
                    generator
                ) for filename_pdf in dir_files_pdfs # if filename_pdf.endswith(pdf_ext)
            }

            # Wait for all tasks to complete
            for future in futures:
                try:
                    future.result()
                except Exception as future_error:
                    logging.error(f"Multithreading error: {future_error}")
    else:
        # Run serial decryption for every file
        for filename_pdf in dir_files_pdfs:
            if filename_pdf.endswith(const_pdf_ext):  # Checks if the file is a PDF
                logging.info(f"Decrypting {filename_pdf}...")

                # Define paths
                encrypted_pdf_file_path = os.path.join(directory, filename_pdf)
                decrypted_pdf_file_path = os.path.join(directory, f"pypbf_decrypted_{filename_pdf}")

                # Run Decryption
                decrypt_pdf(encrypted_pdf_file_path, decrypted_pdf_file_path, generator)
