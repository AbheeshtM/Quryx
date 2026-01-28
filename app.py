import streamlit as st
from groq import Groq

from core.search import search_exam_info
from core.pdf_reader import read_pdf

st.set_page_config(page_title="AI Exam Engine", layout="centered")
st.title("🎓 AI Exam Engine")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

mode = st.radio(
    "Choose Mode",
    ["Exam Topic Mode", "PDF / Notes Mode"]
)

qtype = st.radio(
    "Question Format",
    ["MCQ", "Descriptive / Long Answer"]
)

def generate(prompt):
    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )
    return res.choices[0].message.content


# -------- EXAM TOPIC MODE --------
if mode == "Exam Topic Mode":
    exam = st.text_input("Enter Exam Name (e.g. JEE Main, UPSC, GRE)")
    topic = st.text_input("Enter Topic (e.g. Electrostatics, Polity, Probability)")

    if exam and topic:
        with st.spinner("Searching real exam data..."):
            web_info = search_exam_info(f"{exam} {topic} most asked questions")

        st.subheader("Reference Data")
        st.write(web_info[:1200])

        if st.button("Generate Questions"):
            if qtype == "MCQ":
                prompt = f"""
You are an expert question setter for {exam}.

Topic: {topic}

Using the information below, generate 10 MCQs that are:
- True to the nature of {exam}
- Based on what is commonly asked
- Difficulty split: Easy, Medium, Hard
- Real exam-like

Data:
{web_info}

Format:

Q1: ...
A) ...
B) ...
C) ...
D) ...
Answer: B
Difficulty: Easy
"""
            else:
                prompt = f"""
You are an expert question setter for {exam}.

Topic: {topic}

Using the information below, generate 6 long-answer questions that are:
- Commonly asked in {exam}
- Concept-heavy
- Real exam style
- Mix of medium and hard

Data:
{web_info}

Format:

Q1. (10 marks) Question text
Q2. (15 marks) Question text
...
"""

            st.session_state.paper = generate(prompt)

        if "paper" in st.session_state:
            st.subheader("Generated Paper")
            st.write(st.session_state.paper)

            if st.button("Generate Another Set"):
                del st.session_state["paper"]


# -------- PDF / NOTES MODE --------
if mode == "PDF / Notes Mode":
    exam = st.text_input("Optional Exam Style (e.g. JEE, UPSC, General)")
    pdf = st.file_uploader("Upload Text-based PDF", type=["pdf"])

    if pdf:
        notes = read_pdf(pdf)
        st.write(notes[:1000])

        if st.button("Generate Questions from Notes"):
            if qtype == "MCQ":
                prompt = f"""
Generate 10 MCQs strictly from the notes below.

Style: {exam if exam else "General"}

Notes:
{notes}

Rules:
- Use only given content
- Mix easy, medium, hard

Format:

Q1: ...
A) ...
B) ...
C) ...
D) ...
Answer: B
Difficulty: Medium
"""
            else:
                prompt = f"""
Generate 6 descriptive questions strictly from the notes below.

Style: {exam if exam else "General"}

Notes:
{notes}

Rules:
- Use only given content
- Ask conceptual, long-answer questions

Format:

Q1. (10 marks) Question text
Q2. (15 marks) Question text
...
"""

            st.session_state.paper = generate(prompt)

        if "paper" in st.session_state:
            st.subheader("Generated Paper")
            st.write(st.session_state.paper)

            if st.button("Generate Another Set"):
                del st.session_state["paper"]
