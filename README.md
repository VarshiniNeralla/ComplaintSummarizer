# Complaint Summarizer

A web-based tool to extract and summarize complaints from text or images. The system produces concise, detailed, and context-aware summaries while preserving all critical information.

## Features

- Accepts input as **text** or **image**.
- Extracts text from images using OCR.
- Summarizes complaints, retaining essential details like:
  - Dates
  - Incidents
  - Stolen or damaged items
  - Financial details
  - Legal requests
- Generates concise, legally-relevant summaries.
- Built with **Streamlit** for interactive UI.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd complaint-summarizer
2. source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate
3. pip install -r requirements.txt
4. streamlit run app.py
