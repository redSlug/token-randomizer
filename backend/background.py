from rembg import remove
from PIL import Image
import sys
import os


def remove_background(input_path, output_path):
    """Removes the background from an image using rembg.
    Returns True on success, False on failure.
    """
    try:
        input_image = Image.open(input_path)

        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        output_image = remove(
            input_image,
            alpha_matting=True,
            alpha_matting_foreground_threshold=2,
        )
        # Ensure output is RGBA to handle transparency
        if output_image.mode != "RGBA":
            output_image = output_image.convert("RGBA")
        output_image.save(output_path)
        print(f"Background removed. Output saved to: {output_path}")
        return True  # Indicate success
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_path}", file=sys.stderr)
        return False  # Indicate failure
    except Exception as e:
        print(f"An error occurred during background removal: {e}", file=sys.stderr)
        return False  # Indicate failure


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python rm-bg.py <input_image_path> <output_image_path>")
        print("Example: python rm-bg.py src/coins1.jpg src/coins1_no_bg.png")
        sys.exit(1)

    input_img_path = sys.argv[1]
    # Ensure output is PNG to preserve transparency
    output_img_path = sys.argv[2]
    if not output_img_path.lower().endswith(".png"):
        print(
            "Warning: Output file should ideally be a .png to preserve transparency.",
            file=sys.stderr,
        )

    # Call the function and exit based on its success
    success = remove_background(input_img_path, output_img_path)
    if not success:
        sys.exit(1)
