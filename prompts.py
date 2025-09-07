import random

def get_interview_prompt(role, mode, num_qs):
    """
    Generates a list of interview questions based on role, mode, and number.
    It shuffles and selects a random sample of questions from the database.
    """
    # Expanded questions database for better shuffling
    questions_db = {
        "Software Engineer": {
            "Technical": [
                {"q": "What is the difference between a list and a tuple in Python?", "options": ["Lists are mutable, tuples are not", "Tuples are mutable, lists are not", "They are the same", "Lists can only store integers"], "answer": "Lists are mutable, tuples are not"},
                {"q": "Explain the concept of 'Big O notation'.", "options": ["A way to measure algorithm efficiency", "A type of data structure", "A sorting algorithm", "A programming language"], "answer": "A way to measure algorithm efficiency"},
                {"q": "What is a REST API?", "options": ["A database management system", "A programming paradigm", "An architectural style for networked applications", "A frontend framework"], "answer": "An architectural style for networked applications"},
                {"q": "What is the purpose of a 'finally' block in a try-except statement?", "options": ["To catch all exceptions", "To execute code regardless of whether an exception was raised", "To handle specific errors", "To raise a new exception"], "answer": "To execute code regardless of whether an exception was raised"},
                {"q": "Describe the difference between '==' and 'is' in Python.", "options": ["'==' checks for value equality, 'is' checks for object identity", "'is' checks for value equality, '==' checks for object identity", "They are identical", "Only '==' can be used for custom objects"], "answer": "'==' checks for value equality, 'is' checks for object identity"},
                {"q": "What is Docker and why is it useful?", "options": ["A version control system", "A cloud provider", "A containerization platform", "A database service"], "answer": "A containerization platform"},
            ],
            "Behavioral": [
                 {"q": "Tell me about a time you had a conflict with a coworker and how you resolved it.", "options": ["Ignored the conflict", "Discussed it openly with the coworker to find a solution", "Reported it to HR immediately", "Asked to be moved to another team"], "answer": "Discussed it openly with the coworker to find a solution"},
                 {"q": "How do you handle tight deadlines?", "options": ["Work overtime exclusively", "Prioritize tasks and communicate potential delays", "Ask for an extension immediately", "Delegate all the work to others"], "answer": "Prioritize tasks and communicate potential delays"},
                 {"q": "Describe a project you are particularly proud of. What was your role?", "options": ["Took all the credit", "Explained my specific contributions and the team's success", "Downplayed my role", "Focused only on the failures"], "answer": "Explained my specific contributions and the team's success"},
            ]
        },
        "Product Manager": {
             "Technical": [
                 {"q": "What is A/B testing?", "options": ["A method to compare two versions of a product to see which performs better", "A type of security test", "A database query language", "A project management methodology"], "answer": "A method to compare two versions of a product to see which performs better"},
                 {"q": "What are KPIs?", "options": ["Key Performance Indicators", "Key Programming Interfaces", "Known Project Issues", "Knowledge Process Integration"], "answer": "Key Performance Indicators"},
             ],
            "Behavioral": [
                 {"q": "How would you prioritize features for a new product?", "options": ["Based on what the CEO likes", "Using a framework like RICE or MoSCoW", "Building the easiest features first", "Based on what competitors have"], "answer": "Using a framework like RICE or MoSCoW"},
                 {"q": "How do you say 'no' to a stakeholder's request?", "options": ["Agree to do it but never deliver", "Say 'no' and provide data-driven reasons and alternative solutions", "Say 'yes' to everything", "Ignore the request"], "answer": "Say 'no' and provide data-driven reasons and alternative solutions"},
            ]
        },
         "Data Analyst": {
             "Technical": [
                 {"q": "What is the difference between SQL and NoSQL databases?", "options": ["SQL is for structured data, NoSQL is for unstructured data", "NoSQL is older than SQL", "SQL is only used for web apps", "There is no difference"], "answer": "SQL is for structured data, NoSQL is for unstructured data"},
                 {"q": "Explain what a LEFT JOIN does in SQL.", "options": ["Returns all records from the right table, and the matched records from the left table", "Returns only records that have matching values in both tables", "Returns all records from the left table, and the matched records from the right table", "Returns records from the right table only"], "answer": "Returns all records from the left table, and the matched records from the right table"},
             ],
            "Behavioral": [
                 {"q": "Describe a time you had to explain a complex data finding to a non-technical audience.", "options": ["Used highly technical jargon", "Simplified the message using visualizations and analogies", "Sent them the raw data", "Told them it was too complex to understand"], "answer": "Simplified the message using visualizations and analogies"},
            ]
        }
    }

    # --- No changes needed to the logic below ---
    
    selected_questions_pool = questions_db.get(role, {}).get(mode, [])
    
    # If the pool is smaller than the number of questions requested, just return the whole pool
    if len(selected_questions_pool) < num_qs:
        # We shuffle the pool anyway so the order is random
        random.shuffle(selected_questions_pool)
        return selected_questions_pool

    # Use random.sample to pick a unique, shuffled set of questions
    return random.sample(selected_questions_pool, k=num_qs)
```

**What did I change?**

1.  **Added More Questions:** I expanded the lists of questions for each role and mode. Now, when `random.sample(..., k=3)` is called on a list of 6 questions, it has many different combinations to choose from.
2.  **Added a Safeguard:** I added a small check. If you ask for more questions than are available in the database, it will just return all the available questions in a random order, preventing an error.

### Step 2: Commit and Push to GitHub

No other files need to be changed. Now, just commit this update to your repository.

1.  **Open a terminal or command prompt** in your project's root directory.
2.  **Add the changed file** to the staging area.
    ```bash
    git add utils/prompts.py
    ```
3.  **Commit the change** with a clear message.
    ```bash
    git commit -m "feat: Expand question database for better shuffling"
    ```
4.  **Push the change** to GitHub.
    ```bash
    git push origin main
    

