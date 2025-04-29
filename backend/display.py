
import cv2

def display_image(window_name, image_path):
    """Loads and displays an image using OpenCV."""
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print(f"Error: Could not load image for display: {image_path}", file=sys.stderr)
        return
    cv2.imshow(window_name, img)
    print(f"Displaying: {image_path}. Press any key to close.")
    cv2.waitKey(0)
    cv2.destroyWindow(window_name)
