import argparse
import glob
import os
import random
import sys

import cv2

from background import remove_background
from extract import extract_objects_connected


MIN_TRANSPARENCY_PERCENT = 5.0


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


def pick_and_show_random(directory):
    random_file = pick_random(directory)
    display_image(f"Random Pick from {os.path.basename(directory)}", random_file)
    return True


def pick_random(directory):
    """Picks a random PNG from the directory and displays it."""
    png_files = glob.glob(os.path.join(directory, "*.png"))
    if not png_files:
        print(
            f"No PNG files found in directory '{directory}' to pick from.",
            file=sys.stderr,
        )
        return False

    random_file = random.choice(png_files)
    print(f"Randomly selected: {os.path.basename(random_file)}")
    return random_file


def process_image(image_path):
    print("processing image", image_path)
    input_basename = os.path.basename(image_path)
    print("input_basename", input_basename)
    input_name_part, _ = os.path.splitext(input_basename)
    print("input_name_part", input_name_part)
    bg_removed_dir = "out_bg"
    bg_removed_filename = f"{input_name_part}.png"  # Force PNG
    bg_removed_path = os.path.join(bg_removed_dir, bg_removed_filename)
    os.makedirs(bg_removed_dir, exist_ok=True)

    # 2. Extracted Objects Directory Path
    # The extract script creates the final dir, so we just define the base here
    extracted_obj_base_dir = "tmp/ext"
    extracted_obj_dir = os.path.join(
        extracted_obj_base_dir, input_name_part
    )  # e.g., ext/coins1

    # The extract script should handle creating this directory if needed
    print("removing background", image_path, bg_removed_path)
    remove_background(image_path, bg_removed_path)
    extract_objects_connected(bg_removed_path, extracted_obj_dir)
    return pick_random(extracted_obj_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process an image: 1. Remove background. 2. Check transparency. 3. Extract objects. Optionally pick and show a random extracted object."
    )
    parser.add_argument("--input_image", help="Path to the input image file.")
    parser.add_argument(
        "--pick",
        action="store_true",
        help="Pick one extracted object at random and display it.",
    )

    args = parser.parse_args()
    process_image(input_name_part)
