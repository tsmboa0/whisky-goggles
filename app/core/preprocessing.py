from PIL import ImageEnhance, Image

def enhance_image(image: Image.Image) -> Image.Image:
    image = image.convert("RGB")
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)  # Increase contrast
    return image