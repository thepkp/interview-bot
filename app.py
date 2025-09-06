import streamlit as st
from openai import OpenAI # <-- 1. IMPORT CHANGE: Import the OpenAI class
import os
from dotenv import load_dotenv
from prompts import get_interview_prompt
#from utils.feedback import evaluate_answer
#from utils.report import generate_report

# Load environment variables
load_dotenv()

# --- 2. INITIALIZE CLIENT ---
# The client automatically finds the OPENAI_API_KEY in your .env file
client = OpenAI()

st.set_page_config(page_title="Interview Preparation Bot", layout="wide")

# --- Session State ---
if "questions" not in st.session_state:
    st.session_state.questions = []
if "answers" not in st.session_state:
    st.session_state.answers = []
if "feedback" not in st.session_state:
    st.session_state.feedback = []
if "step" not in st.session_state:
    st.session_state.step = 0

# --- Sidebar: Role & Mode Selection ---
st.sidebar.title("⚙️ Interview Settings")
role = st.sidebar.selectbox("Select Role", ["Software Engineer", "Product Manager", "Data Analyst"])
mode = st.sidebar.radio("Interview Mode", ["Technical", "Behavioral"])
num_qs = st.sidebar.slider("Number of Questions", 3, 5, 3)

# --- Generate Questions ---
if st.sidebar.button("Start Interview"):
    st.session_state.questions = get_interview_prompt(role, mode, num_qs)
    st.session_state.answers = []
    st.session_state.feedback = []
    st.session_state.step = 0
    st.rerun()

st.title("🧑‍💻 Interview Preparation Bot")
st.write(f"**Role:** {role} | **Mode:** {mode}")

def evaluate_answer(question, answer, mode):
    """
    Uses LLM to evaluate user answer. 
    Returns (feedback, score).
    """
    if not answer.strip():
        return "No answer provided.", 0

    prompt = f"""
    You are an interviewer evaluating an answer.
    Question: {question}
    Candidate's Answer: {answer}
    Mode: {mode}

    Give concise feedback (2-3 sentences) and score out of 10.
    Format: 
    Feedback: <text>
    Score: <number>
    """ # <-- This was missing. It closes the multi-line string.

    try:
        # --- 3. API CALL CHANGE ---
        # The API call now uses the client instance
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", # Change to "gpt-4" if available
            messages=[{"role": "user", "content": prompt}]
        )
        # --- 4. RESPONSE PARSING CHANGE ---
        # The response is now an object, not a dictionary
        text = response.choices[0].message.content

        # Simple parsing (customize if needed)
        feedback = text.split("Score:")[0].replace("Feedback:", "").strip()
        try:
            score = int(text.split("Score:")[-1].strip())
        except:
            score = 5
        return feedback, score

    except Exception as e:
        return f"Error: {str(e)}", 0

# --- Interview Flow ---
if st.session_state.questions:
    step = st.session_state.step

    if step < len(st.session_state.questions):
        q = st.session_state.questions[step]
        st.subheader(f"Question {step+1}: {q}")

        user_answer = st.text_area("Your Answer", key=f"ans_{step}")

        col1, col2 = st.columns(2)
        if col1.button("Submit Answer", key=f"submit_{step}"):
            feedback, score = evaluate_answer(q, user_answer, mode)
            st.session_state.answers.append(user_answer)
            st.session_state.feedback.append({"feedback": feedback, "score": score})
            st.session_state.step += 1
            st.rerun()

        if col2.button("Skip", key=f"skip_{step}"):
            st.session_state.answers.append("Skipped")
            st.session_state.feedback.append({"feedback": "Skipped", "score": 0})
            st.session_state.step += 1
            st.rerun()

    else:
        st.success("✅ Interview Complete!")
        st.subheader("📊 Summary Report")

        for i, (q, ans, fb) in enumerate(zip(st.session_state.questions, st.session_state.answers, st.session_state.feedback)):
            st.markdown(f"**Q{i+1}: {q}**")
            st.write(f"📝 Your Answer: {ans}")
            st.write(f"💡 Feedback: {fb['feedback']}")
            st.write(f"⭐ Score: {fb['score']}/10")
            st.write("---")

        if st.button("Download PDF Report"):
            pdf_path = generate_report(st.session_state.questions, st.session_state.answers, st.session_state.feedback)
            with open(pdf_path, "rb") as pdf_file:
                st.download_button("📥 Download Report", data=pdf_file, file_name="interview_report.pdf")


