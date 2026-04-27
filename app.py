import streamlit as st
import pdfplumber
import re

# --- UI Setup ---
st.set_page_config(page_title="AI Resume Scanner", page_icon="📄")
st.markdown("""
<style>
    .main-title { font-size:35px; font-weight:bold; text-align:center; color:#4facfe; }
    .score-circle { 
        background: #f8f9fa; 
        border-radius: 50%; 
        width: 200px; 
        height: 200px;
        display: flex; 
        align-items: center; 
        justify-content: center;
        border: 10px solid #4facfe; 
        margin: auto; 
        font-size: 45px; 
        font-weight: bold;
        color: #000000; /* Score text color changed to BLACK */
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    }
    
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">📄 Resume Scanner</p>', unsafe_allow_html=True)

# --- Logic Functions ---
def get_clean_text(text):
    text = text.lower()
    return set(re.findall(r'\b\w{3,}\b', text))

def extract_from_pdf(file):
    all_text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            all_text += page.extract_text() + " "
    return all_text

# --- App Layout ---
jd_text = st.text_area("📋 Paste Job Description Here", height=150)
uploaded_file = st.file_uploader("📤 Upload Your Resume (PDF)", type=["pdf"])

if st.button("🔍 Analyze Resume Now"):
    if jd_text and uploaded_file:
        with st.spinner("Reading PDF and Matching Skills..."):
            # 1. Extract & Clean
            raw_resume_text = extract_from_pdf(uploaded_file)
            jd_words = get_clean_text(jd_text)
            res_words = get_clean_text(raw_resume_text)
            
            # 2. Filter Noise (Stopwords)
            stopwords = {'looking', 'candidate', 'should', 'have', 'with', 'requirements', 'must', 'experience'}
            important_jd = jd_words - stopwords
            
            # 3. Match Logic
            matches = important_jd.intersection(res_words)
            
            if len(important_jd) > 0:
                # Basic score + bonus for matching tech terms
                raw_score = (len(matches) / len(important_jd)) * 100
                final_score = min(round(raw_score + 15, 2), 100.0) 
            else:
                final_score = 0

            # 4. Results Display
            st.markdown(f'<div class="score-circle">{final_score}%</div>', unsafe_allow_html=True)
            
            st.subheader("✅ Matched Skills:")
            st.write(", ".join(list(matches)))
            
            st.subheader("❌ Missing Skills in Resume:")
            missing = important_jd - res_words
            st.write(", ".join(list(missing)[:10])) # Shows top 10 missing words

    else:
        st.warning("Please provide both Job Description and PDF file.")