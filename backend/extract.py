import cv2
import numpy as np
import os
import sys
import argparse
import random


def draw_bounding_box(input_path, orig_path, output_path, min_area=100):
    # Read RGB image for object detection
    img_for_detection = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img_for_detection is None:
        print(f"Error: Could not read detection image {input_path}", file=sys.stderr)
        return False

    # Read the original image to draw on
    img_to_draw_on = cv2.imread(orig_path, cv2.IMREAD_UNCHANGED) # Read with alpha if present
    if img_to_draw_on is None:
        print(f"Error: Could not read original image {orig_path}", file=sys.stderr)
        return False

    # Prepare image for drawing: Needs to handle different formats
    draw_on_has_alpha = False
    if len(img_to_draw_on.shape) == 3 and img_to_draw_on.shape[2] == 4:    # Already BGRA, good to go
        draw_on_has_alpha = True
    elif len(img_to_draw_on.shape) == 3 and img_to_draw_on.shape[2] == 3:  # Is BGR, good to go
        pass

    # Threshold the alpha channel
    alpha = img_for_detection[:, :, 3]
    _, binary_mask = cv2.threshold(alpha, 10, 255, cv2.THRESH_BINARY)

    # Find connected components
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(
        binary_mask, connectivity=8
    )

    print(f"Found {num_labels - 1} potential objects in {os.path.basename(input_path)}.")

    # Collect valid boxes and select one randomly
    valid_boxes = []
    for label in range(1, num_labels): # Skip background (label 0)
        x, y, w, h, area = stats[label]
        if area >= min_area:
            # Draw circles on all found tokens
            color = (0, 0, 0, 255) if draw_on_has_alpha else (0, 0, 255)
            center = (x + w // 2, y + h // 2)
            radius = min(w // 2, h // 2)
            cv2.circle(img_to_draw_on, center, radius, color, 2)
            print(f"Drew all bounding circles onto {os.path.basename(orig_path)}.")

            valid_boxes.append((x, y, w, h)) # Store coordinates directly

    if not valid_boxes:
        print(f"No objects found meeting the minimum area requirement ({min_area} pixels).")
    else:
        print(f"Found {len(valid_boxes)} objects meeting the area criteria.")
        # Select one box randomly
        selected_box = random.choice(valid_boxes)
        x, y, w, h = selected_box

        # Draw the selected circle on the img_to_draw_on
        color = (0, 255, 255, 255) if draw_on_has_alpha else (255, 255, 255) # Changed BGR color to white for selected, was (0,0,255) red
        center = (x + w // 2, y + h // 2)
        radius = min(w // 2, h // 2)
        cv2.circle(img_to_draw_on, center, radius, color, 2)
        print(f"Drew 1 randomly selected bounding circle onto {os.path.basename(orig_path)}.")

    # Save the modified (or original if no box drawn) drawing image
    try:
        cv2.imwrite(output_path, img_to_draw_on)
        print(f"Saved final image to: {output_path}")
        return True
    except Exception as e:
        print(f"Error saving output image: {e}", file=sys.stderr)
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Detect objects based on alpha channel of an input image and draw bounding boxes onto a separate original image."
    )
    parser.add_argument(
        "input_png", help="Path to the input image file (e.g., PNG with alpha) used for object detection."
    )
    parser.add_argument(
        "original_image", help="Path to the original image file (e.g., JPG, PNG) onto which boxes will be drawn."
    )
    parser.add_argument(
        "output_file", help="Path to save the output image (original_image with boxes drawn)."
    )
    parser.add_argument(
        "min-area",
        type=int,
        default=100,
        help="Minimum object area (from input_image) to draw a box around (default: 100 pixels).",
    )

    args = parser.parse_args()

    # Basic checks if inputs exist
    if not args.input_png.lower().endswith(".png"):
        print(f"Warning: Input file '{args.input_png}' should be a PNG file, preferably with transparency.", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(args.original_image):
        print(f"Error: Original image file not found at {args.original_image}", file=sys.stderr)
        sys.exit(1)

    success = draw_bounding_box(args.input_png, args.original_image, args.output_file, args.min_area)

    if not success:
        sys.exit(1)
