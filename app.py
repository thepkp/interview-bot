import streamlit as st
import os
from dotenv import load_dotenv
from prompts import get_interview_prompt
from utils.report import generate_report
from utils.charts import create_donut_chart, create_bar_chart
# --- NEW: Import Firestore utilities ---
from utils.firestore_utils import init_firestore, save_score, get_leaderboard

# =========================
# Load environment variables & Initialize DB
# =========================
load_dotenv()
# --- NEW: Initialize Firestore ---
db = init_firestore()

st.set_page_config(page_title="Interview Preparation Bot", layout="wide")

# =========================
# Custom CSS
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
    text-align: center;
}
.card b {
    display: block;
    text-align: center;
}
.card span {
     display: block;
    text-align: center;
    color: var(--muted);
}
</style>
""", unsafe_allow_html=True)


# =========================
# Session State
# =========================
# --- NEW: Add user details to session state ---
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "user_email" not in st.session_state:
    st.session_state.user_email = ""

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

# --- NEW: Add personal details input ---
st.sidebar.header("Your Details")
name = st.sidebar.text_input("👤 Your Name", key="user_name")
email = st.sidebar.text_input("✉️ Your Email", key="user_email")
st.sidebar.markdown("---")

st.sidebar.header("Interview Settings")
use_ai = st.sidebar.toggle("🤖 Use AI-Generated Questions", help="Generates unique questions using AI.")
custom_set = st.sidebar.selectbox("Custom Question Set", ["Standard", "FAANG / MAANG"], disabled=use_ai)

if custom_set == "Standard":
    role = st.sidebar.selectbox("Role", ["Software Engineer", "Product Manager", "Data Analyst"])
    mode = st.sidebar.radio("Mode", ["Technical", "Behavioral"])
else:
    st.sidebar.info(f"Using the **{custom_set}** question set.")
    role = "Software Engineer"
    mode = "Technical"

num_qs = st.sidebar.slider("Number of Questions", 3, 10, 3)

if st.sidebar.button("🚀 Start Interview"):
    # --- NEW: Validate user details ---
    if not name or not email:
        st.sidebar.error("Please enter your name and email to start.")
    else:
        spinner_text = "🤖 Generating unique questions..." if use_ai else "Preparing your interview..."
        with st.spinner(spinner_text):
            questions, error_message = get_interview_prompt(role, mode, num_qs, custom_set, use_ai)
            if error_message:
                st.error(error_message)
            st.session_state.questions = questions

        st.session_state.answers = []
        st.session_state.feedback = []
        st.session_state.step = 0
        st.session_state.score = 0
        st.rerun()

# =========================
# Main UI
# =========================
st.title("Interview Preparation Bot")
st.markdown("<p style='color:var(--muted); font-size:16px;'>Practice your interview skills with AI-powered feedback.</p>", unsafe_allow_html=True)

if not st.session_state.questions:
    # --- NEW: Display Leaderboard on landing page ---
    st.subheader("🏆 Leaderboard")
    if db:
        role_filter = st.selectbox("Filter by Role", ["All", "Software Engineer", "Product Manager", "Data Analyst"])
        leaderboard_df = get_leaderboard(db, role_filter)
        if not leaderboard_df.empty:
            st.dataframe(leaderboard_df, use_container_width=True, hide_index=True)
        else:
            st.info("No scores yet. Be the first to take an interview!")
    else:
        st.warning("Leaderboard is unavailable as the database connection failed.")
    st.markdown("---")


    st.info("Configure your interview settings in the sidebar and click **Start Interview** when ready.")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='card'><div class='card-icon'>🎯</div><b>Role-Specific Questions</b><span>Practice tailored questions for your chosen role.</span></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='card'><div class='card-icon'>🤖</div><b>AI-Powered Feedback</b><span>Get detailed scoring and suggestions.</span></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='card'><div class='card-icon'>📊</div><b>Progress Tracking</b><span>Track your growth with reports.</span></div>", unsafe_allow_html=True)

else:
    # === Interview Flow ===
    step = st.session_state.step
    if step < len(st.session_state.questions):
        q = st.session_state.questions[step]
        st.markdown(f"<div class='card'><b>Q{step+1}: {q['q']}</b></div>", unsafe_allow_html=True)
        choice = st.radio("Choose your answer:", q.get("options", []), index=None, key=f"mcq_{step}")
        col1, col2 = st.columns([1, 0.1])
        if col1.button("Submit", key=f"submit_{step}"):
            if choice:
                is_correct = choice == q["answer"]
                st.session_state.feedback.append("✅ Correct" if is_correct else f"❌ Incorrect (Answer: {q['answer']})")
                if is_correct:
                    st.session_state.score += 1
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
        # === Summary Report ===
        st.success("✅ Interview Complete!")
        
        # --- NEW: Save score to leaderboard ---
        if db:
            save_score(db, st.session_state.user_name, st.session_state.user_email, st.session_state.score, len(st.session_state.questions), role)
            st.toast("🏆 Your score has been saved to the leaderboard!")

        st.subheader("📊 Summary Report")
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

