import random
import os
import json
import google.generativeai as genai

# Configure the generative AI model
try:
    # Using a known valid and recent model name
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e:
    model = None
    print(f"Error configuring Generative AI: {e}")

# This is the original, hardcoded database of questions.
# It will be used as a fallback if the AI fails or is not selected.
questions_db = {
    "Custom Sets": {
        "FAANG / MAANG": [
            {"q": "Given an array of integers, find the two numbers that add up to a specific target.", "options": ["Brute-force (O(n^2))", "Hash Map (O(n))", "Sort and two-pointers (O(n log n))", "All of the above are possible solutions"], "answer": "All of the above are possible solutions"},
            {"q": "How would you design a URL shortening service like TinyURL?", "options": ["Using a hash function", "Using a simple counter", "Using a combination of a counter and base62 encoding", "Using a random string generator"], "answer": "Using a combination of a counter and base62 encoding"},
        ]
    },
    "Software Engineer": {
        "Technical": [
            {"q": "What is the difference between a list and a tuple in Python?", "options": ["Lists are mutable, tuples are not", "Tuples are mutable, lists are not", "They are the same", "Lists can only store integers"], "answer": "Lists are mutable, tuples are not"},
            {"q": "Explain the concept of 'Big O notation'.", "options": ["A way to measure algorithm efficiency", "A type of data structure", "A sorting algorithm", "A programming language"], "answer": "A way to measure algorithm efficiency"},
        ],
        "Behavioral": [
             {"q": "Tell me about a time you had a conflict with a coworker and how you resolved it.", "options": ["Ignored the conflict", "Discussed it openly with the coworker to find a solution", "Reported it to HR immediately", "Asked to be moved to another team"], "answer": "Discussed it openly with the coworker to find a solution"},
        ]
    },
    "Product Manager": {
        "Behavioral": [
             {"q": "How would you prioritize features for a new product?", "options": ["Based on what the CEO likes", "Using a framework like RICE or MoSCoW", "Building the easiest features first", "Based on what competitors have"], "answer": "Using a framework like RICE or MoSCoW"},
        ]
    },
     "Data Analyst": {
         "Technical": [
             {"q": "What is the difference between SQL and NoSQL databases?", "options": ["SQL is for structured data, NoSQL is for unstructured data", "NoSQL is older than SQL", "SQL is only used for web apps", "There is no difference"], "answer": "SQL is for structured data, NoSQL is for unstructured data"},
         ]
     }
}


def get_ai_interview_questions(role, mode, num_qs, custom_set):
    """
    Generates interview questions using the Gemini AI model.
    """
    if not model:
        return None, "Generative AI model is not configured. Please check your API key in the Streamlit secrets."

    company_context = f"for a top tech company like those in FAANG / MAANG" if custom_set == "FAANG / MAANG" else ""
    
    # Updated prompt to explicitly ask for JSON output and nothing else.
    prompt = f"""
    You are an expert interviewer. Generate {num_qs} high-quality, {mode} interview questions for a {role} position {company_context}.
    Your response MUST be a valid JSON array of objects, and nothing else. Do not include any text, notes, or markdown before or after the JSON.
    
    Each object in the array must have these three keys:
    1. "q": A string containing the question text.
    2. "options": An array of exactly 4 strings for multiple-choice options.
    3. "answer": A string containing the correct answer, which must exactly match one of the strings in the "options" array.
    """

    try:
        # Simplified the generation call for more reliability
        response = model.generate_content(prompt)
        
        # Clean the response text in case the model adds markdown formatting
        json_text = response.text.strip().replace("```json", "").replace("```", "")
        generated_questions = json.loads(json_text)
        
        if not isinstance(generated_questions, list):
             raise ValueError("AI did not return a list of questions as expected.")

        return generated_questions, None
    except (json.JSONDecodeError, ValueError) as e:
        error_msg = f"Failed to parse the AI's response. Error: {e}"
        print(error_msg)
        print("--- Raw AI Response ---")
        print(response.text)
        print("-----------------------")
        return None, error_msg
    except Exception as e:
        error_msg = f"An unexpected error occurred during AI generation: {e}"
        print(error_msg)
        return None, error_msg


def get_interview_prompt(role, mode, num_qs, custom_set="Standard", use_ai=False):
    """
    Main function to get questions. It can use AI or the preset database.
    Returns a tuple: (questions_list, error_message)
    """
    if use_ai:
        questions, error = get_ai_interview_questions(role, mode, num_qs, custom_set)
        if questions:
            return questions, None
        else:
            # Fallback to standard questions if AI fails
            standard_questions, _ = get_interview_prompt(role, mode, num_qs, custom_set, use_ai=False)
            error_message = f"{error}. Falling back to standard questions."
            return standard_questions, error_message

    # --- Logic for preset questions ---
    if custom_set != "Standard":
        selected_questions_pool = questions_db.get("Custom Sets", {}).get(custom_set, [])
    else:
        selected_questions_pool = questions_db.get(role, {}).get(mode, [])

    if not selected_questions_pool:
        return [{"q": "No questions found for this selection.", "options": [], "answer": ""}], None

    if len(selected_questions_pool) < num_qs:
        random.shuffle(selected_questions_pool)
        return selected_questions_pool, None

    return random.sample(selected_questions_pool, k=num_qs), None

