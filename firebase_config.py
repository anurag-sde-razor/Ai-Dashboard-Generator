import streamlit as st
from dotenv import load_dotenv
import os
import json
import requests

# Load environment variables
load_dotenv()

# Firebase configuration
firebase_config = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FIREBASE_APP_ID"),
    "measurementId": os.getenv("FIREBASE_MEASUREMENT_ID")
}

# Firebase REST API endpoints
FIREBASE_AUTH_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={firebase_config['apiKey']}"
FIREBASE_SIGNUP_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={firebase_config['apiKey']}"
FIREBASE_RESET_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={firebase_config['apiKey']}"

def sign_up(email, password):
    try:
        data = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        response = requests.post(FIREBASE_SIGNUP_URL, json=data)
        response_data = response.json()
        
        if response.status_code == 200:
            return {
                "email": email,
                "uid": response_data.get("localId"),
                "idToken": response_data.get("idToken")
            }
        else:
            error_message = response_data.get("error", {}).get("message", "Unknown error")
            st.error(f"Error creating account: {error_message}")
            return None
    except Exception as e:
        st.error(f"Error creating account: {str(e)}")
        return None

def sign_in(email, password):
    try:
        data = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        response = requests.post(FIREBASE_AUTH_URL, json=data)
        response_data = response.json()
        
        if response.status_code == 200:
            return {
                "email": email,
                "uid": response_data.get("localId"),
                "idToken": response_data.get("idToken")
            }
        else:
            error_message = response_data.get("error", {}).get("message", "Unknown error")
            st.error(f"Error signing in: {error_message}")
            return None
    except Exception as e:
        st.error(f"Error signing in: {str(e)}")
        return None

def reset_password(email):
    try:
        data = {
            "email": email,
            "requestType": "PASSWORD_RESET"
        }
        response = requests.post(FIREBASE_RESET_URL, json=data)
        response_data = response.json()
        
        if response.status_code == 200:
            return True
        else:
            error_message = response_data.get("error", {}).get("message", "Unknown error")
            st.error(f"Error sending password reset email: {error_message}")
            return False
    except Exception as e:
        st.error(f"Error sending password reset email: {str(e)}")
        return False 