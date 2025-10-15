import streamlit as st
import requests
import os
from PIL import Image
import io
import base64

# Page configuration
st.set_page_config(
    page_title="Complaint Summarizer",
    page_icon="📄",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .error-box {
        padding: 1rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<h1 class="main-header"> 📄 Complaint Summarizer llama 3.1 8b</h1>', unsafe_allow_html=True)

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Backend URL configuration
    backend_url = st.text_input(
        "Backend URL", 
        value="http://localhost:5000",
        help="URL where your Flask backend is running"
    )
    
    st.markdown("---")
    st.markdown("### Instructions")
    st.markdown("""
    1. **Upload Image**: Upload a complaint document image for OCR extraction and summarization
    2. **Enter Text**: Or directly paste complaint text for summarization
    3. **Get Summary**: Receive a concise, legally-relevant summary
    """)

# Main content area
tab1, tab2 = st.tabs(["📷 Upload Image", "✏️ Enter Text"])

with tab1:
    st.markdown('<h2 class="section-header">📷 Upload Complaint Image</h2>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=['png', 'jpg', 'jpeg', 'bmp', 'tiff'],
        help="Upload a complaint document image for OCR extraction and summarization"
    )
    
    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image",  use_container_width=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.button("🔍 Extract & Summarize", type="primary", use_container_width=True):
                with st.spinner("Processing image and generating summary..."):
                    try:
                        # Prepare the file for upload
                        files = {'file': (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                        
                        # Make request to backend
                        response = requests.post(f"{backend_url}/ocr-summarize", files=files)
                        
                        if response.status_code == 200:
                            result = response.json()
                            summary = result.get('summary', 'No summary generated')
                            
                            st.markdown('<div class="success-box">', unsafe_allow_html=True)
                            st.markdown("### ✅ Summary Generated Successfully!")
                            st.markdown("</div>", unsafe_allow_html=True)
                            
                            st.markdown("### 📝 Complaint Summary:")
                            st.markdown(summary)
                            
                            # Download button for summary
                            st.download_button(
                                label="💾 Download Summary",
                                data=summary,
                                file_name=f"complaint_summary_{uploaded_file.name.split('.')[0]}.txt",
                                mime="text/plain"
                            )
                        else:
                            error_msg = response.json().get('error', 'Unknown error occurred')
                            st.markdown('<div class="error-box">', unsafe_allow_html=True)
                            st.markdown(f"### ❌ Error: {error_msg}")
                            st.markdown("</div>", unsafe_allow_html=True)
                            
                    except requests.exceptions.ConnectionError:
                        st.markdown('<div class="error-box">', unsafe_allow_html=True)
                        st.markdown("### ❌ Connection Error")
                        st.markdown("Could not connect to the backend. Please ensure your Flask app is running.")
                        st.markdown("</div>", unsafe_allow_html=True)
                    except Exception as e:
                        st.markdown('<div class="error-box">', unsafe_allow_html=True)
                        st.markdown(f"### ❌ Error: {str(e)}")
                        st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            st.markdown("### 💡 Tips for Better Results")
            st.markdown("""
            - Ensure the image is clear and well-lit
            - Text should be readable and not blurry
            - Avoid images with heavy shadows or glare
            - Higher resolution images work better
            """)
            st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.markdown('<h2 class="section-header">✏️ Enter Complaint Text</h2>', unsafe_allow_html=True)
    
    complaint_text = st.text_area(
        "Paste your complaint text here:",
        height=200,
        placeholder="Enter the complaint text that you want to summarize..."
    )
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("📝 Summarize Text", type="primary", use_container_width=True):
            if complaint_text.strip():
                with st.spinner("Generating summary..."):
                    try:
                        # Prepare the data for the request
                        data = {'text': complaint_text}
                        
                        # Make request to backend
                        response = requests.post(f"{backend_url}/summarize-text", json=data)
                        
                        if response.status_code == 200:
                            result = response.json()
                            summary = result.get('summary', 'No summary generated')
                            
                            st.markdown('<div class="success-box">', unsafe_allow_html=True)
                            st.markdown("### ✅ Summary Generated Successfully!")
                            st.markdown("</div>", unsafe_allow_html=True)
                            
                            st.markdown("### 📝 Complaint Summary:")
                            st.markdown(summary)
                            
                            # Download button for summary
                            st.download_button(
                                label="💾 Download Summary",
                                data=summary,
                                file_name="complaint_summary.txt",
                                mime="text/plain"
                            )
                        else:
                            error_msg = response.json().get('error', 'Unknown error occurred')
                            st.markdown('<div class="error-box">', unsafe_allow_html=True)
                            st.markdown(f"### ❌ Error: {error_msg}")
                            st.markdown("</div>", unsafe_allow_html=True)
                            
                    except requests.exceptions.ConnectionError:
                        st.markdown('<div class="error-box">', unsafe_allow_html=True)
                        st.markdown("### ❌ Connection Error")
                        st.markdown("Could not connect to the backend. Please ensure your Flask app is running.")
                        st.markdown("</div>", unsafe_allow_html=True)
                    except Exception as e:
                        st.markdown('<div class="error-box">', unsafe_allow_html=True)
                        st.markdown(f"### ❌ Error: {str(e)}")
                        st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.markdown('<div class="error-box">', unsafe_allow_html=True)
                st.markdown("### ❌ Please enter some text to summarize")
                st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("### 📋 About Text Summarization")
        st.markdown("""
        The AI will:
        - Extract key legal information
        - Identify important dates and details
        - Summarize in a concise, legally-relevant format
        - Preserve critical facts and requests
        """)
        st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #7f8c8d; padding: 1rem;'>
        <p>📄 Complaint Summarizer - Powered by Streamlit & Groq AI</p>
    </div>
    """, 
    unsafe_allow_html=True
)
