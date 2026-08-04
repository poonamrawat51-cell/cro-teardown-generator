import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Page Setup
st.set_page_config(
    page_title="SaaS CRO Teardown Generator",
    page_icon="⚡",
    layout="wide"
)

# 2. Sidebar Configuration for API Key
st.sidebar.title("⚙️ Configuration")
import streamlit as st
import google.generativeai as genai

# Sidebar input for custom key
user_key = st.sidebar.text_input("Enter Gemini API Key (Optional)", type="password")

# Use user key if provided; otherwise, fallback to your Streamlit Secret
api_key = user_key if user_key else st.secrets.get("GEMINI_API_KEY", "")

if api_key:
    genai.configure(api_key=api_key)
else:
    st.sidebar.warning("Please provide a Gemini API Key to proceed.")
if not api_key:
    st.info("👈 Enter your Gemini API Key in the sidebar to start!")
    st.stop()

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-flash-latest')

# 3. Main Interface Header
st.title("⚡ SaaS Landing Page CRO & Video Script Generator")
st.write("Upload a screenshot or paste copy to generate a 60-second video audit script and CRO teardown.")

st.divider()

# 4. User Inputs
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. Upload Screenshot")
    uploaded_file = st.file_uploader("Upload Landing Page Image", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Landing Page UI", use_container_width=True)

with col2:
    st.subheader("2. Additional Details (Optional)")
    hero_copy = st.text_area("Paste Headline / Copy Text:", placeholder="e.g., The All-In-One CRM for B2B Teams...")
    target_audience = st.text_input("Target Audience / ICP:", placeholder="e.g., Marketing Managers, SaaS Founders...")
    
    generate_btn = st.button("🚀 Generate CRO Audit & Script", type="primary", use_container_width=True)

# 5. Processing & Output Generation
if generate_btn:
    if not uploaded_file and not hero_copy:
        st.error("Please upload a screenshot OR paste copy text to analyze.")
        st.stop()

    with st.spinner("Analyzing UI, visual hierarchy, and messaging..."):
        prompt = f"""
        You are an expert Conversion Rate Optimization (CRO) strategist and Video Scriptwriter.
        Analyze the provided landing page image and text context.

        Audience Context: {target_audience if target_audience else 'B2B / SaaS Buyers'}
        Provided Text: {hero_copy if hero_copy else 'Refer to the screenshot.'}

        Provide your analysis in two sections:

        SECTION 1: TOP 3 CRO RECOMMENDATIONS
        Highlight 3 major conversion issues (visual hierarchy, CTA clarity, white space, value prop). 
        Format as clear bullet points with bold headers.

        SECTION 2: 60-SECOND LOOM / TIKTOK VIDEO AUDIT SCRIPT
        Write a structured video script with timestamps (0-15s, 15-30s, 30-45s, 45-60s).
        Include:
        - [Visual Cue]: What to show or highlight on screen.
        - [Dialogue]: Concise, high-converting spoken lines (Hook -> Problem -> Fix -> CTA).
        """

        try:
            inputs = [prompt]
            if uploaded_file:
                inputs.append(image)

            response = model.generate_content(inputs)
            
            st.divider()
            st.success("Analysis Complete!")
            st.markdown(response.text)

        except Exception as e:
            st.error(f"Error generating analysis: {e}")
