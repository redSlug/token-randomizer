from PIL import Image
import numpy as np
import argparse
import sys
import os


def get_transparency_percentage(png_path):
    """Calculates the percentage of transparent pixels in a PNG image.

    Args:
        png_path (str): Path to the input PNG file.

    Returns:
        float: The percentage of transparent pixels (0.0 to 100.0),
               or None if the file cannot be opened or has no alpha channel.
    """
    try:
        img = Image.open(png_path)
        if img.mode != "RGBA":
            # If not RGBA, try converting. If it fails, it had no alpha.
            try:
                img = img.convert("RGBA")
            except ValueError:
                print(
                    f"Error: Image at '{png_path}' does not have an alpha channel or could not be converted.",
                    file=sys.stderr,
                )
                return None

        alpha = np.array(img)[:, :, 3]  # Extract alpha channel

        total_pixels = alpha.size
        if total_pixels == 0:
            return 0.0  # Avoid division by zero for empty images

        # Consider pixels with alpha < threshold as transparent
        # Using a small threshold like 10 accounts for near-transparent pixels
        transparency_threshold = 10
        transparent_pixels = np.sum(alpha < transparency_threshold)

        percent_transparent = (transparent_pixels / total_pixels) * 100
        return percent_transparent
    except FileNotFoundError:
        print(f"Error: File not found at '{png_path}'", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error processing image '{png_path}': {e}", file=sys.stderr)
        return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Calculate the percentage of transparent pixels in a PNG image."
    )
    parser.add_argument("input_png", help="Path to the input PNG file.")

    args = parser.parse_args()

    if not args.input_png.lower().endswith(".png"):
        print(
            f"Warning: Input file '{args.input_png}' should be a PNG file.",
            file=sys.stderr,
        )

    percentage = get_transparency_percentage(args.input_png)

    if percentage is not None:
        print(f"Transparency: {percentage:.2f}%")
        print(f"Opaque: {100.0 - percentage:.2f}%")
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Failure indicated by the function
