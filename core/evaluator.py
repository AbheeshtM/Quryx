def evaluate(user_answers, correct_answers):
    score = 0
    for k in correct_answers:
        if user_answers.get(k) == correct_answers[k]:
            score += 1
    return score, len(correct_answers)
