import streamlit as st
import os
import time
from dotenv import load_dotenv
from prompts import get_interview_prompt
from utils.report import generate_report
# Imports for chart modules, assuming they are in the same directory
from donut_chart import create_donut_chart
from bar_chart import create_bar_chart

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
# Session State Initialization
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
if "interview_start_time" not in st.session_state:
    st.session_state.interview_start_time = 0
if "ranking" not in st.session_state:
    st.session_state.ranking = None

# =========================
# Sidebar Settings
# =========================
st.sidebar.title("⚙️ Setup Interview")

use_ai = st.sidebar.toggle("🤖 Use AI-Generated Questions", help="Generates unique questions using AI. Requires a Google AI API key in your .env file.")

custom_set = st.sidebar.selectbox(
    "Custom Question Set",
    ["Standard", "FAANG / MAANG"],
    disabled=use_ai
)

if custom_set == "Standard":
    role = st.sidebar.selectbox("Role", ["Software Engineer", "Product Manager", "Data Analyst"])
    mode = st.sidebar.radio("Mode", ["Technical", "Behavioral"])
else:
    st.sidebar.markdown("---")
    st.sidebar.info(f"Using the **{custom_set}** question set.")
    role = "Software Engineer" # Default for FAANG set
    mode = "Technical" # Default for FAANG set

num_qs = st.sidebar.slider("Number of Questions", 3, 10, 3)

if st.sidebar.button("🚀 Start Interview"):
    spinner_text = "🤖 Generating unique questions..." if use_ai or custom_set == "FAANG / MAANG" else "Preparing your interview..."
    with st.spinner(spinner_text):
        questions, error_message = get_interview_prompt(role, mode, num_qs, custom_set, use_ai)
        if error_message:
            st.warning(error_message) # Use a warning for fallback, error for complete failure
        if not questions:
            st.error("Could not load any questions. Please try again.")
            st.stop()
        st.session_state.questions = questions

    # Reset state for the new interview
    st.session_state.answers = []
    st.session_state.feedback = []
    st.session_state.step = 0
    st.session_state.score = 0
    st.session_state.interview_start_time = time.time()
    st.session_state.ranking = None
    st.rerun()

# =========================
# Main UI Logic
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

# Landing Page
if not st.session_state.questions:
    st.info("Configure your interview settings in the sidebar and click **Start Interview** when ready.")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='card'><div class='card-icon'>🎯</div><b>Role-Specific Questions</b><span>Practice tailored questions for your chosen role.</span></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='card'><div class='card-icon'>🤖</div><b>AI-Powered Feedback</b><span>Get detailed scoring and suggestions.</span></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='card'><div class='card-icon'>📊</div><b>Progress Tracking</b><span>Track your growth with reports.</span></div>", unsafe_allow_html=True)
else:
    step = st.session_state.step
    total_questions = len(st.session_state.questions)

    # Interview Flow
    if step < total_questions:
        elapsed_time = time.time() - st.session_state.get('interview_start_time', time.time())
        
        header_cols = st.columns([3, 1])
        with header_cols[0]:
            st.markdown(f"### Question {step + 1}/{total_questions}")
        with header_cols[1]:
            st.info(f"⏳ {int(elapsed_time // 60):02d}:{int(elapsed_time % 60):02d}")

        q = st.session_state.questions[step]
        st.markdown(f"<div class='card'>{q['q']}</div>", unsafe_allow_html=True)

        choice = st.radio("Choose your answer:", q.get("options", []), index=None, key=f"mcq_{step}")

        # Submit and Skip buttons
        col1, col2 = st.columns([1, 0.1])
        if col1.button("Submit", key=f"submit_{step}"):
            if choice:
                is_correct = choice == q["answer"]
                st.session_state.feedback.append("✅ Correct" if is_correct else f"❌ Incorrect (Correct Answer: {q['answer']})")
                if is_correct:
                    st.session_state.score += 1
                st.session_state.answers.append(choice)
            else:
                st.session_state.answers.append("Not Answered")
                st.session_state.feedback.append("Skipped")
            st.session_state.step += 1
            st.rerun()

        if col2.button("Skip", key=f"skip_{step}"):
            st.session_state.answers.append("Skipped")
            st.session_state.feedback.append("Skipped")
            st.session_state.step += 1
            st.rerun()

    # Summary Report
    else:
        # --- Calculation Block (run once) ---
        if st.session_state.ranking is None:
            end_time = time.time()
            time_taken = end_time - st.session_state.get('interview_start_time', end_time)
            st.session_state.time_taken = time_taken

            def calculate_ranking(score, total_questions, time_taken):
                if total_questions == 0:
                    return "N/A", "Complete an interview to get a rank."

                accuracy = (score / total_questions) * 100
                avg_time_per_q = time_taken / total_questions

                if accuracy >= 95 and avg_time_per_q < 30:
                    return "S-Tier (Godlike)", "Flawless accuracy and lightning-fast responses. Truly top-tier performance."
                elif accuracy >= 80 and avg_time_per_q < 60:
                    return "A-Tier (Expert)", "High accuracy and great speed. You're well-prepared for technical challenges."
                elif accuracy >= 60:
                    return "B-Tier (Proficient)", "Good accuracy. Focus on increasing your response speed and deepening your knowledge."
                elif accuracy >= 40:
                    return "C-Tier (Competent)", "You have a foundational understanding. Consistent practice will improve your accuracy."
                else:
                    return "D-Tier (Beginner)", "A good first step. Focus on reviewing fundamentals and trying again."

            rank, desc = calculate_ranking(st.session_state.score, total_questions, st.session_state.time_taken)
            st.session_state.ranking = rank
            st.session_state.ranking_description = desc


        st.success("✅ Interview Complete!")
        st.subheader("📊 Summary Report")

        # --- Metrics Row ---
        m1, m2, m3 = st.columns(3)
        accuracy_percent = (st.session_state.score / total_questions) * 100 if total_questions > 0 else 0
        m1.metric("Final Score", f"{st.session_state.score}/{total_questions}", f"{accuracy_percent:.2f}%")
        m2.metric("Total Time", f"{st.session_state.time_taken:.2f}s")
        m3.metric("Your Rank", st.session_state.ranking)
        st.markdown(f"> *{st.session_state.ranking_description}*")
        
        with st.expander("How are rankings calculated?"):
            st.markdown("""
            - **S-Tier (Godlike):** >95% accuracy & <30s per question.
            - **A-Tier (Expert):** >80% accuracy & <60s per question.
            - **B-Tier (Proficient):** >60% accuracy.
            - **C-Tier (Competent):** >40% accuracy.
            - **D-Tier (Beginner):** <=40% accuracy.
            """)
        st.write("---")


        # --- Charts Row ---
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<h5>Overall Performance</h5>", unsafe_allow_html=True)
            donut_fig = create_donut_chart(st.session_state.score, total_questions)
            st.plotly_chart(donut_fig, use_container_width=True)

        with col2:
            st.markdown("<h5>Question Breakdown</h5>", unsafe_allow_html=True)
            
            # Added debug line as requested
            st.write(f"DEBUG: Feedback content is {st.session_state.feedback}") 

            bar_fig = create_bar_chart(st.session_state.feedback)
            st.plotly_chart(bar_fig, use_container_width=True)
        
        st.write("---")
        st.subheader("💡 Detailed Feedback")
        for i, (q, ans, fb) in enumerate(zip(st.session_state.questions, st.session_state.answers, st.session_state.feedback)):
            with st.expander(f"**Q{i+1}: {q['q']}**"):
                st.write(f"📝 **Your Answer:** {ans}")
                st.write(f"💬 **Feedback:** {fb}")

        # PDF Report Download
        pdf_path = generate_report(
            [q['q'] for q in st.session_state.questions],
            st.session_state.answers,
            [{"feedback": fb, "score": (1 if '✅ Correct' in fb else 0)} for fb in st.session_state.feedback]
        )
        with open(pdf_path, "rb") as pdf_file:
            st.download_button(
                label="📥 Download PDF Report",
                data=pdf_file,
                file_name="interview_report.pdf",
                mime="application/octet-stream"
            )

