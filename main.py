from PIL import Image, ImageFilter, ImageOps
import pytesseract

# If you're on Windows, uncomment and update this path
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load and preprocess image
image = Image.open("img3.jpg")                # Replace with your image file
gray = ImageOps.grayscale(image)                    # Convert to grayscale
gray = gray.filter(ImageFilter.MedianFilter())      # Reduce noise

# OCR
text = pytesseract.image_to_string(gray)            # You can add lang='eng' or other languages if needed

print("Extracted Text:\n", text)
