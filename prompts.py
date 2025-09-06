def get_interview_prompt(role, mode, num_qs=3):
    """
    Returns dummy questions (replace with LLM API call later).
    """
    if mode == "Technical":
        sample_qs = [
            f"What is the time complexity of binary search in {role} role?",
            f"Explain OOPs concepts with examples relevant to {role}.",
            f"How would you design a scalable login system?",
            f"What are the differences between REST and GraphQL APIs, and when would you use each in {role}?",
            f"Explain database normalization and why it’s important.",
            f"How would you optimize a slow SQL query?",
            f"Describe how caching improves performance in large-scale systems.",
            f"What are design patterns? Give an example you might use in {role}.",
            f"How does garbage collection work in languages like Java/Python?",
            f"Explain the differences between concurrency and parallelism with an example."
        ]
    else:
        sample_qs = [
            "Tell me about a time you resolved a conflict in your team.",
            "Describe a challenging project you led and its outcome.",
            "How do you handle feedback and criticism?",
            "Give an example of when you had to quickly adapt to change.",
            "Tell me about a failure and what you learned from it.",
            "How do you manage deadlines when working under pressure?",
            "Describe a time when you went above and beyond your responsibilities.",
            "What motivates you to perform at your best?",
            "How do you handle disagreements with your manager or mentor?",
            "Give an example of when you had to work with a difficult teammate."
        ]
    return sample_qs[:num_qs]
