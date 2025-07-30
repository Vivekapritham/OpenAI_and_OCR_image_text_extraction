
from tkinter import Tk, filedialog
from PIL import Image
import pytesseract

# Optional: Set Tesseract path if needed
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

Tk().withdraw()

file_path = filedialog.askopenfilename(
    title="Select an Image",
    filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")]
)

if file_path:
    image = Image.open(file_path)

    # Use multiple languages: Tamil, Hindi, Telugu, Kannada, Malayalam, Bengali, English
    text = pytesseract.image_to_string(image, lang='tam+hin+tel+kan+mal+ben+eng')

    print("\n📌 Extracted Text:\n")
    print(text)
else:
    print("❌ No image selected.")
