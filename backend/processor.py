import argparse
import os
import shutil

from memory import MemoryMonitor
from background import remove_background
from extract import draw_bounding_box
from resize import resize_jpg
from display import display_image  ## only for debugging


MIN_TRANSPARENCY_PERCENT = 5.0


def process_image(image_path):

    print("processing image", image_path)
    resize_jpg(image_path, image_path, 750)

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
    extracted_obj_dir = os.path.join(extracted_obj_base_dir, input_name_part)  # e.g., ext/coins1
    target_file = os.path.join(extracted_obj_dir, "output.png")  # e.g., ext/coins1/output.png

    # Clean up: not needed for 1 users, but may be needed in the future
    # if os.path.exists(extracted_obj_dir):
    #     shutil.rmtree(extracted_obj_dir)
    # os.makedirs(os.path.dirname(target_file), exist_ok=True)     # Make sure the parent directories exist

    monitor = MemoryMonitor()
    monitor.start()

    # The extract script should handle creating this directory if needed
    print("removing background", image_path, bg_removed_path)
    remove_background(image_path, bg_removed_path)

    print("drawing boxes", bg_removed_path, image_path, target_file)
    draw_bounding_box(bg_removed_path, image_path, target_file)

    # display_image('output_png', target_file)

    peak = monitor.stop()
    print(f"Peak memory usage: {peak / 1024**2:.2f} MB")

    return target_file


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
    process_image(args.input_image)
