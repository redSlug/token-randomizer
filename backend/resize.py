

import cv2

def resize_jpg(input_path, output_path=None, max_size=768):
    """
    Resize a JPG image so that the largest dimension is max_size pixels.

    Args:
        input_path (str): Path to input JPG file.
        output_path (str, optional): Path to save resized JPG. If None, overwrites input.
        max_size (int): Maximum size for the largest dimension (width or height).
    """
    # Load the image
    img = cv2.imread(input_path)

    if img is None:
        raise ValueError(f"Cannot open image: {input_path}")

    height, width = img.shape[:2]

    # Check if resizing needed
    max_dim = max(width, height)
    if max_dim <= max_size:
        print("Image is already small enough, no resizing needed.")
        return

    # Compute scale and new size
    scale = max_size / max_dim
    new_width = int(width * scale)
    new_height = int(height * scale)

    # Resize the image
    resized_img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)

    # Save the resized image
    if output_path is None:
        output_path = input_path  # Overwrite the original

    cv2.imwrite(output_path, resized_img)
    print(f"Resized image saved to {output_path}")