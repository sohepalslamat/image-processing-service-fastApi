import io
from fastapi import UploadFile
from PIL import Image

from image_processing.factories import ImageProcessorFactory


async def process_image(file: UploadFile, transformations: list) -> io.BytesIO:
    # Open the image
    image = Image.open(file.file)
    
    # Apply transformations using the strategy pattern
    for transformation in transformations:
        processor = ImageProcessorFactory.get_processor(transformation['type'], **transformation['params'])
        image = processor.process(image)

    # Save the processed image to a BytesIO object to upload to Firebase
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')  # Save as PNG or JPEG as needed
    img_byte_arr.seek(0)

    return img_byte_arr