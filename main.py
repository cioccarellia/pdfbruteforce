import os
import time
from random import shuffle

import PyPDF2
from PyPDF2.errors import FileNotDecryptedError

from generators.alphanumeric import gen_alphanumeric
from generators.numeric import gen_numeric

# Define the directory containing the PDF files
directory_path = ""



guess_lower_range = 200_000
guess_upper_range = 300_000

def current_milli_time():
    return round(time.time() * 1000)


def decrypt_pdf(input_path, output_path):
    with open(input_path, 'rb') as file:
        time0 = current_milli_time()

        pdf_reader = PyPDF2.PdfReader(file)

        if pdf_reader.is_encrypted:
            for code in (gen_numeric(guess_lower_range, guess_upper_range)):
                print(code, end='\r')
                try:
                    pdf_reader.decrypt(str(code))
                    pdf_writer = PyPDF2.PdfWriter()

                    for page_num in range(len(pdf_reader.pages)):
                        pdf_writer.add_page(pdf_reader.pages[page_num])

                    new_filename = output_path + "." + str(code) + ".pdf"

                    with open(new_filename, 'wb') as output_file:
                        pdf_writer.write(output_file)

                    with open('decrypted.txt', 'a') as decrypted_list:
                        decrypted_list.write(f"{output_path} -> {code}\n")

                    os.remove(input_path)
                    time1 = current_milli_time()

                    print(f"--> Decryption successful, code={code}. Decrypted file saved as {new_filename}, took {(time1-time0) / 1000}s")
                    return
                except FileNotDecryptedError as unsuccessful_decryption:
                    continue
                except Exception as exc:
                    print(f"--> Unknown error: {exc}")
                    return

            print("--> Decryption unsuccessful")
            return
        else:
            print("--> File not encrypted")
            return



# Function to decrypt each PDF file in the directory
def decrypt_files_in_directory(directory):
    files = os.listdir(directory)
    shuffle(files)

    for filename in files:
        if filename.endswith('.pdf'):  # Check if the file is a PDF
            print(f"Decrypting {filename}")
            file_path = os.path.join(directory, filename)
            output_path = os.path.join(directory, f"decrypted_{filename}")
            decrypt_pdf(file_path, output_path)




