import streamlit as st
import requests
import json

# -----------------------
# Page configuration
# -----------------------
st.set_page_config(
    page_title="📰 Fake News Detector",
    page_icon="📰",
    layout="centered"
)

# -----------------------
# Header
# -----------------------
st.markdown(
    "<h1 style='text-align: center; color: #E74C3C;'>📰 Fake News Detector</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align: center;'>Paste any news article below and our AI fact-checking assistant will analyze it.</p>",
    unsafe_allow_html=True
)
st.divider()

# -----------------------
# Sidebar info
# -----------------------
st.sidebar.header("Instructions")
st.sidebar.markdown("""
- Paste the text of the news article you want to check.
- Click **Analyze** to get the AI’s evaluation.
- Type 'exit' or leave blank to cancel.
- Powered by OpenRouter API and Gemma-3n-e2b-it model.
""")

# -----------------------
# API Configuration
# -----------------------
API_KEY = ""  # Replace with your key
MODEL = "google/gemma-3n-e2b-it:free"

# -----------------------
# News input
# -----------------------
news_text = st.text_area("Paste the news article here:")

# -----------------------
# Analyze button
# -----------------------
if st.button("Analyze"):
    if not news_text.strip():
        st.warning("⚠️ Please paste some news text to analyze.")
    else:
        with st.spinner("Analyzing news..."):
            try:
                response = requests.post(
                    url="https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {API_KEY}",
                        "Content-Type": "application/json"
                    },
                    data=json.dumps({
                        "model": MODEL,
                        "messages": [
                            {
                                "role": "user",
                                "content": f"You are a fact-checking assistant. Analyze this news and tell if it is likely fake or reliable. Explain why, keeping your explanation concise and answer in points concisely:\n{news_text}"
                            }
                        ]
                    })
                )

                if response.status_code == 200:
                    data = response.json()
                    answer = data["choices"][0]["message"]["content"]
                    st.markdown("### 📝 News Analysis Result")
                    st.info(answer)
                else:
                    st.error(f"API Error {response.status_code}: {response.text}")

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

st.divider()

# -----------------------
# Footer
# -----------------------
st.markdown(
    "<p style='text-align:center; font-size:12px;'>Developed by You | Powered by OpenRouter API & Gemma Model 🚀</p>",
    unsafe_allow_html=True
)
