import unittest
from PIL import Image
import os
import sys

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from src.digit_matcher import DigitMatcher


class TestDigitMatcher(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        print("Setting up test")
        self.matcher = DigitMatcher()

        # Create test directory if it doesn't exist
        self.test_dir = "tests/test_images"
        os.makedirs(self.test_dir, exist_ok=True)

        # Create test image for digit 1
        self.test_image_1 = Image.new('L', (28, 28), color=255)
        # Draw vertical line
        for y in range(5, 23):
            self.test_image_1.putpixel((14, y), 0)

        # Save test image
        self.test_image_1_path = os.path.join(self.test_dir, "test_1.png")
        self.test_image_1.save(self.test_image_1_path)

    def tearDown(self):
        """Clean up test files after tests."""
        if os.path.exists(self.test_image_1_path):
            os.remove(self.test_image_1_path)
        if os.path.exists(self.test_dir):
            os.rmdir(self.test_dir)

    def test_load_template(self):
        """Test if template loading works correctly."""
        # Test valid template loading
        self.matcher.load_template(1, self.test_image_1_path)
        self.assertIn(1, self.matcher.templates)

        # Test invalid digit error
        with self.assertRaises(ValueError):
            self.matcher.load_template(10, self.test_image_1_path)

    def test_match_digit(self):
        """Test if digit matching works correctly."""
        # First load template
        self.matcher.load_template(1, self.test_image_1_path)

        # Test matching with same image
        matched_digit, distance = self.matcher.match_digit(self.test_image_1)
        self.assertEqual(matched_digit, 1)
        self.assertAlmostEqual(distance, 0.0, places=5)

    def test_error_handling(self):
        """Test if errors are handled correctly."""
        # Test matching without templates
        with self.assertRaises(ValueError):
            self.matcher.match_digit(self.test_image_1)

        # Test with None image
        with self.assertRaises(ValueError):
            self.matcher.match_digit(None)


if __name__ == '__main__':
    unittest.main()