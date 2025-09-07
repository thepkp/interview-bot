import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json
import pandas as pd

# Function to initialize Firestore
# Uses st.cache_resource to only run once per session
@st.cache_resource
def init_firestore():
    """Initializes a connection to the Firestore database."""
    try:
        # Check if the app is already initialized
        if not firebase_admin._apps:
            # Get the service account key from Streamlit secrets
            secret_value = st.secrets["FIREBASE_SERVICE_ACCOUNT"]

            # Check if Streamlit has already parsed the secret as a dictionary
            if isinstance(secret_value, dict):
                service_account_key = secret_value
            # If it's a string, load it as JSON
            elif isinstance(secret_value, str):
                service_account_key = json.loads(secret_value)
            else:
                raise TypeError("Firebase service account secret is not in a valid format (string or dict).")

            cred = credentials.Certificate(service_account_key)
            firebase_admin.initialize_app(cred)
        # Return the Firestore client
        return firestore.client()
    except Exception as e:
        # Provide a more helpful error message
        st.error(f"Failed to initialize Firestore: {e}. Please ensure your FIREBASE_SERVICE_ACCOUNT secret is a valid JSON.")
        return None

def save_score(db, name, email, score, total_questions, role):
    """Saves a user's score to the leaderboard collection."""
    if not db:
        return

    # Calculate the score percentage for sorting
    percentage = (score / total_questions) * 100 if total_questions > 0 else 0
    
    doc_ref = db.collection('leaderboard').document()
    doc_ref.set({
        'name': name,
        'email': email,
        'score': score,
        'total_questions': total_questions,
        'percentage': percentage,
        'role': role,
        'timestamp': firestore.SERVER_TIMESTAMP
    })

def get_leaderboard(db, role_filter='All'):
    """Fetches and formats the leaderboard data from Firestore."""
    if not db:
        return pd.DataFrame()

    query = db.collection('leaderboard')
    
    # Apply role filter if it's not 'All'
    if role_filter != 'All':
        query = query.where('role', '==', role_filter)
        
    # Order by the highest percentage and limit to the top 10
    docs = query.order_by('percentage', direction=firestore.Query.DESCENDING).limit(10).stream()
    
    leaderboard_data = []
    for i, doc in enumerate(docs):
        data = doc.to_dict()
        leaderboard_data.append({
            "Rank": i + 1,
            "Name": data.get("name"),
            "Role": data.get("role"),
            "Score": f"{data.get('score', 0)} / {data.get('total_questions', 0)} ({data.get('percentage', 0):.1f}%)"
        })
        
    return pd.DataFrame(leaderboard_data)

