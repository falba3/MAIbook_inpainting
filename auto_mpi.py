from auto_masker import masker
from auto_prompter import prompter
from auto_inpainter import inpainter


import os
import sys
import logging


def main(images_directory):
    try:
        if os.path.exists(images_directory):
            os.chdir(images_directory)

            masker(images_directory)
            prompter(images_directory)
            inpainter(images_directory)

        else:
            os.chdir(images_directory)
            logging.basicConfig(filename='error.log', level=logging.ERROR)
            raise Exception(f"directory '{images_directory}' does not exist")

    except Exception as e:
        os.chdir(images_directory)
        logging.basicConfig(filename='error.log', level=logging.ERROR)
        logging.error(f"An error occurred: {str(e)}")




if __name__ == "__main__":
    inp = "".join(sys.argv[1:])
    main(inp)