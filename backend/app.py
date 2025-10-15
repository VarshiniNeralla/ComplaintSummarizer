from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import easyocr
from transformers import pipeline

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize OCR and Summarizer
reader = easyocr.Reader(['en'])
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

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

    # Step 2: Summarization
    summary = summarizer(extracted_text, max_length=150, min_length=50, do_sample=False)
    return jsonify({'summary': summary[0]['summary_text']})

@app.route('/summarize-text', methods=['POST'])
def summarize_text():
    data = request.get_json()
    text = data.get('text', '')

    if not text.strip():
        return jsonify({'error': 'No text provided'}), 400

    summary = summarizer(text, max_length=150, min_length=50, do_sample=False)
    return jsonify({'summary': summary[0]['summary_text']})

if __name__ == '__main__':
    app.run(debug=True)
