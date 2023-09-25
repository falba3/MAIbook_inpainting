import os
from PIL import Image as pil_Image
from graphics import GraphWin, Image, Point, Rectangle


def masker(images_directory):
    if not os.path.exists('masks'):
        os.mkdir('masks')

    os.chdir(images_directory)
    images = os.listdir()
    for image_n in images:
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



masker('images')