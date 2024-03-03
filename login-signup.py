import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth, firestore

# Initialize Firebase Admin SDK
cred = credentials.Certificate("firebase-metadata/wit-reality-firebase-data.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Streamlit app
def main():
    st.title("Firebase Authentication Demo")

    # Page navigation
    page = st.sidebar.radio("Navigation", ["Signup", "Login", "Dashboard"])

    if page == "Signup":
        signup()
    elif page == "Login":
        login()
    elif page == "Dashboard":
        dashboard()

# Signup page
def signup():
    st.header("Signup")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        if email and password:
            try:
                user = auth.create_user_with_email_and_password(email, password)
                st.success(f"Successfully signed up as {email}")
            except auth.AuthError as e:
                st.error(f"Signup failed: {e}")

# Login page
def login():
    st.header("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Sign In"):
        if email and password:
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                st.success(f"Successfully signed in as {user['email']}")
            except auth.AuthError as e:
                st.error(f"Authentication failed: {e}")

# Dashboard page
def dashboard():
    st.header("Dashboard")

    user = auth.current_user

    if user:
        st.write(f"Welcome, {user.email}!")

        # Text input
        input_text = st.text_area("Enter your text:")
        if st.button("Submit"):
            if input_text:
                save_text(user.uid, input_text)
                st.success("Text saved successfully!")
            else:
                st.warning("Please enter some text before saving.")
    else:
        st.error("User not authenticated.")

# Save text input to Firestore
def save_text(user_id, text):
    doc_ref = db.collection("users").document(user_id)
    doc_ref.set({"text": text})

if __name__ == "__main__":
    main()

