from image_handler import ImageHandler
import numpy as np
from PIL import Image
from typing import Dict, Tuple

class DigitMatcher:
    """
    A class for matching handwritten digits against template images.
    Uses template matching approach where each digit (0-9) has a reference image.
    New images are compared against these templates to find the best match.

    Attributes:
        image_handler (ImageHandler): Handles image loading and processing
        templates (Dict[int, np.ndarray]): Stores template matrices for each digit
    """

    def __init__(self):
        """Initialize DigitMatcher with ImageHandler and empty templates dictionary."""
        self.image_handler = ImageHandler()
        self.templates: Dict[int, np.ndarray] = {}

    def load_template(self, digit: int, image_path: str) -> None:
        """
        Load and store a template image for a digit.
        Template images are converted to normalized matrices for comparison.

        Args:
            digit (int): The digit this template represents (0-9)
            image_path (str): Path to the template image file

        Raises:
            ValueError: If digit is not 0-9
            FileNotFoundError: If template image not found
        """
        # Validate digit range
        if not 0 <= digit <= 9:
            raise ValueError("Digit must be between 0 and 9")

        # Load and process image
        image = self.image_handler.load_image(image_path)
        # Convert to normalized matrix
        template_matrix = self.image_handler.image_to_matrix(image)
        # Store in templates dictionary
        self.templates[digit] = template_matrix

    def match_digit(self, image: Image.Image) -> Tuple[int, float]:
        """
        Find the best matching digit for an input image.
        Compares input image against all stored templates using MSE distance.

        Args:
            image (PIL.Image.Image): Input image to match

        Returns:
            Tuple[int, float]: (matched digit, distance score)
                              Lower distance score means better match

        Raises:
            ValueError: If no templates are loaded or image is invalid
        """
        # Validate input
        if image is None:
            raise ValueError("Input image cannot be None")

        # Check if templates are loaded
        if not self.templates:
            raise ValueError("No templates loaded. Please load templates first.")

        # Convert input image to normalized matrix
        input_matrix = self.image_handler.image_to_matrix(image)

        # Initialize best match tracking
        best_match = None
        best_distance = float('inf')  # Start with infinity

        # Compare with each template
        for digit, template in self.templates.items():
            distance = self.image_handler.calculate_distance(input_matrix, template)
            if distance < best_distance:
                best_distance = distance
                best_match = digit

        # Verify we found a match
        if best_match is None:
            raise RuntimeError("Failed to find matching digit")

        return (best_match, best_distance)