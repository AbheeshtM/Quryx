def build_mcq_prompt(exam, topic, context):
    return f"""
You are an expert exam question setter.

Exam style: {exam}
Topic: {topic}

STRICT RULES:
- DO NOT provide correct answers
- DO NOT provide explanations
- Some questions MAY have multiple correct options
- Questions must be real exam-style
- Output must be clean and searchable

Use the reference below ONLY for style and difficulty:

{context}

Generate exactly 10 MCQs.

FORMAT (follow exactly):

Q1: ...
A) ...
B) ...
C) ...
D) ...
"""
