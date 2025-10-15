from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import easyocr
from groq import Groq

from dotenv import load_dotenv
load_dotenv()   
groq_api_key = os.getenv("GROQ_API_KEY")

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------- OCR ----------------
reader = easyocr.Reader(['en'])

# ---------------- Groq Client ----------------
# Replace YOUR_API_KEY with your actual Groq API key
groq_client = Groq(api_key=groq_api_key)
MODEL_NAME = "llama-3.1-8b-instant"

def groq_summarize(text):
    """
    
    Summarizes text using Groq's LLaMA 3.1 8B Instant model.
    
    """    
    
    prompt = (
        "Summarize the following police complaint clearly and concisely. "
        "Keep all critical details such as dates, names, locations, stolen items, "
        "financial losses, and legal actions requested:\n\n" + text
    )
    
    response = groq_client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# ---------------- Routes ----------------
@app.route('/ocr-summarize', methods=['POST'])
def ocr_summarize():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    # Step 1: OCR extraction
    result = reader.readtext(path, detail=0)
    extracted_text = " ".join(result)

    if not extracted_text.strip():
        return jsonify({'error': 'No text detected in image'}), 400

    # Step 2: Groq summarization
    summary = groq_summarize(extracted_text)
    return jsonify({'summary': summary})

@app.route('/summarize-text', methods=['POST'])
def summarize_text():
    data = request.get_json()
    text = data.get('text', '')

    if not text.strip():
        return jsonify({'error': 'No text provided'}), 400

    summary = groq_summarize(text)
    return jsonify({'summary': summary})

if __name__ == '__main__':
    app.run(debug=True)
