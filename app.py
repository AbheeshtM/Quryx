import streamlit as st
from groq import Groq

from core.search import search_exam_info
from core.pdf_reader import read_pdf
from core.question_gen import build_mcq_prompt

st.set_page_config(page_title="AI Exam Engine", layout="centered")
st.title("🎓 AI Exam Engine")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

mode = st.radio(
    "Choose Mode",
    ["Exam Topic Mode", "PDF / Notes Mode"]
)

def generate(prompt):
    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )
    return res.choices[0].message.content


# ================= EXAM TOPIC MODE =================
if mode == "Exam Topic Mode":
    exam = st.text_input("Enter Exam Name (e.g. JEE Main, UPSC, GRE)")
    topic = st.text_input("Enter Topic (e.g. Electrostatics, Polity)")

    if exam and topic:
        with st.spinner("Fetching exam style..."):
            web_info = search_exam_info(f"{exam} {topic} questions")

        if st.button("Generate Questions"):
            prompt = build_mcq_prompt(exam, topic, web_info)
            st.session_state.paper = generate(prompt)
            st.session_state.copied_question = ""

    if "paper" in st.session_state:
        st.subheader("📄 Generated Questions")

        raw = st.session_state.paper
        questions = raw.split("\n\nQ")
        questions = ["Q" + q.strip() for q in questions if q.strip()]

        for i, q in enumerate(questions):
            st.markdown(f"### Question {i+1}")
            st.code(q)

            st.button(
                "📋 Copy Question",
                key=f"copy_exam_{i}",
                on_click=lambda q=q: st.session_state.update(
                    {"copied_question": q}
                )
            )


# ================= PDF / NOTES MODE =================
if mode == "PDF / Notes Mode":
    exam = st.text_input("Optional Exam Style (e.g. JEE, UPSC, General)")
    topic = st.text_input("Topic from Notes")
    pdf = st.file_uploader("Upload Text-based PDF", type=["pdf"])

    if pdf and topic:
        notes = read_pdf(pdf)
        st.write(notes[:800])

        if st.button("Generate Questions from Notes"):
            prompt = f"""
You are an expert exam question setter.

Topic: {topic}
Exam style: {exam}

STRICT RULES:
- DO NOT provide correct answers
- DO NOT provide explanations
- Some questions MAY have multiple correct options
- Use ONLY the content below

CONTENT:
{notes}

Generate exactly 10 MCQs.

FORMAT:

Q1: ...
A) ...
B) ...
C) ...
D) ...
"""
            st.session_state.paper = generate(prompt)
            st.session_state.copied_question = ""

    if "paper" in st.session_state:
        st.subheader("📄 Generated Questions")

        raw = st.session_state.paper
        questions = raw.split("\n\nQ")
        questions = ["Q" + q.strip() for q in questions if q.strip()]

        for i, q in enumerate(questions):
            st.markdown(f"### Question {i+1}")
            st.code(q)

            st.button(
                "📋 Copy Question",
                key=f"copy_pdf_{i}",
                on_click=lambda q=q: st.session_state.update(
                    {"copied_question": q}
                )
            )


# ================= SOLVER / CHAT =================
st.divider()
st.subheader("🔍 Solve / Search Question")

query = st.text_area(
    "Copied question will appear here",
    value=st.session_state.get("copied_question", ""),
    height=200
)

if st.button("Ask AI to Solve"):
    if query.strip():
        with st.spinner("Solving..."):
            solution = generate(
                f"Solve this question step by step:\n\n{query}"
            )
            st.write(solution)
    else:
        st.warning("Please copy or paste a question first.")
