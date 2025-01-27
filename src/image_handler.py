from plistlib import InvalidFileException

import PIL
from PIL import Image

class ImageHandler:
    """
    A class for handling images loading and preprocessing for digit recognition.
    """
    STANDARD_SIZE = (28, 28)

    def load_image(self,path) -> Image.Image:
        """
        Loads an image from the given path and returns it in greyscale.

        Args:
            path (str): The path to the image file.

        Returns:
            PIL.Image.Image: The loaded image in greyscale.

        Raises:
            FileNotFoundError: If the file is not found.
            PIL.UnidentifiedImageError: If the file is not a valid image
        """
        try:
            img = Image.open(path)
            img_grey = img.convert('L')
            return img_grey
        except  FileNotFoundError as e:
            raise FileNotFoundError(f'Could not find image file at {path}') from e
        except PIL.UnidentifiedImageError as e:
            raise PIL.UnidentifiedImageError(f'File at {path} is not a valid image') from e

    def verify_image_size(self, image: Image.Image) -> bool:
        """
        Checks if the image is the correct size(28px * 28px) for digit recognition.

        Args:
            image (PIL.Image.Image): The image to check.

        Returns:
            bool: True if the image is the correct size, False otherwise.
        """
        return image.size == self.STANDARD_SIZE

    def resize_image(self, image: Image.Image) -> Image.Image:
        """
        Resizes the image to the standard size(28px * 28px) while preserving the aspect ratio.
        If necessary, pads the image with white pixels to maintain square dimensions.

        Args:
            image (PIL.Image.Image): The image to resize.

        Returns:
            PIL.Image.Image: The resized image.

        Example:
            If input image is 100 * 50
            1. New size will be 28 * 14 (preserving aspect ratio)
            2. Image will be centered on 28 * 28 white background
        """
        # Return original image if already correct size
        if self.verify_image_size(image):
            return image

        # Calculate the aspect ratio
        aspect_ratio = image.size[0] / image.size[1]
        resized_image = Image.new('L', self.STANDARD_SIZE, 255)  # Create a white background on which to paste the resized image

        # Calculate new dimensions preserving aspect ratio
        if aspect_ratio > 1:  # Width is larger than height
            new_width = self.STANDARD_SIZE[0]
            new_height = int(new_width / aspect_ratio)

        else:  # Height is larger than width
            new_height = self.STANDARD_SIZE[1]
            new_width = int(new_height * aspect_ratio)

        # Resize image using high-quality resampling
        resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Create white background
        final_image = Image.new('L', self.STANDARD_SIZE, 255)  # 'L' for greyscale

        # Calculate Position to paste resized image at center
        paste_x = (self.STANDARD_SIZE[0] - new_width) // 2
        paste_y = (self.STANDARD_SIZE[1] - new_height) // 2

        # Paste resized image onto white background
        final_image.paste(resized_image, (paste_x, paste_y))

        return final_image

        return final_image