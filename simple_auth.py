import streamlit as st
import hashlib
import json
import os
from pathlib import Path

# File to store user credentials
USERS_FILE = "users.json"

# Initialize users file if it doesn't exist
def init_users_file():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({}, f)

# Load users from file
def load_users():
    init_users_file()
    with open(USERS_FILE, "r") as f:
        return json.load(f)

# Save users to file
def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

# Hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Sign up a new user
def sign_up(email, password):
    try:
        users = load_users()
        
        # Check if user already exists
        if email in users:
            st.error("User already exists")
            return None
        
        # Create new user
        hashed_password = hash_password(password)
        users[email] = {
            "password": hashed_password,
            "uid": hashlib.md5(email.encode()).hexdigest()
        }
        
        # Save updated users
        save_users(users)
        
        return {
            "email": email,
            "uid": users[email]["uid"]
        }
    except Exception as e:
        st.error(f"Error creating account: {str(e)}")
        return None

# Sign in a user
def sign_in(email, password):
    try:
        users = load_users()
        
        # Check if user exists
        if email not in users:
            st.error("User does not exist")
            return None
        
        # Check password
        hashed_password = hash_password(password)
        if users[email]["password"] != hashed_password:
            st.error("Invalid password")
            return None
        
        return {
            "email": email,
            "uid": users[email]["uid"]
        }
    except Exception as e:
        st.error(f"Error signing in: {str(e)}")
        return None

# Reset password (simplified)
def reset_password(email):
    try:
        users = load_users()
        
        # Check if user exists
        if email not in users:
            st.error("User does not exist")
            return False
        
        # In a real app, we would send an email here
        # For this demo, we'll just show a success message
        st.success(f"Password reset link would be sent to {email}")
        return True
    except Exception as e:
        st.error(f"Error resetting password: {str(e)}")
        return False 