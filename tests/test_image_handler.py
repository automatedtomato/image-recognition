import unittest
from PIL import Image
import os
import sys

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from src.image_handler import ImageHandler


class TestImageHandler(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        print("Setting up test")  # Debug print
        self.handler = ImageHandler()
        self.test_image = Image.new('L', (50, 50), color=255)
        print("Setup complete")  # Debug print to confirm setup finished

    def test_load_image(self):
        """Test if image loading works correctly."""
        import os

        # Create test directory if it doesn't exist
        test_dir = 'tests/test_images'
        os.makedirs(test_dir, exist_ok=True)

        # Define paths before try block
        test_path = os.path.join(test_dir, 'test_image.png')
        color_path = os.path.join(test_dir, 'test_color_image.png')

        # Test loading non-existent file
        with self.assertRaises(FileNotFoundError):
            self.handler.load_image('non_existent_image.png')

        try:
            # Save and test grayscale image
            self.test_image.save(test_path)
            loaded_image = self.handler.load_image(test_path)
            self.assertIsInstance(loaded_image, Image.Image)
            self.assertEqual(loaded_image.mode, 'L')  # Check if grayscale

            # Test loading and converting color image
            color_image = Image.new('RGB', (50, 50), color='red')
            color_image.save(color_path)
            loaded_color = self.handler.load_image(color_path)
            self.assertEqual(loaded_color.mode, 'L')  # Should convert to grayscale

        finally:
            # Clean up test files
            if os.path.exists(test_path):
                os.remove(test_path)
            if os.path.exists(color_path):
                os.remove(color_path)

    def test_verify_image_size(self):
        """Test if size verification works correctly."""
        # Test with wrong size (50x50)
        self.assertFalse(self.handler.verify_image_size(self.test_image))

        # Test with correct size (28x28)
        correct_size_image = Image.new('L', (28, 28), color=255)
        self.assertTrue(self.handler.verify_image_size(correct_size_image))

    def test_resize_image(self):
        """Test if resizing works correctly for various image dimensions."""
        print("Running test_resize_image")
        # Test square image (current test)
        resized_square = self.handler.resize_image(self.test_image)
        self.assertEqual(resized_square.size, (28, 28))

        # Test wide image (landscape)
        wide_image = Image.new('L', (100, 50), color=255)
        resized_wide = self.handler.resize_image(wide_image)
        self.assertEqual(resized_wide.size, (28, 28))

        # Test tall image (portrait)
        tall_image = Image.new('L', (50, 100), color=255)
        resized_tall = self.handler.resize_image(tall_image)
        self.assertEqual(resized_tall.size, (28, 28))

        # Test image that's already 28x28
        correct_size = Image.new('L', (28, 28), color=255)
        resized_correct = self.handler.resize_image(correct_size)
        self.assertEqual(resized_correct.size, (28, 28))
        print("Test_resize_image complete")

if __name__ == '__main__':
    unittest.main()