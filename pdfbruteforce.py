import logging
import string

from core_api import decrypt_all_in_directory, decrypt_pdf
from generators.alphanumeric import gen_alphanumeric
from generators.numeric import gen_numeric


def main():
    single = True

    if single:
        decrypt_pdf(
            "hal-00761669---736472.pdf",
            "sample/pybf_decrypted_hal-00761669---736472.pdf",
            gen_alphanumeric(string.digits, 6)
        )

        decrypt_pdf(
            "sample/fb0f00c4---11111.pdf",
            "sample/pybf_decrypted_hal-00761669---736472.pdf",
            gen_numeric(0, 1000000)
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