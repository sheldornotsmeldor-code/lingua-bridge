import streamlit as st
import google.generativeai as genai
import pandas as pd
import os

# --- CONFIGURATION ---
# 1. SETUP API KEY
# Replace 'YOUR_GEMINI_API_KEY_HERE' with your actual key.
api_key = "AIzaSyCSU5mhIX-BLbKaW_U9p7kxuDt9cHkoccc"

if not api_key or "YOUR_GEMINI" in api_key:
    st.error("⚠️ Please enter your Google Gemini API Key in the code!")
    st.stop()

genai.configure(api_key=api_key)

# 2. SETUP PAGE
st.set_page_config(page_title="Sheldor's LinguaBridge", page_icon="🌉", layout="wide")

# --- DATA STORAGE (PANDAS) ---
CSV_FILE = "my_vocab.csv"

def load_vocab():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    return pd.DataFrame(columns=["Original", "Selection", "Context", "Notes"])

def save_to_vocab(original, selection, context, notes):
    df = load_vocab()
    new_entry = pd.DataFrame([[original, selection, context, notes]], 
                             columns=["Original", "Selection", "Context", "Notes"])
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)
    return df

# --- THE AI BRAIN (GEMINI 2.5 flash) ---
def get_gemini_response(prompt):
    # UPGRADE: Switched to 'gemini-1.5-pro' for better nuance and reasoning
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(prompt)
    return response.text

# --- UI LAYOUT ---
st.title("🌉 Sheldor's LinguaBridge (Pro Edition)")
st.markdown("Your context-aware communication simulator.")

# Sidebar: Vocabulary Notebook
with st.sidebar:
    st.header("📓 Personal Phrasebook")
    vocab_df = load_vocab()
    if not vocab_df.empty:
        st.dataframe(vocab_df, hide_index=True)
        st.download_button("Download CSV", vocab_df.to_csv(index=False), "my_vocab.csv")
    else:
        st.info("No words saved yet. Start learning!")

# --- MAIN INPUT AREA ---
col1, col2 = st.columns([2, 1])

with col1:
    user_input = st.text_area("Your Input (Chinese or English):", height=150, 
                              placeholder="e.g., 摆烂, or 'I want to ask my prof for more time'")

with col2:
    st.subheader("Scenario Selector")
    # THE UPGRADE: Context is king!
    context = st.radio("Choose your Context:", [
        "🎓 Academic Writing (Formal, Passive, Precise)",
        "📧 Email to Superior (Polite, Clear, Deferential)",
        "💬 Lab Chat / Casual (Idiomatic, Relaxed)",
        "🎤 Presentation Script (Engaging, Spoken Style)"
    ])

# --- THE "TRI-LEVEL" ENGINE ---
if st.button("Generate Options", type="primary"):
    if user_input:
        with st.spinner("Analyzing nuance with Gemini 1.5 Pro..."):
            
            # THE MEGA PROMPT
            prompt = f"""
            Act as an expert Linguist and Communication Coach.
            
            User Input: "{user_input}"
            Selected Context: "{context}"
            
            Task:
            1. Detect language. If Chinese -> Translate to English. If English -> Polish/Upgrade.
            2. Provide 3 distinct options based on the context:
               - Option A: The Safe Choice (Standard, correct, mistake-free).
               - Option B: The Native Choice (Idiomatic, how a native speaker sounds).
               - Option C: The Pro Choice (Sophisticated, impressive vocabulary).
            3. The "Why" Engine: Explain the nuance of each choice briefly.
            
            Output Format (Markdown):
            
            ### 🎯 Analysis
            (Briefly comment on the original input)
            
            ### 1. The Safe Choice 🛡️
            **"..."**
            *Why: ...*
            
            ### 2. The Native Choice 🇺🇸
            **"..."**
            *Why: ...*
            
            ### 3. The Pro Choice 💼
            **"..."**
            *Why: ...*
            
            ### 💡 Key Vocabulary
            (List 1-2 useful words from above with definitions)
            """
            
            # Get response
            result = get_gemini_response(prompt)
            
            # Display Result
            st.markdown("---")
            st.markdown(result)
            
            # Save Feature
            st.markdown("---")
            with st.expander("💾 Save a phrase to your Notebook"):
                col_save_1, col_save_2 = st.columns([3, 1])
                with col_save_1:
                    phrase_to_save = st.text_input("Copy the phrase you liked here:")
                with col_save_2:
                    note_to_save = st.text_input("Add a note (e.g. 'Good for emails')")
                
                if st.button("Save Entry"):
                    save_to_vocab(user_input, phrase_to_save, context, note_to_save)
                    st.success("Saved to sidebar!")
                    st.rerun()
