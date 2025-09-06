import openai

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
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Change to "gpt-4" if available
            messages=[{"role": "user", "content": prompt}]
        )
        text = response["choices"][0]["message"]["content"]

        # Simple parsing (customize if needed)
        feedback = text.split("Score:")[0].replace("Feedback:", "").strip()
        try:
            score = int(text.split("Score:")[-1].strip())
        except:
            score = 5
        return feedback, score

    except Exception as e:
        return f"Error: {str(e)}", 0
