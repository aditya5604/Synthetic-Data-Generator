import base64
from PIL import Image
from io import BytesIO

def prepare_image(base64_image_string):
    # Assuming `base64_image_string` is the base64 string you received from the frontend

    # Decode the base64 string
    image_bytes = base64.b64decode(base64_image_string)

    # Create a BytesIO object and read the image bytes
    image_data = BytesIO(image_bytes)

    # Open the image with PIL and resize it
    init_image = Image.open(image_data).convert("RGB").resize((768, 512))
    print("Image loaded successfully")
    return init_image