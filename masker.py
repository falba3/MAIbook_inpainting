import os
import logging
from PIL import Image as pil_Image, ImageDraw, ImageFilter
from graphics import GraphWin, Image, Point, Rectangle


def masker(images_directory):
    try:
        if os.path.exists(images_directory):
            os.chdir(images_directory)
            if not os.path.exists('masks'):
                os.mkdir('masks')
            images = os.listdir()
            for image_n in images:
                if image_n != "masks" and image_n != '.DS_Store' and image_n != 'error.log' and image_n != "prompts":
                    image = pil_Image.open(image_n)
                    width, height = image.size
                    win = GraphWin(image_n, width, height)
                    img = Image(Point(width/2, height/2), image_n)
                    img.draw(win)
                    top_left = win.getMouse()
                    bottom_right = win.getMouse()
                    box = Rectangle(top_left, bottom_right)
                    box.draw(win)
                    win.getMouse()
                    win.close()
                    top_left = top_left.getX(), top_left.getY()
                    bottom_right = bottom_right.getX(), bottom_right.getY()
                    mask = pil_Image.new('L', image.size, 0)
                    draw = ImageDraw.Draw(mask)
                    draw.rectangle((top_left[0], top_left[1], bottom_right[0], bottom_right[1]), fill=255)
                    blurred_mask = mask.filter(ImageFilter.GaussianBlur(radius=10))
                    blurred_mask.save(f'masks/{image_n[:-4]}_mask.png')
        else:
            os.chdir('..')
            logging.basicConfig(filename='error.log', level=logging.ERROR)
            raise Exception(f"directory '{images_directory}' does not exist")

    except Exception as e:
        os.chdir('..')
        logging.basicConfig(filename='error.log', level=logging.ERROR)
        logging.error(f"An error occurred: {str(e)}")


masker('images2')