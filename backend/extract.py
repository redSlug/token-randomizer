import cv2
import numpy as np
from PIL import Image
import os
import sys
import argparse


def extract_objects_connected(input_path, output_dir):
    try:
        os.makedirs(output_dir, exist_ok=True)
    except Exception as e:
        print(f"Error creating output directory: {e}")

    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img.shape[2] < 4:
        raise ValueError("Image has no transparency channel; it's not really png")

    alpha = img[:, :, 3]

    # Threshold the alpha channel to binary mask
    _, binary_mask = cv2.threshold(alpha, 10, 255, cv2.THRESH_BINARY)

    # Remove noise by morphological operations (optional but helpful)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    cleaned_mask = cv2.morphologyEx(binary_mask, cv2.MORPH_OPEN, kernel, iterations=2)

    # Find connected components
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(
        cleaned_mask, connectivity=8
    )

    print(f"Found {num_labels - 1} objects.")  # label 0 is background

    for label in range(1, num_labels):  # Skip background
        x, y, w, h, area = stats[label]

        # Skip very small areas (e.g., noise that survived cleaning)
        if area < 100:
            print(f"Skipping object {label} with area {area} pixels.")
            continue

        # Mask for current component
        component_mask = (labels == label).astype(np.uint8) * 255
        object_alpha = cv2.bitwise_and(alpha, alpha, mask=component_mask)
        object_rgb = cv2.bitwise_and(img[:, :, :3], img[:, :, :3], mask=component_mask)

        # Combine RGB and alpha
        object_rgba = cv2.merge((object_rgb, object_alpha))

        # Crop to bounding box
        cropped = cv2.cvtColor(object_rgba[y : y + h, x : x + w], cv2.COLOR_BGRA2RGBA)

        # Save with PIL
        output_path = os.path.join(output_dir, f"object_{label}.png")
        Image.fromarray(cropped).save(output_path)
        print(f"Saved: {output_path}")

    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract objects from a PNG based on transparency, filtering noise."
    )
    parser.add_argument(
        "input_png", help="Path to the input PNG file (with transparency)."
    )
    parser.add_argument(
        "output_dir", help="Directory to save the extracted object PNG files."
    )
    parser.add_argument(
        "-min",
        "--min-area",
        type=int,
        default=100,
        help="Minimum contour area to consider an object (default: 100 pixels).",
    )

    args = parser.parse_args()

    if not args.input_png.lower().endswith(".png"):
        print(
            f"Warning: Input file '{args.input_png}' should be a PNG file, preferably with transparency.",
            file=sys.stderr,
        )

    success = extract_objects_connected(args.input_png, args.output_dir)

    if not success:
        sys.exit(1)
