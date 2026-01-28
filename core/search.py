from ddgs import DDGS

def search_exam_info(exam_name):
    texts = []
    queries = [
        f"{exam_name} latest syllabus",
        f"{exam_name} exam pattern",
        f"{exam_name} sample question paper",
    ]

    with DDGS() as ddgs:
        for q in queries:
            for r in ddgs.text(q, max_results=2):
                if "body" in r:
                    texts.append(r["body"])

    return "\n".join(texts)
