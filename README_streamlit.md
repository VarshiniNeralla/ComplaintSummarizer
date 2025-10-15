# Complaint Summarizer - Streamlit Frontend

A Streamlit-based frontend for the Complaint Summarizer application that provides OCR text extraction and AI-powered summarization of police complaints.

## Features

- 📷 **Image Upload**: Upload complaint document images for OCR extraction and summarization
- ✏️ **Text Input**: Direct text input for summarization
- 🤖 **AI Summarization**: Powered by Groq's LLaMA 3.1 8B Instant model
- 💾 **Download Results**: Download summaries as text files
- 🎨 **Modern UI**: Clean, responsive interface with custom styling

## Prerequisites

- Python 3.7+
- Flask backend running (app2.py)
- Groq API key configured in your environment

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements_streamlit.txt
```

2. Make sure your Flask backend is running:
```bash
cd backend
python app2.py
```

3. Run the Streamlit app:
```bash
streamlit run streamlit_app.py
```

## Usage

### Option 1: Upload Image
1. Go to the "📷 Upload Image" tab
2. Upload a complaint document image (PNG, JPG, JPEG, BMP, TIFF)
3. Click "🔍 Extract & Summarize"
4. View and download the generated summary

### Option 2: Enter Text
1. Go to the "✏️ Enter Text" tab
2. Paste your complaint text in the text area
3. Click "📝 Summarize Text"
4. View and download the generated summary

## Configuration

- **Backend URL**: Configure the Flask backend URL in the sidebar (default: http://localhost:5000)
- **API Key**: Ensure your Groq API key is set in the environment variables

## File Structure

```
complaint-summarizer/
├── streamlit_app.py          # Main Streamlit application
├── requirements_streamlit.txt # Python dependencies
├── README_streamlit.md       # This file
└── backend/
    ├── app2.py              # Flask backend
    └── ...
```

## Troubleshooting

### Connection Error
- Ensure your Flask backend is running on the specified URL
- Check that the backend URL in the sidebar is correct

### No Text Detected
- Ensure the uploaded image is clear and well-lit
- Try a higher resolution image
- Check that the text in the image is readable

### API Errors
- Verify your Groq API key is correctly set in the environment
- Check your internet connection
- Ensure you have sufficient API credits

## Dependencies

- `streamlit`: Web app framework
- `requests`: HTTP client for API calls
- `Pillow`: Image processing
- `python-dotenv`: Environment variable management

## Backend Integration

The Streamlit app communicates with the Flask backend through two endpoints:
- `/ocr-summarize`: For image upload and OCR processing
- `/summarize-text`: For direct text summarization

Make sure your backend is running and accessible before using the Streamlit frontend.
