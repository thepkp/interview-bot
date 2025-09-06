def get_interview_prompt(role, mode, num_qs=3):
    """
    Returns dummy questions (replace with LLM API call later).
    """
    if mode == "Technical":
        sample_qs = [
            f"What is time complexity of binary search in {role} role?",
            f"Explain OOPs concepts with examples relevant to {role}.",
            f"How would you design a scalable login system?"
        ]
    else:
        sample_qs = [
            "Tell me about a time you resolved a conflict in your team.",
            "Describe a challenging project you led and its outcome.",
            "How do you handle feedback and criticism?"
        ]
    return sample_qs[:num_qs]
