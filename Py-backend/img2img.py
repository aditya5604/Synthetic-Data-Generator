from PIL import Image
from diffusers import StableDiffusionImg2ImgPipeline
import torch
import os
import base64
from img_prep import prepare_image

model_id_or_path = "runwayml/stable-diffusion-v1-5"
def generate_image(prompt : str, negative_prompt : str,  base64_image_string : str, strength : float, guidance_scale : float , output_img_name : str):
    pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id_or_path, torch_dtype=torch.float16)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    pipe = pipe.to(device)

    init_image = prepare_image(base64_image_string)
    
    base64_images = []
    for i in range(4):
        if not negative_prompt:
            images = pipe(prompt=prompt, image=init_image, strength=strength, guidance_scale=guidance_scale).images
        else:
            images = pipe(prompt=prompt, negative_prompt=negative_prompt,
                           image=init_image, strength=strength, guidance_scale=guidance_scale).images

        image_path = f"{output_img_name}_{i}.jpg"
        print(f"Saving image to {image_path}")
        images[0].save(image_path)

        # Convert the image to a base64 string
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            base64_images.append(base64_image)

        # Remove the image file after converting it to base64
        #os.remove(image_path)

    return base64_images

if __name__ == "__main__":
    prompt = "a beautiful landscape painting"
    negative_prompt = "a dark and gloomy landscape painting"

    #convert an image to base64
    with open("/home/aashish/Downloads/fine-tuning/imageGenerator/sample.jpeg", "rb") as image_file:
        base64_image_string = base64.b64encode(image_file.read()).decode('utf-8')
    
    generate_image(prompt, negative_prompt, base64_image_string, 0.5, 0.5, "output_image")