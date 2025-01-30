# Handwritten Digit Recognition Project

A Python project to identify handwritten digits (0-9) using template matching approach. This project is designed as a learning tool to understand fundamental concepts in Machine Learning and Image Processing.

## Project Structure
```
digit_recognition/
    ├── data/           (for storing image data)
    ├── src/            (for source code)
    │   ├── __init__.py
    │   ├── image_handler.py  (handles image processing)
    │   └── digit_matcher.py  (matches digits with templates)
    └── tests/          (for test files)
        ├── __init__.py
        └── test_image_handler.py
```

## Features Implemented

### Image Handler
- Image loading and grayscale conversion
- Resizing images to standard size (28x28)
- Image normalization (pixel values 0-1)
- Distance calculation between images

### Digit Matcher
- Template management for digits 0-9
- Digit matching using Mean Square Error
- Error handling and input validation

## Requirements
- Python 3
- PIL (Pillow) for image processing
- NumPy for numerical operations

## Installation
1. Clone the repository
2. Install required packages:
```bash
pip install Pillow numpy
```

## Usage
```python
from src.digit_matcher import DigitMatcher
from PIL import Image

# Create instance
matcher = DigitMatcher()

# Load templates
matcher.load_template(1, "path/to/template_1.png")
# ... load other templates ...

# Match a digit
image = Image.open("path/to/test_digit.png")
digit, confidence = matcher.match_digit(image)
```

## Testing
Tests are implemented using Python's unittest framework:
```bash
python -m unittest tests/test_image_handler.py
```

## Project Goals
1. Learn Python ML/AI engineering fundamentals
2. Understand image processing basics
3. Practice mathematical concepts in ML/AI
4. Implement basic template matching algorithm

## Next Steps
1. Complete test suite implementation
2. Add template digit images
3. Test with real handwritten digits
4. Add performance metrics

## Learning Focus
This project emphasizes:
- Python programming fundamentals
- Image processing concepts
- Basic ML algorithms
- Test-driven development
- Documentation practices

## Note
This project is designed for learning purposes and might not include comprehensive error handling or edge cases.
