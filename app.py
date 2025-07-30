from flask import Flask, render_template, request, send_from_directory
from PIL import Image, UnidentifiedImageError
from werkzeug.utils import secure_filename
from openai import OpenAI
import pytesseract
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Allowed file types
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

client = OpenAI()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def clean_text_with_openai(raw_text):
    prompt = f"""
    The following text was extracted from an image using OCR. 
    It may contain spelling errors or formatting issues. Clean it up and return a corrected, readable version.

    OCR Text:
    {raw_text}
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that cleans up OCR text."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ OpenAI processing failed: {str(e)}"

@app.route('/', methods=['GET', 'POST'])
def index():
    extracted_text = ""
    uploaded_image = None

    if request.method == 'POST':
        if 'image' not in request.files:
            return render_template('index.html', text="⚠️ No file uploaded.")

        file = request.files['image']
        if file.filename == '':
            return render_template('index.html', text="⚠️ No file selected.")

        if not allowed_file(file.filename):
            return render_template('index.html', text="⚠️ Unsupported file type. Please upload PNG, JPG, JPEG, or GIF.")

        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        uploaded_image = filename  # for preview

        try:
            image = Image.open(filepath)
        except UnidentifiedImageError:
            return render_template('index.html', text="⚠️ Could not identify image. Please upload a valid image file.")
        except Exception as e:
            return render_template('index.html', text=f"⚠️ Image error: {str(e)}")

        method = request.form.get('method', 'tesseract')
        raw_text = pytesseract.image_to_string(image, lang='tam+hin+tel+kan+mal+ben+eng')
        print(f"[DEBUG] Extracted Text:\n{raw_text}")  # Debug print

        if method == 'openai':
            extracted_text = clean_text_with_openai(raw_text)
        else:
            extracted_text = raw_text

    return render_template('index.html', text=extracted_text, image=uploaded_image)

if __name__ == '__main__':
    app.run(debug=True)
