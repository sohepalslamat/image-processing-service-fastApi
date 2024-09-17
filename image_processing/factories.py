from image_processing.processors import GrayscaleProcessor, ImageProcessor, ResizeProcessor, RotateProcessor


class ImageProcessorFactory:
    @staticmethod
    def get_processor(transformation: str, **kwargs) -> ImageProcessor:
        if transformation == "resize":
            return ResizeProcessor(kwargs['width'], kwargs['height'])
        elif transformation == "grayscale":
            return GrayscaleProcessor()
        elif transformation == "rotate":
            return RotateProcessor(kwargs['degrees'])
        else:
            raise ValueError(f"Unknown transformation: {transformation}")