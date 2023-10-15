import os
import sys
import torch
import logging
import numpy as np
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from torchvision.transforms.functional import to_tensor
from PIL import Image, ImageFilter, ImageDraw
# import matplotlib.pyplot as plt


def masker(images_directory):
    try:
        model = fasterrcnn_resnet50_fpn(weights=True)
        model.eval()

        if os.path.exists(images_directory):
            os.chdir(images_directory)
            if not os.path.exists('masks'):
                os.mkdir('masks')

            images = os.listdir()
            for image_n in images:
                if image_n[-4:] == '.png':
                    image = Image.open(image_n)
                    image_tensor = to_tensor(image).unsqueeze(0)

                    with torch.no_grad():
                        predictions = model(image_tensor)

                    boxes = predictions[0]["boxes"]
                    labels = predictions[0]["labels"]
                    scores = predictions[0]["scores"]

                    confidence_threshold = 0.5

                    child_label = 1
                    child_indices = torch.where((labels == child_label) & (scores > confidence_threshold))
                    child_boxes = boxes[child_indices]
                    child_labels = labels[child_indices]
                    child_scores = scores[child_indices]

                    if len(child_scores) > 0:
                        max_score_index = np.argmax(child_scores)
                        max_score_box = child_boxes[max_score_index]

                        x, y, x2, y2 = map(int, max_score_box)

                        mask = Image.new('L', image.size, 0)
                        draw = ImageDraw.Draw(mask)
                        draw.rectangle((x, y, x2, y2), fill=255)
                        blurred_mask = mask.filter(ImageFilter.GaussianBlur(radius=10))
                        blurred_mask.save(f'masks/{image_n[:-4]}_mask.png')
                        print(f"{images_directory}/{image_n}: succesfully masked! ")
                        # print(f"{image_n}: {max_score_box}")
                        #
                        # # plt.imshow(image)
                        # # ax = plt.gca()
                        # # ax.add_patch(plt.Rectangle((x, y), x2 - x, y2 - y, fill=False, color='green', linewidth=2))
                        # # ax.text(x, y - 5, f"Child: {child_scores[max_score_index]:.2f}", color='green', fontsize=10,
                        # #         backgroundcolor="white")
                        # # plt.axis('off')
                        # # plt.show()
                    else:
                        os.chdir(images_directory)
                        logging.basicConfig(filename='error.log', level=logging.ERROR)
                        print(f"No child found in {images_directory}/{image_n}")
                        raise Exception("No child found in the image")

                    # print(len(child_boxes), len(child_labels), len(child_scores))

    except Exception as e:
        os.chdir(images_directory)
        logging.basicConfig(filename='error.log', level=logging.ERROR)
        logging.error(f"An error occurred: {str(e)}")


# masker('/Users/franco/Desktop/backgrounds')

if __name__ == "__main__":
    inp = "".join(sys.argv[1:])
    masker(inp)