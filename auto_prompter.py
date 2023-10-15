import os
import sys
import logging
from PIL import Image as pil_Image
import pandas as pd
from graphics import GraphWin, Image, Point


def prompter(images_directory):
    try:
        if os.path.exists(images_directory):
            os.chdir(images_directory)

            if not os.path.exists('prompts.csv'):
                logging.basicConfig(filename='error.log', level=logging.ERROR)
                raise Exception(f"prompts.csv file does not exist")

            if not os.path.exists('prompts'):
                os.mkdir('prompts')

            df = pd.read_csv('prompts.csv')
            for index, row in df.iterrows():
                prompt = row['prompt']
                photo = str(row['photo'])
                with open(f"prompts/{photo}.txt", 'w') as file:
                    file.write(prompt)
        else:
            os.chdir(images_directory)
            logging.basicConfig(filename='error.log', level=logging.ERROR)
            raise Exception(f"directory '{images_directory}' does not exist")

    except Exception as e:
        os.chdir(images_directory)
        logging.basicConfig(filename='error.log', level=logging.ERROR)
        logging.error(f"An error occurred: {str(e)}")


# prompter('backgrounds')


if __name__ == "__main__":
    inp = "".join(sys.argv[1:])
    prompter(inp)