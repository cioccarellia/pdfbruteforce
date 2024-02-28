import logging

from core_api import decrypt_files_in_directory, decrypt_pdf
from generators.alphanumeric import gen_alphanumeric
from generators.numeric import gen_numeric


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    decrypt_pdf(
        "sample/hal-00761669---736472.pdf",
        "sample/pybf_decrypted_hal-00761669---736472.pdf",
        gen_numeric(700000, 740000)
    )


    decrypt_pdf(
        "sample/fb0f00c4---11111.pdf",
        "sample/pybf_decrypted_hal-00761669---736472.pdf",
        gen_numeric(0, 1000000)
    )


    # decrypt_files_in_directory(
    #     "sample",
    #     generator=gen_numeric(0, 100_000)
    # )