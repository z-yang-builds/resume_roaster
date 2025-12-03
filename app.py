import streamlit as st
from openai import OpenAI
import os

# Page Config
st.set_page_config(page_title="Resume Roaster", layout="wide")

st.title("🔥 Resume Roaster")
st.markdown("### Ruthless critique from a cynical Google Recruiter.")

# 1. Try to get Key from Environment Variable (for your local terminal setup)
api_key = os.getenv("OPENAI_API_KEY")

# 2. Fallback: Ask for Key in Sidebar if not found
if not api_key:
    api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")

if not api_key:
    st.info("👈 Please enter your OpenAI API Key in the sidebar to continue.")
    st.stop()

# Initialize Client
client = OpenAI(api_key=api_key)

# Layout: Two columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("Your Resume")
    resume_text = st.text_area("Paste your resume text here...", height=400)

with col2:
    st.subheader("Job Description (Optional)")
    job_description = st.text_area("Paste the JD here (for context)...", height=400)

# Button
if st.button("Roast My Resume 🚀", type="primary"):
    if not resume_text:
        st.error("Please paste your resume text first!")
    else:
        with st.spinner("Summoning the mean recruiter..."):
            # The "Deep Dive" System Prompt
            system_prompt = """
            You are an expert Executive Recruiter for top-tier Tech companies (Google, Meta, OpenAI). 
            Your goal is not just to roast, but to providing a deep, structural, and line-by-line critique to transform a good resume into a top 1% resume.

            CRITICAL RULES:
            1.  **Do NOT use flowery language.** Do not suggest words like "visionary," "cutting-edge," or "synergy." If the user uses them, scream at them.
            2.  **Focus on "So What?":** Every bullet point must have a metric OR a clear business outcome. 
            3.  **Be lengthy and detailed.** Do not give short generic advice. Analyze specific bullet points deeply.

            Output Structure:
            
            ### 💀 The Brutal Reality Check (The Roast)
            (Give a harsh, 3-4 sentence summary of why this resume gets rejected in 6 seconds. Be specific about the vibe.)

            ### 📉 Score Card
            - **Impact Quantification:** X/10
            - **Action Verbs Strength:** X/10
            - **ATS Readability:** X/10
            - **Fluff Factor:** X/10 (High is bad)

            ### 🔍 Section-by-Section Deep Dive

            #### Professional Experience
            (Iterate through key bullet points. For each weak point:)
            * **Original:** "[Quote the user's text]"
            * **Critique:** (Why is this weak? Is it the metric? The verb? The context?)
            * **The 10x Rewrite:** (Rewrite it using the X-Y-Z formula: Accomplished [X] as measured by [Y], by doing [Z]. Make it punchy and number-heavy.)

            ### 🚩 Red Flags & Buzzwords to Kill
            (List specific words in the resume that make the candidate look junior or naive.)

            ### 💡 Final Strategy for PM/AI Roles
            (Based on the content, give 3 specific strategic moves to position this candidate better for Product Management in AI.)
            """
            
            try:
                # Call OpenAI
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Resume Content:\n{resume_text}\n\nJob Description:\n{job_description}"}
                    ]
                )
                
                # Display Result
                st.success("Roast Complete! Brace yourself:")
                st.markdown("---")
                st.markdown(response.choices[0].message.content)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
