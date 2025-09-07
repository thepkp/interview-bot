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
            {"q": "What is the CAP theorem and what does it state?", "options": ["Consistency, Atomicity, Partition Tolerance", "Consistency, Availability, Partition Tolerance", "Concurrency, Availability, Performance", "Consistency, Availability, Persistence"], "answer": "Consistency, Availability, Partition Tolerance"},
            {"q": "How would you design a distributed caching system?", "options": ["Using a single, powerful server", "Using a consistent hashing ring with multiple nodes", "Storing cache data in a SQL database", "By turning off the database"], "answer": "Using a consistent hashing ring with multiple nodes"},
            {"q": "Explain the concept of database sharding.", "options": ["A type of data encryption", "Horizontally partitioning data across multiple databases", "Creating a backup of a database", "A database indexing technique"], "answer": "Horizontally partitioning data across multiple databases"},
            {"q": "What is the difference between a load balancer and a reverse proxy?", "options": ["They are the same thing", "A load balancer distributes traffic, a reverse proxy retrieves resources on behalf of a client", "A load balancer is for databases, a reverse proxy is for web servers", "A reverse proxy is a type of firewall"], "answer": "A load balancer distributes traffic, a reverse proxy retrieves resources on behalf of a client"},
            {"q": "How does the TCP three-way handshake work?", "options": ["SYN, SYN-ACK, ACK", "REQ, RESP, FIN", "START, DATA, END", "SYN, FIN, ACK"], "answer": "SYN, SYN-ACK, ACK"},
            {"q": "What problem does consistent hashing solve?", "options": ["Minimizes key remapping when nodes are added or removed", "Ensures data is always consistent", "Speeds up database queries", "Prevents SQL injection attacks"], "answer": "Minimizes key remapping when nodes are added or removed"},
            {"q": "Design a system to find the top K most frequent elements in a stream of data.", "options": ["Store all elements in a list and sort", "Use a hash map and a min-heap (priority queue)", "Use a balanced binary search tree", "A simple array is sufficient"], "answer": "Use a hash map and a min-heap (priority queue)"},
            {"q": "What are microservices and what are their benefits?", "options": ["A design pattern for small databases", "An architectural style that structures an application as a collection of loosely coupled services", "A type of JavaScript framework", "A way to write monolithic applications"], "answer": "An architectural style that structures an application as a collection of loosely coupled services"}
        ]
    },
    "Software Engineer": {
        "Technical": [
            {"q": "What is the difference between a list and a tuple in Python?", "options": ["Lists are mutable, tuples are not", "Tuples are mutable, lists are not", "They are the same", "Lists can only store integers"], "answer": "Lists are mutable, tuples are not"},
            {"q": "Explain the concept of 'Big O notation'.", "options": ["A way to measure algorithm efficiency", "A type of data structure", "A sorting algorithm", "A programming language"], "answer": "A way to measure algorithm efficiency"},
            {"q": "What is the difference between a process and a thread?", "options": ["Threads share memory space, processes do not", "Processes are always faster than threads", "A process can have only one thread", "They are the same concept"], "answer": "Threads share memory space, processes do not"},
            {"q": "What are ACID properties in the context of databases?", "options": ["Atomicity, Consistency, Isolation, Durability", "Association, Concurrency, Integrity, Durability", "Availability, Consistency, Integrity, Distribution", "Atomicity, Concurrency, Isolation, Distribution"], "answer": "Atomicity, Consistency, Isolation, Durability"},
            {"q": "What is polymorphism in Object-Oriented Programming?", "options": ["The ability of an object to take on many forms", "A way to inherit properties from a parent class", "The process of hiding implementation details", "A type of data encapsulation"], "answer": "The ability of an object to take on many forms"},
            {"q": "What is the purpose of a CDN (Content Delivery Network)?", "options": ["To host the main application server", "To improve website performance by distributing content geographically closer to users", "To act as a primary database", "A tool for version control"], "answer": "To improve website performance by distributing content geographically closer to users"},
            {"q": "What is the difference between `let`, `const`, and `var` in JavaScript?", "options": ["There is no difference", "`let` and `const` are block-scoped, `var` is function-scoped", "`var` is the modern standard", "`const` variables can be reassigned"], "answer": "`let` and `const` are block-scoped, `var` is function-scoped"},
            {"q": "What is a deadlock in operating systems?", "options": ["When a process is finished executing", "A situation where two or more competing actions are waiting for the other to finish", "A security vulnerability", "A type of memory leak"], "answer": "A situation where two or more competing actions are waiting for the other to finish"},
            {"q": "What is Docker?", "options": ["A programming language", "A database management system", "A platform for developing, shipping, and running applications in containers", "A version control system like Git"], "answer": "A platform for developing, shipping, and running applications in containers"},
            {"q": "Explain the concept of RESTful APIs.", "options": ["A type of database", "A software architectural style for creating networked applications", "A specific programming language", "A data serialization format"], "answer": "A software architectural style for creating networked applications"}
        ],
        "Behavioral": [
            {"q": "Tell me about a time you had a conflict with a coworker and how you resolved it.", "options": ["Ignored the conflict", "Discussed it openly with the coworker to find a solution", "Reported it to HR immediately", "Asked to be moved to another team"], "answer": "Discussed it openly with the coworker to find a solution"},
            {"q": "Describe a challenging project you worked on and how you handled it.", "options": ["I avoided the challenging parts", "Broke the project down into smaller tasks and prioritized them", "Complained to my manager daily", "I quit the project"], "answer": "Broke the project down into smaller tasks and prioritized them"},
            {"q": "How do you keep your technical skills up-to-date?", "options": ["I don't, I rely on my existing knowledge", "By reading tech blogs, taking online courses, and working on side projects", "Only by doing what's required for my job", "Waiting for my company to provide training"], "answer": "By reading tech blogs, taking online courses, and working on side projects"},
            {"q": "Tell me about a time you made a technical mistake. What did you do?", "options": ["I blamed a coworker", "I tried to hide the mistake", "I owned up to it, identified the root cause, and communicated the fix", "I pretended it didn't happen"], "answer": "I owned up to it, identified the root cause, and communicated the fix"},
            {"q": "How do you handle negative feedback on your code or work?", "options": ["I get defensive and argue", "I ignore it completely", "I listen, ask clarifying questions, and use it as a learning opportunity", "I agree with everything without understanding"], "answer": "I listen, ask clarifying questions, and use it as a learning opportunity"},
            {"q": "How would you explain a complex technical concept to a non-technical stakeholder?", "options": ["I would use as much technical jargon as possible", "I wouldn't bother explaining it", "Use analogies and focus on the 'what' and 'why' rather than the 'how'", "I would send them the technical documentation"], "answer": "Use analogies and focus on the 'what' and 'why' rather than the 'how'"},
            {"q": "How do you approach learning a new technology or framework?", "options": ["I read the entire documentation from start to finish", "I jump in and start coding without a plan", "I start with the official tutorials, then build a small project to solidify my understanding", "I wait for a senior engineer to teach me"], "answer": "I start with the official tutorials, then build a small project to solidify my understanding"},
            {"q": "Describe your process for debugging a difficult issue.", "options": ["Randomly change code until it works", "Restart the computer and hope for the best", "Reproduce the bug, form a hypothesis, and test it by isolating variables", "Ask a senior engineer to fix it for me"], "answer": "Reproduce the bug, form a hypothesis, and test it by isolating variables"},
            {"q": "How do you deal with technical debt?", "options": ["Ignore it, it's not a priority", "Advocate for allocating time to refactor and address it in future sprints", "Rewrite the entire application from scratch", "Blame previous developers for it"], "answer": "Advocate for allocating time to refactor and address it in future sprints"},
            {"q": "What are your long-term career goals as a software engineer?", "options": ["I don't have any", "To become a senior individual contributor or move into a leadership role", "To switch to a non-technical field", "To do the same thing I'm doing now forever"], "answer": "To become a senior individual contributor or move into a leadership role"}
        ]
    },
    "Product Manager": {
        "Technical": [
            {"q": "What is an API and how does it differ from an SDK?", "options": ["They are the same", "API is a set of rules, SDK is a set of tools", "API is for frontend, SDK is for backend", "SDK is a type of API"], "answer": "API is a set of rules, SDK is a set of tools"},
            {"q": "Explain the difference between front-end and back-end development.", "options": ["Front-end is what the user sees, back-end is the server logic", "Front-end uses HTML, back-end uses CSS", "There is no difference", "Front-end is harder than back-end"], "answer": "Front-end is what the user sees, back-end is the server logic"},
            {"q": "What is a 'tech stack'?", "options": ["A pile of old computers", "A list of required bug fixes", "The set of technologies used to build an application", "A software design pattern"], "answer": "The set of technologies used to build an application"},
            {"q": "What does it mean for a system to be 'scalable'?", "options": ["It is easy to use", "It has no bugs", "It can handle a growing amount of work or users", "It is written in a popular language"], "answer": "It can handle a growing amount of work or users"},
            {"q": "What is the purpose of a wireframe vs. a mockup vs. a prototype?", "options": ["They all mean the same thing", "Wireframe is structure, Mockup is visual, Prototype is interactive", "A prototype is a final product", "Wireframes are only for mobile apps"], "answer": "Wireframe is structure, Mockup is visual, Prototype is interactive"},
            {"q": "Explain what a SQL JOIN is used for.", "options": ["To delete a table", "To combine rows from two or more tables based on a related column", "To create a new database", "To add a new column to a table"], "answer": "To combine rows from two or more tables based on a related column"},
            {"q": "How would you explain 'technical debt' to a non-technical stakeholder?", "options": ["It's a security bug", "It's the cost of a software license", "It is the implied cost of rework caused by choosing an easy solution now instead of a better approach", "It's money the company owes to its developers"], "answer": "It is the implied cost of rework caused by choosing an easy solution now instead of a better approach"},
            {"q": "What are some key metrics you would track for a mobile app's technical performance?", "options": ["Number of downloads", "Daily active users", "Crash rate and API latency", "App store rating"], "answer": "Crash rate and API latency"},
            {"q": "What is the difference between Agile and Waterfall development methodologies?", "options": ["Agile is iterative, Waterfall is sequential", "Waterfall is a newer methodology", "There is no difference", "Agile is only for small teams"], "answer": "Agile is iterative, Waterfall is sequential"},
            {"q": "What is the role of a database in a modern web application?", "options": ["To style the webpage", "To store, retrieve, and manage user and application data", "To run the web server", "To handle user authentication only"], "answer": "To store, retrieve, and manage user and application data"}
        ],
        "Behavioral": [
            {"q": "How would you prioritize features for a new product?", "options": ["Based on what the CEO likes", "Using a framework like RICE or MoSCoW", "Building the easiest features first", "Based on what competitors have"], "answer": "Using a framework like RICE or MoSCoW"},
            {"q": "How do you measure the success of a product?", "options": ["By the number of features it has", "By how much the development team likes it", "By defining and tracking key metrics (KPIs) like user engagement and revenue", "By the absence of bugs"], "answer": "By defining and tracking key metrics (KPIs) like user engagement and revenue"},
            {"q": "How do you say 'no' to a feature request from a stakeholder?", "options": ["By saying yes to everything to keep them happy", "By ignoring their request", "By explaining the trade-offs and aligning the decision with the product strategy and goals", "By promising to build it later with no intention of doing so"], "answer": "By explaining the trade-offs and aligning the decision with the product strategy and goals"},
            {"q": "Tell me about a product you admire and why.", "options": ["I don't use any products", "Pick a well-known product and explain its excellent user experience or business model", "A product that is very complex and hard to use", "A product that is failing"], "answer": "Pick a well-known product and explain its excellent user experience or business model"},
            {"q": "Describe your process for developing a product roadmap.", "options": ["I just make a list of features I think are cool", "It's a collaborative process involving market research, stakeholder input, and strategic goals", "I copy the roadmap of our main competitor", "The engineers decide what to build"], "answer": "It's a collaborative process involving market research, stakeholder input, and strategic goals"},
            {"q": "Describe a time a product launch didn't go as planned. What did you do?", "options": ["I blamed the marketing team", "I analyzed what went wrong, communicated with stakeholders, and created a plan to address the issues", "I ignored the problem", "I immediately started working on a new product"], "answer": "I analyzed what went wrong, communicated with stakeholders, and created a plan to address the issues"},
            {"q": "How do you work with engineering teams?", "options": ["I give them a list of demands and deadlines", "I work collaboratively, clearly defining the 'what' and 'why', and letting them determine the 'how'", "I attend all of their technical meetings and tell them how to code", "I avoid speaking to them"], "answer": "I work collaboratively, clearly defining the 'what' and 'why', and letting them determine the 'how'"},
            {"q": "How do you handle ambiguity when starting a new project?", "options": ["I wait for someone to give me all the answers", "I panic and do nothing", "I start by conducting research and talking to users to reduce uncertainty and define a clear problem", "I make a lot of assumptions and hope for the best"], "answer": "I start by conducting research and talking to users to reduce uncertainty and define a clear problem"},
            {"q": "What's the most important quality for a Product Manager?", "options": ["Being the best coder on the team", "The ability to write perfect documentation", "Empathy for the user and strong communication skills", "The ability to create the best PowerPoint slides"], "answer": "Empathy for the user and strong communication skills"},
            {"q": "How do you conduct user research?", "options": ["By assuming I am the user", "Through a mix of surveys, interviews, and usability testing", "By asking my friends what they think", "I don't, I just build what I think is right"], "answer": "Through a mix of surveys, interviews, and usability testing"}
        ]
    },
    "Data Analyst": {
        "Technical": [
            {"q": "What is the difference between SQL and NoSQL databases?", "options": ["SQL is for structured data, NoSQL is for unstructured data", "NoSQL is older than SQL", "SQL is only used for web apps", "There is no difference"], "answer": "SQL is for structured data, NoSQL is for unstructured data"},
            {"q": "What is the difference between `JOIN` and `UNION` in SQL?", "options": ["`JOIN` combines columns from different tables, `UNION` combines rows", "`UNION` combines columns, `JOIN` combines rows", "They are identical operations", "`JOIN` is faster than `UNION`"], "answer": "`JOIN` combines columns from different tables, `UNION` combines rows"},
            {"q": "Explain the ETL (Extract, Transform, Load) process.", "options": ["A type of database query", "A process to move data from a source to a data warehouse", "A data visualization technique", "A statistical modeling method"], "answer": "A process to move data from a source to a data warehouse"},
            {"q": "What is data cleaning?", "options": ["Deleting all your data", "The process of detecting and correcting corrupt or inaccurate records from a dataset", "A way to format charts and graphs", "The final step in data visualization"], "answer": "The process of detecting and correcting corrupt or inaccurate records from a dataset"},
            {"q": "What is the difference between `DELETE`, `TRUNCATE`, and `DROP` in SQL?", "options": ["They are all the same", "`DELETE` is row-level, `TRUNCATE` removes all rows, `DROP` removes the table", "`DROP` is the only one that is reversible", "`TRUNCATE` is faster than `DELETE` because it doesn't log"], "answer": "`DELETE` is row-level, `TRUNCATE` removes all rows, `DROP` removes the table"},
            {"q": "What is the p-value in the context of hypothesis testing?", "options": ["The probability of the result being correct", "The probability of observing the data, assuming the null hypothesis is true", "The power of a statistical test", "The sample size"], "answer": "The probability of observing the data, assuming the null hypothesis is true"},
            {"q": "What are window functions in SQL?", "options": ["Functions that open a new window in the browser", "Functions that operate on a set of rows and return a single value for each row from the underlying query", "Functions for creating graphical user interfaces", "A type of data encryption"], "answer": "Functions that operate on a set of rows and return a single value for each row from the underlying query"},
            {"q": "Explain the concept of A/B testing.", "options": ["A test with only two questions", "A method of comparing two versions of a webpage or app against each other to determine which one performs better", "A type of database backup", "Testing the API and the Backend"], "answer": "A method of comparing two versions of a webpage or app against each other to determine which one performs better"},
            {"q": "What is the difference between supervised and unsupervised machine learning?", "options": ["Supervised learning uses labeled data, unsupervised learning uses unlabeled data", "Unsupervised learning is always more accurate", "Supervised learning requires a human to watch the computer", "There is no difference"], "answer": "Supervised learning uses labeled data, unsupervised learning uses unlabeled data"},
            {"q": "What is a data warehouse?", "options": ["A physical building where servers are stored", "A large, centralized repository of data that is used for reporting and analysis", "A small, temporary database", "The same as a standard transactional database"], "answer": "A large, centralized repository of data that is used for reporting and analysis"}
        ],
        "Behavioral": [
            {"q": "Describe a time you found an unexpected insight in a dataset. What was the impact?", "options": ["I ignored it to finish my work faster", "I investigated it further and presented the finding, which led to a new business strategy", "I assumed it was an error in the data", "I kept the finding to myself"], "answer": "I investigated it further and presented the finding, which led to a new business strategy"},
            {"q": "How do you ensure the quality and accuracy of your data analysis?", "options": ["I just assume the data is correct", "By performing data validation, checking for outliers, and cross-referencing with other sources", "I ask a colleague to check my work without explaining my methods", "I rush through the analysis to meet deadlines"], "answer": "By performing data validation, checking for outliers, and cross-referencing with other sources"},
            {"q": "Describe a project where you had to work with incomplete or messy data. What steps did you take?", "options": ["I refused to work with the data", "I deleted the rows with missing values", "I used techniques like imputation for missing values and documented my cleaning process", "I presented the messy data as it was"], "answer": "I used techniques like imputation for missing values and documented my cleaning process"},
            {"q": "How do you prioritize your tasks when you have multiple data requests with tight deadlines?", "options": ["I work on the easiest request first", "I work on them in the order they were received", "I assess the impact and urgency of each request and communicate my timeline to stakeholders", "I complain about the workload"], "answer": "I assess the impact and urgency of each request and communicate my timeline to stakeholders"},
            {"q": "Tell me about a time you made a mistake in your analysis. How did you handle it?", "options": ["I hoped nobody would notice", "I immediately informed the stakeholders, corrected the mistake, and explained the impact", "I blamed the data source", "I deleted the analysis and started over without telling anyone"], "answer": "I immediately informed the stakeholders, corrected the mistake, and explained the impact"},
            {"q": "How do you stay updated with the latest trends and tools in data analytics?", "options": ["I rely only on the tools my company provides", "By following industry blogs, participating in webinars, and experimenting with new tools", "I think learning new tools is a waste of time", "I wait to be told what to learn"], "answer": "By following industry blogs, participating in webinars, and experimenting with new tools"},
            {"q": "Describe a situation where your data analysis challenged a long-held belief within the company.", "options": ["I changed my analysis to match the belief", "I presented my findings with clear data and visualizations, and explained my methodology", "I didn't share the findings to avoid conflict", "I announced the finding in a large meeting without preparing stakeholders"], "answer": "I presented my findings with clear data and visualizations, and explained my methodology"},
            {"q": "How would you handle a disagreement with a stakeholder about the interpretation of your data?", "options": ["I would agree with their interpretation to avoid an argument", "I would listen to their perspective and walk them through the data and my analysis to find common ground", "I would insist that my interpretation is the only correct one", "I would escalate the issue to their manager"], "answer": "I would listen to their perspective and walk them through the data and my analysis to find common ground"},
            {"q": "What is your process for starting a new data analysis project?", "options": ["I start creating charts immediately", "I first seek to understand the business problem and the key questions that need to be answered", "I gather as much data as possible without a clear goal", "I wait for detailed instructions on every step"], "answer": "I first seek to understand the business problem and the key questions that need to be answered"},
            {"q": "Can you give an example of how you've used data to tell a compelling story?", "options": ["I just present a table of numbers", "I use visualizations and a clear narrative to explain what the data means and why it's important", "I don't believe in storytelling with data", "I make the story overly complicated with jargon"], "answer": "I use visualizations and a clear narrative to explain what the data means and why it's important"}
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


def get_preset_interview_questions(role, mode, num_qs, custom_set):
    """Helper function to get questions from the hardcoded DB."""
    if custom_set != "Standard":
        selected_questions_pool = questions_db.get("Custom Sets", {}).get(custom_set, [])
    else:
        selected_questions_pool = questions_db.get(role, {}).get(mode, [])

    if not selected_questions_pool:
        return [{"q": "No questions found for this selection.", "options": [], "answer": ""}], None

    # Ensure we don't request more questions than are available
    k = min(num_qs, len(selected_questions_pool))
    
    return random.sample(selected_questions_pool, k=k), None


def get_interview_prompt(role, mode, num_qs, custom_set="Standard", use_ai=False):
    """
    Main function to get questions. It can use AI or the preset database.
    Returns a tuple: (questions_list, error_message)
    """
    # If the user wants AI, use it.
    if use_ai:
        questions, error = get_ai_interview_questions(role, mode, num_qs, custom_set)
        if questions:
            return questions, None
        else:
            # Fallback to preset questions if AI fails
            error_message = f"{error}. Falling back to preset questions."
            preset_questions, _ = get_preset_interview_questions(role, mode, num_qs, custom_set)
            return preset_questions, error_message

    # --- Logic for preset questions (AI toggled off) ---
    return get_preset_interview_questions(role, mode, num_qs, custom_set)

