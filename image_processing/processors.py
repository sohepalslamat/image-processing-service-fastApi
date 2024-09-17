from PIL import Image

class ImageProcessor:
    def process(self, image: Image) -> Image:
        raise NotImplementedError("Subclasses should implement this method.")

class ResizeProcessor(ImageProcessor):
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def process(self, image: Image) -> Image:
        return image.resize((self.width, self.height))

class GrayscaleProcessor(ImageProcessor):
    def process(self, image: Image) -> Image:
        return image.convert('L')

class RotateProcessor(ImageProcessor):
    def __init__(self, degrees: int):
        self.degrees = degrees

    def process(self, image: Image) -> Image:
        return image.rotate(self.degrees)