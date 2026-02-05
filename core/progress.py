import json
from datetime import datetime

PATH = "data/progress.json"

def save_result(exam, score, total):
    try:
        with open(PATH, "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append({
        "exam": exam,
        "score": score,
        "total": total,
        "time": datetime.now().isoformat()
    })

    with open(PATH, "w") as f:
        json.dump(data, f, indent=2)
