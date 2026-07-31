import cv2
import numpy as np
from datetime import datetime


def main():
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Error: Could not open the camera.")
        return

    # HSV ranges for Rubik's Cube colors
    color_ranges = {
        "Red": [
            (np.array([0, 120, 70]), np.array([10, 255, 255])),
            (np.array([170, 120, 70]), np.array([179, 255, 255])),
        ],
        "Orange": [
            (np.array([11, 120, 80]), np.array([22, 255, 255])),
        ],
        "Yellow": [
            (np.array([23, 100, 100]), np.array([35, 255, 255])),
        ],
        "Green": [
            (np.array([36, 70, 70]), np.array([85, 255, 255])),
        ],
        "Blue": [
            (np.array([90, 70, 70]), np.array([130, 255, 255])),
        ],
        "White": [
            (np.array([0, 0, 180]), np.array([179, 55, 255])),
        ],
    }

    # Rectangle and text colors in BGR format
    box_colors = {
        "Red": (0, 0, 255),
        "Orange": (0, 165, 255),
        "Yellow": (0, 255, 255),
        "Green": (0, 255, 0),
        "Blue": (255, 0, 0),
        "White": (255, 255, 255),
    }

    kernel = np.ones((5, 5), np.uint8)

    while True:
        success, frame = camera.read()

        if not success:
            print("Error: Could not read camera frame.")
            break

        # Reduce camera noise
        blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)

        # Convert the camera frame from BGR to HSV
        hsv_frame = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)

        for color_name, ranges in color_ranges.items():
            combined_mask = np.zeros(
                hsv_frame.shape[:2],
                dtype=np.uint8,
            )

            # Red requires two HSV ranges
            for lower_range, upper_range in ranges:
                mask = cv2.inRange(
                    hsv_frame,
                    lower_range,
                    upper_range,
                )

                combined_mask = cv2.bitwise_or(
                    combined_mask,
                    mask,
                )

            # Remove small unwanted areas
            combined_mask = cv2.morphologyEx(
                combined_mask,
                cv2.MORPH_OPEN,
                kernel,
            )

            combined_mask = cv2.morphologyEx(
                combined_mask,
                cv2.MORPH_CLOSE,
                kernel,
            )

            contours, _ = cv2.findContours(
                combined_mask,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE,
            )

            for contour in contours:
                area = cv2.contourArea(contour)

                # Ignore very small detected areas
                if area < 300:
                    continue

                x, y, width, height = cv2.boundingRect(contour)
                aspect_ratio = width / float(height)

                # Focus on square-like Rubik's Cube stickers
                if not 0.5 <= aspect_ratio <= 1.8:
                    continue

                box_color = box_colors[color_name]

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + width, y + height),
                    box_color,
                    2,
                )

                cv2.putText(
                    frame,
                    color_name,
                    (x, max(y - 10, 25)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    box_color,
                    2,
                )

        cv2.putText(
            frame,
            "Q: Exit | S: Save Screenshot",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2,
        )

        cv2.imshow("Real-Time Color Recognition", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("s"):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = f"output_screenshot_{timestamp}.png"

            cv2.imwrite(filename, frame)
            print(f"Screenshot saved as {filename}")

        elif key == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
