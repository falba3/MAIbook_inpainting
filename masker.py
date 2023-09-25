import os

def masker(images_directory):
    images = os.listdir(images_directory)
    for image in images:
        print(image)

    if not os.path.exists('masks'):
        os.mkdir('masks')
    else:
        print(os.listdir('masks'))