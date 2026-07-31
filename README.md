# Color Recognition Using OpenCV

## Project Overview

This project is a real-time color recognition system developed using Python and OpenCV.

The program captures video through a webcam, detects colored regions, draws bounding boxes around them, and displays the name of each recognized color.

The system can be used with different colored objects and is not limited to a specific object or shape.

## Recognized Colors

- Red
- Orange
- Yellow
- Green
- Blue
- White

## Tools and Libraries

- Python
- OpenCV
- NumPy
- Visual Studio Code

## Installation

Install the required libraries using:

```bash
pip install opencv-python numpy
```

## How to Run

1. Download or clone the repository.
2. Open the project folder in Visual Studio Code.
3. Open the terminal.
4. Run the following command:

```bash
python color_recognition.py
```

5. Place a colored object in front of the webcam.
6. Press `S` to save a screenshot.
7. Press `Q` to close the program.

## How It Works

1. The webcam captures video frames in real time.
2. Each frame is blurred slightly to reduce camera noise.
3. The frame is converted from BGR to HSV color space.
4. HSV ranges are used to recognize the supported colors.
5. Morphological operations remove small unwanted regions.
6. Contours are used to locate colored areas.
7. A labeled bounding box is drawn around each detected region.

## Output

### First Test

![First Output](output_screenshot_20260731_181329_994602.png)

### Second Test

![Second Output](output_screenshot_20260731_181450_654715.png)

## Project Files

- [Python Code](color_recognition.py)
- [First Output Screenshot](output_screenshot_20260731_181329_994602.png)
- [Second Output Screenshot](output_screenshot_20260731_181450_654715.png)
