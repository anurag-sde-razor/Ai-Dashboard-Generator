# This file serves as a wrapper for the authentication UI components
from modules.auth_ui import show_login_page, show_signup_page, show_reset_password_page

# Re-export the functions
__all__ = ['show_login_page', 'show_signup_page', 'show_reset_password_page'] 