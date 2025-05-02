import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from PIL import Image
from app.core.recognizer import Recognizer

# Initialize the recognizer pipeline
print("Starting test...")
recog = Recognizer()
print("Initialized recognizer")

# Path to a test image (replace with an actual test image path)
test_image_path = os.path.join(os.path.dirname(__file__), '../data/bottle_images/3123.jpg')  # Example image containing multiple bottles
print("path initislized")
try:
    image = Image.open(test_image_path).convert("RGB")
    print("image conversted to RGB")
except FileNotFoundError:
    print(f"Test image not found at {test_image_path}")
    exit(1)

# Run the recognition
print("starting to call the recognize function")
results = recog.recognize(image)
print("function done")

# Print the results
if not results:
    print("No whisky bottles were recognized.")
else:
    print("Recognized bottles:")
    for match in results:
        print(f"The final result is: {match}")
        # name = match.get("name")
        # region = match.get("region")
        # abv = match.get("abv")
        # score = match.get("score")
        # label_text = match.get("label_text")
        # print(f" - {name} ({region}, ABV: {abv}%) with confidence {score:.2f}. Label text: '{label_text}'")
