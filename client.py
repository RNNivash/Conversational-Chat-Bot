import firebase_admin
from firebase_admin import credentials, firestore
import pyrebase
import datetime

# Initialize Firebase Admin
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Function to log user queries
def log_user_query(uid, user_input, bot_response):
    doc_ref = db.collection("users").document(uid).collection("chats").document()
    doc_ref.set({
        "query": user_input,
        "response": bot_response,
        "timestamp": datetime.datetime.utcnow()
    })

# Firebase client config
from dotenv import load_dotenv
import os
import pyrebase

load_dotenv()

firebase_config = {
    "apiKey": os.getenv("API_KEY"),
    "authDomain": os.getenv("AUTH_DOMAIN"),
    "databaseURL": os.getenv("DATABASE_URL"),  
    "projectId": os.getenv("PROJECT_ID"),
    "storageBucket": os.getenv("STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("MESSAGING_SENDER_ID"),
    "appId": os.getenv("APP_ID")
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
# Initialize Pyrebase
firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

# Get email and password input from user
email = input("Enter email: ")
password = input("Enter password: ")

# Sign in user
user = auth.sign_in_with_email_and_password(email, password)
uid = user['localId']

# Now, you can log queries and responses for the authenticated user
print(f"Logged in as UID: {uid}")