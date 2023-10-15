import sys
import os
import logging
from PIL import Image
from diffusers import StableDiffusionXLInpaintPipeline
import torch


pipe = StableDiffusionXLInpaintPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-refiner-1.0", torch_dtype=torch.float16, variant="fp16", use_safetensors=True).to("cuda")


def refiner(images_directory):
    try:
        global pipe
        if os.path.exists(images_directory):
            if os.path.exists(images_directory + '/masks') and os.path.exists(images_directory + '/prompts'):
                if not os.path.exists(images_directory + '/refined'):
                    os.mkdir(images_directory + '/outputs/refined')
                images = os.listdir(images_directory)
                for image_n in images:
                    if image_n[-4:] == '.png':
                        name = image_n[:-4]
                        if os.path.exists(f"{images_directory}/outputs/{name}_output.png") and os.path.exists(f"{images_directory}/masks/{name}_mask.png")\
                                and os.path.exists(f"{images_directory}/prompts/{name}.txt"):
                            print(f"image:  {images_directory}/outputs/{name}_output.png\nmask:    {images_directory}/masks/{name}_mask.png\nprompt:    {images_directory}/prompts/{name}.txt")

                            with open(f"{images_directory}/prompts/{name}.txt", 'r') as file:
                                prompt = file.readline()
                            background = Image.open(f"{images_directory}/outputs/{name}_output.png")
                            negative_prompt = "Out of frame, cropped, deformed, disfigured, extra character, headless, unclear, Nikon, Sony, Canon, DSLR, photorealism, photorealistic, lens, aperture, 85mm, 100mm, 200mm, kiss, scary, violence, alcohol, drugs, text, font, letters, blood, injury, watermark, logo"
                            mask = Image.open(f"{images_directory}/masks/{name}_mask.png")

                            image_output = pipe(prompt=prompt,
                                                 image=background,
                                                 mask_image=mask,
                                                 # width=background.size[0],
                                                 # height=background.size[1],
                                                negative_prompt=negative_prompt,
                                                strength=0.99999,
                                                # strength=1,
                                                num_inference_steps=20,
                                                guidance_scale=10
                                                ).images[0]
                            image_output.save(f"{images_directory}/outputs/refined/{name}_refined.png")

                        else:
                            os.chdir(images_directory)
                            logging.basicConfig(filename='error.log', level=logging.ERROR)
                            raise Exception(f"missing mask or prompt for {name}.png")

            else:
                os.chdir(images_directory)
                logging.basicConfig(filename='error.log', level=logging.ERROR)
                raise Exception(f"'masks' folder does not exist")
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
    refiner(inp)