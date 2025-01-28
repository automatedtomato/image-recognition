from src.image_handler import ImageHandler
from src.digit_matcher import DigitMatcher
import numpy as np
import os

def main():
    # Create instance
    handler = ImageHandler()
    digit_matcher = DigitMatcher()

    # Get correct path relative to this file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(current_dir)

    # Create paths using os.path.join
    template_dir = os.path.join(project_dir, 'data', 'templates')
    test_image_path = os.path.join(project_dir, 'data/test_images', 'digit_5.png')  # Enter the name of file you want to check HERE

    # Load all templates from directory
    digit_matcher.load_all_templates(template_dir)
    test_image = handler.load_image(test_image_path)

    # Match digit and print result
    predicted_digit, distance = digit_matcher.match_digit(test_image)
    print(f'Predicted digit is {predicted_digit} (distance: {distance:.4f})')

if __name__ == '__main__':
    main()