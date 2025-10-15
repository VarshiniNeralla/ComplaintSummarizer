import streamlit as st
import os
import easyocr
from groq import Groq
from dotenv import load_dotenv
from PIL import Image
import tempfile

# ---------------- Setup ----------------
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    st.error("❌ GROQ_API_KEY not found. Please set it in a .env file.")
    st.stop()

groq_client = Groq(api_key=groq_api_key)
MODEL_NAME = "llama-3.3-70b-versatile"

reader = easyocr.Reader(['en'], verbose=False)

# ---------------- Helper: Groq Summarizer ----------------
def groq_summarize(text):
    """Summarize text using Groq's LLaMA 3.3 70B Versatile model."""
    prompt = (
        "Summarize the following police complaint clearly and concisely. "
        "Keep all critical details such as dates, names, locations, stolen items, "
        "financial losses, and legal actions requested:\n\n" + text
    )

    response = groq_client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content.strip()

# ---------------- Streamlit UI ----------------
st.set_page_config(page_title="Police Complaint Summarizer", layout="wide")

st.title("Police Complaint Summarizer llama 3.3 70b")
st.markdown(
    "This app extracts and summarizes police complaints using **Groq’s LLaMA 3.3 70B Versatile** model."
)

tab1, tab2 = st.tabs(["📄 Upload Complaint Image", "📝 Paste Complaint Text"])

# ---------- TAB 1: OCR + Summarize ----------
with tab1:
    uploaded_file = st.file_uploader("Upload an image (JPG, PNG)", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Complaint", use_column_width=True)

        if st.button("Summarize from Image"):
            with st.spinner("Extracting text and summarizing..."):
                try:
                    # Save temporarily for EasyOCR
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp:
                        temp.write(uploaded_file.read())
                        temp_path = temp.name

                    # OCR extraction
                    result = reader.readtext(temp_path, detail=0)
                    os.remove(temp_path)

                    extracted_text = " ".join(result)
                    if not extracted_text.strip():
                        st.error("No text detected in the image.")
                    else:
                        summary = groq_summarize(extracted_text)
                        st.subheader("📜 Summarized Complaint")
                        st.write(summary)
                except Exception as e:
                    st.error(f"Error during OCR or summarization: {e}")

# ---------- TAB 2: Text + Summarize ----------
with tab2:
    text_input = st.text_area("Paste your complaint text here:", height=300)

    if st.button("Summarize Text Complaint"):
        if not text_input.strip():
            st.warning("Please enter a complaint before summarizing.")
        else:
            with st.spinner("Summarizing your complaint..."):
                try:
                    summary = groq_summarize(text_input)
                    st.subheader("📜 Summarized Complaint")
                    st.write(summary)
                except Exception as e:
                    st.error(f"Error during summarization: {e}")
