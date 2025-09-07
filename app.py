import streamlit as st
import os
from dotenv import load_dotenv
from prompts import get_interview_prompt
from utils.report import generate_report
from utils.charts import create_donut_chart, create_bar_chart

# =========================
# Load environment variables
# =========================
load_dotenv()

st.set_page_config(page_title="Interview Preparation Bot", layout="wide")

# =========================
# Custom CSS (Dark Theme, Modern UI)
# =========================
st.markdown("""
<style>
:root {
  --bg: #0f172a; 
  --card: #1e293b;
  --text: #f1f5f9;
  --muted: #94a3b8;
  --accent: #3b82f6;
}
.stApp {
  background: var(--bg);
  color: var(--text);
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}
h1, h2, h3 {
  font-weight: 600;
  letter-spacing: -0.02em;
}
.stSidebar {
  background: #111827 !important;
  color: var(--text);
}
.stButton > button {
  border-radius: 8px;
  padding: 0.6rem 1rem;
  background: var(--accent);
  color: white;
  font-weight: 500;
  transition: all 0.2s ease;
}
.stButton > button:hover {
  background: #2563eb;
}
.card {
  background: var(--card);
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 16px;
  text-align: center;
  box-shadow: 0px 6px 18px rgba(0,0,0,0.35);
  transition: transform 0.2s ease;
}
.card:hover {
  transform: translateY(-3px);
}
.card-icon {
  font-size: 30px;
  margin-bottom: 10px;
  color: var(--accent);
}
</style>
""", unsafe_allow_html=True)

# =========================
# Session State
# =========================
if "questions" not in st.session_state:
    st.session_state.questions = []
if "answers" not in st.session_state:
    st.session_state.answers = []
if "feedback" not in st.session_state:
    st.session_state.feedback = []
if "step" not in st.session_state:
    st.session_state.step = 0
if "score" not in st.session_state:
    st.session_state.score = 0

# =========================
# Sidebar Settings
# =========================
st.sidebar.title("⚙️ Setup Interview")
role = st.sidebar.selectbox("Role", ["Software Engineer", "Product Manager", "Data Analyst"])
mode = st.sidebar.radio("Mode", ["Technical", "Behavioral"])
num_qs = st.sidebar.slider("Number of Questions", 3, 10, 3)

if st.sidebar.button("🚀 Start Interview"):
    st.session_state.questions = get_interview_prompt(role, mode, num_qs)
    st.session_state.answers = []
    st.session_state.feedback = []
    st.session_state.step = 0
    st.session_state.score = 0
    st.rerun()

# =========================
# Main UI (Landing + Interview Flow)
# =========================
st.title("Interview Preparation Bot")
st.markdown(
    "<p style='color:var(--muted); font-size:16px;'>"
    "Practice your interview skills with AI-powered feedback. "
    "Select your role, choose between technical or behavioral questions, "
    "and get detailed feedback to improve performance."
    "</p>", 
    unsafe_allow_html=True
)

if not st.session_state.questions:
    # Landing Page with Feature Cards
    st.info("Configure your interview settings in the sidebar and click **Start Interview** when ready.")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='card'><div class='card-icon'>🎯</div><b>Role-Specific Questions</b><br><span>Practice tailored questions for your chosen role.</span></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='card'><div class='card-icon'>🤖</div><b>AI-Powered Feedback</b><br><span>Get detailed scoring and suggestions.</span></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='card'><div class='card-icon'>📊</div><b>Progress Tracking</b><br><span>Track your growth with reports.</span></div>", unsafe_allow_html=True)

else:
    # === Interview Flow ===
    step = st.session_state.step
    if step < len(st.session_state.questions):
        q = st.session_state.questions[step]
        st.markdown(f"<div class='card'><b>Q{step+1}: {q['q']}</b></div>", unsafe_allow_html=True)

        choice = st.radio("Choose your answer:", q["options"], index=None, key=f"mcq_{step}")

        col1, col2 = st.columns(2)
        if col1.button("Submit", key=f"submit_{step}"):
            if choice:
                if choice == q["answer"]:
                    st.session_state.feedback.append("✅ Correct")
                    st.session_state.score += 1
                else:
                    st.session_state.feedback.append(f"❌ Incorrect (Answer: {q['answer']})")
                st.session_state.answers.append(choice)
            else:
                st.session_state.answers.append("Skipped")
                st.session_state.feedback.append("Skipped")
            st.session_state.step += 1
            st.rerun()

        if col2.button("Skip", key=f"skip_{step}"):
            st.session_state.answers.append("Skipped")
            st.session_state.feedback.append("Skipped")
            st.session_state.step += 1
            st.rerun()

    else:
          # === Summary Report ==
          # === Summary Report ===
            st.success("✅ Interview Complete!")
            st.subheader("📊 Summary Report")
            
            # --- Visualizations ---
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("<h5>Overall Performance</h5>", unsafe_allow_html=True)
                donut_fig = create_donut_chart(st.session_state.score, len(st.session_state.questions))
                st.plotly_chart(donut_fig, use_container_width=True)
            
            with col2:
                st.markdown("<h5>Question Breakdown</h5>", unsafe_allow_html=True)
                bar_fig = create_bar_chart(st.session_state.feedback)
                st.plotly_chart(bar_fig, use_container_width=True)
            
            st.info(f"🎯 Final Score: {st.session_state.score}/{len(st.session_state.questions)}")
            st.write("---")
            
            # --- Detailed Feedback ---
            st.subheader("💡 Detailed Feedback")
            for i, (q, ans, fb) in enumerate(zip(st.session_state.questions, st.session_state.answers, st.session_state.feedback)):
                with st.expander(f"**Q{i+1}: {q['q']}**"):
                    st.write(f"📝 **Your Answer:** {ans}")
                    st.write(f"💬 **Feedback:** {fb}")
            
            
            if st.button("Download PDF Report"):
                pdf_path = generate_report(
                    [q['q'] for q in st.session_state.questions],
                    st.session_state.answers,
                    [{"feedback": fb, "score": (1 if 'Correct' in fb else 0)} for fb in st.session_state.feedback]
                )
                with open(pdf_path, "rb") as pdf_file:
                    st.download_button("📥 Download Report", data=pdf_file, file_name="interview_report.pdf")
