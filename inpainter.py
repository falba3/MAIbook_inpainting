import os
import logging

def inpainter(images_directory):
    if os.path.exists(images_directory):
        if os.path.exists(images_directory + '/masks'):
            images = os.listdir(images_directory)
            for image_n in images:
                if image_n != "masks" and image_n != '.DS_Store' and image_n != 'error.log':
                    name = image_n[:-4]
                    if os.path.exists(f"{images_directory}/{name}.png") and os.path.exists(f"{images_directory}/masks/{name}_mask.png"):
                        print(f"image:  {images_directory}/{name}.png\nmask:    {images_directory}/masks/{name}_mask.png")

                        # image_output = pipe(prompt=prompt,
                        #                     image=background,
                        #                     mask_image=mask,
                        #                     width=background.size[0],
                        #                     height=background.size[1],
                        #                     negative_prompt=negative_prompt,
                        #                     strength=strength,
                        #                     num_inference_steps=num_inference_steps,
                        #                     guidance_scale=guidance_scale
                        #                     ).images[0]
                        # image_output.save(f'output/{name}_out.png')
                    else:
                        logging.basicConfig(filename='error.log', level=logging.ERROR)
                        raise Exception(f"missing mask for {name}.png")

        else:
            logging.basicConfig(filename='error.log', level=logging.ERROR)
            raise Exception(f"'masks' folder does not exist")
    else:
        logging.basicConfig(filename='error.log', level=logging.ERROR)
        raise Exception(f"directory '{images_directory}' does not exist")

inpainter('images')