import logging
import string

from core_api import decrypt_all_in_directory, decrypt_pdf
from generators.alphanumeric import gen_alphanumeric
from generators.numeric import gen_numeric


def main():
    single = True

    if single:
        decrypt_pdf(
            "sample/parolo/aiutino.pdf",
            "verifica.pdf",
            gen_alphanumeric(['password', 'non', 'corretta'], 3)
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