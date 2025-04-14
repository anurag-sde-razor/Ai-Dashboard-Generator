import streamlit as st
from firebase_config import sign_up, sign_in, reset_password
import streamlit.components.v1 as components

# Set page config
st.set_page_config(
    page_title="AI Dashboard Generator",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        margin-top: 1rem;
    }
    .auth-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'user' not in st.session_state:
    st.session_state.user = None

def show_login_page():
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    st.title("Login")
    
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login"):
            user = sign_in(email, password)
            if user:
                st.session_state.user = user
                st.success("Logged in successfully!")
                st.rerun()
    
    with col2:
        if st.button("Forgot Password"):
            if email:
                if reset_password(email):
                    st.success("Password reset email sent!")
            else:
                st.warning("Please enter your email first")
    
    st.markdown("Don't have an account? [Sign Up](#signup)", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def show_signup_page():
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    st.title("Sign Up")
    
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    
    if st.button("Sign Up"):
        if password == confirm_password:
            user = sign_up(email, password)
            if user:
                st.success("Account created successfully!")
                st.session_state.user = user
                st.rerun()
        else:
            st.error("Passwords do not match!")
    
    st.markdown("Already have an account? [Login](#login)", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def show_dashboard():
    st.title("Welcome to AI Dashboard Generator")
    st.write("You are logged in!")
    
    if st.button("Logout"):
        st.session_state.user = None
        st.rerun()

# Main app logic
if st.session_state.user is None:
    # Always show authentication page if user is not logged in
    st.title("AI Dashboard Generator")
    st.write("Please login or sign up to access the dashboard")
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        show_login_page()
    
    with tab2:
        show_signup_page()
else:
    # Only show dashboard if user is logged in
    show_dashboard() 