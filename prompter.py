import os
import logging
from PIL import Image as pil_Image
from graphics import GraphWin, Image, Point


def prompter(images_directory):
    try:
        if os.path.exists(images_directory):
            os.chdir(images_directory)
            if not os.path.exists('prompts'):
                os.mkdir('prompts')
            images = os.listdir()
            for image_n in images:
                if image_n != "masks" and image_n != '.DS_Store' and image_n != 'error.log' and image_n != 'prompts':
                    image = pil_Image.open(image_n)
                    width, height = image.size
                    win = GraphWin(image_n, width, height)
                    img = Image(Point(width/2, height/2), image_n)
                    img.draw(win)
                    win.getMouse()
                    win.close()
        else:
            logging.basicConfig(filename='error.log', level=logging.ERROR)
            raise Exception(f"directory '{images_directory}' does not exist")

    except Exception as e:
        logging.basicConfig(filename='error.log', level=logging.ERROR)
        logging.error(f"An error occurred: {str(e)}")


prompter('images')