import logging
import string

from core_api import decrypt_all_in_directory, decrypt_pdf
from generators.alphanumeric import gen_dictionary
from generators.numeric import gen_numeric


def decrypt_polimi_code():
    decrypt_all_in_directory(
        "DS",
        generator=gen_numeric(200_000, 300_000),
        param_multidecrypt_randomize_dirlist=True,
        param_multidecrypt_multithreaded=True,
        param_verbose_output=False,
        param_show_progress_bar=False,
        param_remove_file_after_decryption=True
    )


def decrypt_parolo():
    decrypt_pdf(
        "sample/parolo/aiutino.pdf",
        "verifica.pdf",
        gen_dictionary(['password', 'non', 'corretta'], 3)
    )


def main():
    single = True

    if single:
        decrypt_pdf(
            "sample/parolo/aiutino.pdf",
            "verifica.pdf",
            gen_dictionary(['password', 'non', 'corretta'], 3)
        )

    else:
        decrypt_all_in_directory(
            "sample",
            generator=gen_numeric(0, 100_000)
        )



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    try:
        main()
    except KeyboardInterrupt:
        logging.error("Quitting")