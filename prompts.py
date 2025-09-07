import random

def get_interview_prompt(role, mode, num_qs, custom_set="None"):
    """
    Generates a list of interview questions.
    If a custom_set is provided, it uses that. Otherwise, it uses role and mode.
    """
    questions_db = {
        # --- NEW: A section for custom, curated question sets ---
        "Custom Sets": {
            "FAANG / MAANG": [
                {"q": "Given an array of integers, find the two numbers that add up to a specific target.", "options": ["Brute-force (O(n^2))", "Hash Map (O(n))", "Sort and two-pointers (O(n log n))", "All of the above are possible solutions"], "answer": "All of the above are possible solutions"},
                {"q": "How would you design a URL shortening service like TinyURL?", "options": ["Using a hash function", "Using a simple counter", "Using a combination of a counter and base62 encoding", "Using a random string generator"], "answer": "Using a combination of a counter and base62 encoding"},
                {"q": "What is the difference between a process and a thread?", "options": ["Threads share memory space, processes don't", "Processes are lighter than threads", "A process can have only one thread", "They are the same"], "answer": "Threads share memory space, processes don't"},
                {"q": "Explain the concept of database indexing.", "options": ["A way to make databases slower but more accurate", "A data structure that improves the speed of data retrieval", "A method for encrypting data", "A way to backup a database"], "answer": "A data structure that improves the speed of data retrieval"},
                {"q": "Describe the CAP theorem in distributed systems.", "options": ["Consistency, Availability, Partition tolerance", "Correctness, Accuracy, Performance", "CPU, Algorithm, Power", "Client, Application, Protocol"], "answer": "Consistency, Availability, Partition tolerance"},
                {"q": "What is Dynamic Programming and when would you use it?", "options": ["For sorting arrays", "For problems with optimal substructure and overlapping subproblems", "For designing user interfaces", "For sending network requests"], "answer": "For problems with optimal substructure and overlapping subproblems"},
            ]
        },
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

    # --- UPDATED LOGIC: Prioritize custom set over role/mode ---
    if custom_set != "None (select role below)":
        selected_questions_pool = questions_db.get("Custom Sets", {}).get(custom_set, [])
    else:
        selected_questions_pool = questions_db.get(role, {}).get(mode, [])

    # If the pool is smaller than the number of questions requested, just return the whole pool
    if len(selected_questions_pool) < num_qs:
        random.shuffle(selected_questions_pool)
        return selected_questions_pool

    # Use random.sample to pick a unique, shuffled set of questions
    return random.sample(selected_questions_pool, k=num_qs)

