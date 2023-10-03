import sys
import os
import logging
from PIL import Image
from diffusers import DiffusionPipeline
import torch


pipe = DiffusionPipeline.from_pretrained("Lykon/absolute-realism-1.6525-inpainting").to("cuda")
# pipe = DiffusionPipeline.from_pretrained("Lykon/dreamshaper-7-inpainting").to("cuda")

def inpainter(images_directory):
    global pipe
    if os.path.exists(images_directory):
        if os.path.exists(images_directory + '/masks') and os.path.exists(images_directory + '/prompts'):
            images = os.listdir(images_directory)
            for image_n in images:
                if image_n != "masks" and image_n != '.DS_Store' and image_n != 'error.log' and image_n != 'prompts':
                    name = image_n[:-4]
                    if os.path.exists(f"{images_directory}/{name}.png") and os.path.exists(f"{images_directory}/masks/{name}_mask.png")\
                            and os.path.exists(f"{images_directory}/prompts/{name}.txt"):
                        print(f"image:  {images_directory}/{name}.png\nmask:    {images_directory}/masks/{name}_mask.png\nprompt:    {images_directory}/prompts/{name}.txt")

                        with open(f"{images_directory}/prompts/{name}.txt", 'r') as file:
                            prompt = file.readline()
                        background = Image.open(f"{images_directory}/{name}.png")
                        negative_prompt = "Out of frame, cropped, deformed, disfigured, extra character, headless, unclear, Nikon, Sony, Canon, DSLR, photorealism, photorealistic, lens, aperture, 85mm, 100mm, 200mm, kiss, scary, violence, alcohol, drugs, text, font, letters, blood, injury, watermark, logo"
                        mask = Image.open(f"{images_directory}/masks/{name}_mask.png")

                        image_output = pipe(prompt=prompt,
                                             image=background,
                                             mask_image=mask,
                                             width=background.size[0],
                                             height=background.size[1],
                                            negative_prompt=negative_prompt,
                                            # strength=0.99,
                                            strength=1,
                                            num_inference_steps=20,
                                            guidance_scale=10
                                            ).images[0]
                        image_output.save(f"{name}_output.png")

                    else:
                        os.chdir('..')
                        logging.basicConfig(filename='error.log', level=logging.ERROR)
                        raise Exception(f"missing mask for {name}.png")

        else:
            os.chdir('..')
            logging.basicConfig(filename='error.log', level=logging.ERROR)
            raise Exception(f"'masks' folder does not exist")
    else:
        os.chdir('..')
        logging.basicConfig(filename='error.log', level=logging.ERROR)
        raise Exception(f"directory '{images_directory}' does not exist")

if __name__ == "__main__":
    inp = "".join(sys.argv[1:])
    inpainter(inp)