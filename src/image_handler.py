from plistlib import InvalidFileException

import PIL
from PIL import Image  # Library for handling images
import numpy as np  # Library for working with images as numpy arrays

class ImageHandler:
    """
    A class for handling images loading and preprocessing for digit recognition.
    """
    STANDARD_SIZE = (28, 28)

    def load_image(self, path) -> Image.Image:
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

    def image_to_matrix(self, image: Image.Image) -> np.ndarray:
        """
        Converts a greyscale image into a numpy array.

        Args:
            image (PIL.Image.Image): The image to convert.

        Returns:
            np.ndarray: The 2D numpy array representing the image.

        Raises:
            ValueError: If the image is not a PIL image.
        """

        # Verify input is PIL image
        if not isinstance(image, Image.Image):
            raise ValueError('Input must be a PIL image')

        # Resize image
        resized_img = self.resize_image(image)

        # Convert image to numpy array (0-255)
        image_array = np.array(resized_img)

        # Normalize array (0-1)
        normalized_array = image_array / 255.0

        return normalized_array

    def calculate_distance(self, n_arr1: np.ndarray, n_arr2: np.ndarray) -> float:
        """
        Calculates Mean Square Error between two normalized image arrays.
            * Mean Square Error (MSE: 平均二乗誤差): 各値の誤差の二乗を平均したもの

        Args:
            n_arr1 (np.ndarray): First normalized image array (28x28)
            n_arr2 (np.ndarray): Second normalized image array (28x28)
            • This will compare two normalized matrices
            • Return a number representing how different they are
            • Lower number means more similar images

        Returns:
            float: Mean Square Error (smaller means more similar)

        Raises:
            ValueError: If arrays are not same shape or not 28x28
        """

        # Check if arrays are correct shape
        if n_arr1.shape != (28, 28) or n_arr2.shape != (28, 28):
            raise ValueError('Both arrays must be 28x28')

        # Calculate MSE using numpy
        return float(np.mean(np.square(n_arr1 - n_arr2)))

        """
        :::Without numpy:::
        # Assuming n_arr1/n_arr2 are 28x28 lists
        total_elements = len(n_arr1) * len(n_arr1[0]
        suquared_diff_sum = 0.0
        
        for i in range(len(n_arr1)):  # Iterate over rows
            for j in range(len(n_arr1[i])):  # Iterate over columns
                squared_diff_sum += pow((n_arr1[i][j] - n_arr2[i][j]), 2)
        
        return squared_diff_sum / total_elements
        """
