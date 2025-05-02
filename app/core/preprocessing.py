from io import BytesIO
from PIL import Image
import numpy as np

try:
    # rembg for background removal (optional: if installed)
    from rembg import remove
except ImportError:
    remove = None

try:
    import cv2  # OpenCV for finding contours
except ImportError:
    cv2 = None

def remove_background(image, session=None):
    """
    Remove background from the given PIL image using rembg. Returns a PIL image with alpha channel.
    """
    if remove is None:
        # If rembg is not available, return original image
        return image
    # If a session is provided (to avoid model re-loading), use it
    if session:
        output = remove(image, session=session)
    else:
        output = remove(image)
    return output

def segment_bottles(image):
    """
    Identify and crop individual bottle regions from a background-removed image.
    Returns a list of PIL images for each detected bottle.
    """
    if cv2 is None:
        # Fallback: if OpenCV not available, return the whole image as single segment
        return [image]
    # Ensure image has an alpha channel (from background removal)
    if image.mode != "RGBA":
        image = image.convert("RGBA")
    # Create mask from alpha channel
    alpha = np.array(image.split()[-1])
    # Binarize the alpha mask
    _, thresh = cv2.threshold(alpha, 1, 255, cv2.THRESH_BINARY)
    # Find contours of the binary mask (each contour should correspond to a bottle)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    bottle_crops = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w < 10 or h < 10:
            continue  # skip tiny regions (noise)
        # Crop the region from the original image (to retain actual colors)
        crop = image.crop((x, y, x + w, y + h))
        # Convert cropped image to RGB (fill background with white if transparent)
        if crop.mode == "RGBA":
            bg = Image.new("RGBA", crop.size, (255, 255, 255, 255))
            bg.paste(crop, mask=crop.split()[3])
            crop = bg.convert("RGB")
        else:
            crop = crop.convert("RGB")
        bottle_crops.append(crop)
    # If no contours found, return the original image as a single segment
    if not bottle_crops:
        bottle_crops = [image.convert("RGB")]
    return bottle_crops

def preprocess_image(image, session=None):
    """
    Full preprocessing pipeline: remove background and split into individual bottle images.
    """
    # Step 1: Remove background from the image (makes bottle regions easier to isolate)
    img_no_bg = remove_background(image, session=session)
    # Step 2: Segment the image into separate bottles
    bottle_images = segment_bottles(img_no_bg)
    return bottle_images
