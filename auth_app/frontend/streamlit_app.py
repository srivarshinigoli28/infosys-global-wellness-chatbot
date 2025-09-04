import os
import requests
import streamlit as st

API_BASE = os.environ.get("API_BASE", "http://127.0.0.1:8000")

st.set_page_config(page_title="Global Wellness Chatbot", layout="centered")

st.markdown(
    """
    <style>
    /* App background */
    .stApp {
        background-color: #ffffff !important;
        color: #000000 !important;
    }

    /* Titles & headers */
    h1, h2, h3, h4, h5, h6 {
        color: #000000 !important;
    }

    /* All dropdowns / selectboxes */
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    div[data-baseweb="select"] span, div[data-baseweb="select"] input {
        color: #000000 !important;
    }
    div[data-baseweb="select"] span[class*="SingleValue"] {
        color: #000000 !important;
    }
    div[data-baseweb="select"] div[class*="Option"] {
        background-color: #ffffff !important;
        color: #000000 !important;
    }

    /* Labels and normal text */
    .css-10trblm, .css-16huue1, .stMarkdown, label, p, span, div {
        color: #000000 !important;
    }

    /* Input boxes */
    .stTextInput input, .stPasswordInput input, .stSelectbox div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #cccccc !important;
    }

    /* Buttons */
    .stButton>button {
        background-color: #f5f5f5 !important;
        color: #000000 !important;
        border: 1px solid #cccccc !important;
        border-radius: 6px !important;
        padding: 0.5em 1em;
    }
    .stButton>button:hover {
        background-color: #e6e6e6 !important;
        border-color: #999999 !important;
    }

    /* Divider */
    hr {
        border: 1px solid #cccccc !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# utils
def api_post(path, json=None, token=None):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    resp = requests.post(f"{API_BASE}{path}", json=json, headers=headers, timeout=10)
    if resp.status_code >= 400:
        try:
            detail = resp.json().get("detail", resp.text)
        except Exception:
            detail = resp.text
        st.error(detail)
        return None
    return resp.json()

def api_get(path, token=None):
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    resp = requests.get(f"{API_BASE}{path}", headers=headers, timeout=10)
    if resp.status_code >= 400:
        try:
            detail = resp.json().get("detail", resp.text)
        except Exception:
            detail = resp.text
        st.error(detail)
        return None
    return resp.json()

def api_put(path, json=None, token=None):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    resp = requests.put(f"{API_BASE}{path}", json=json, headers=headers, timeout=10)
    if resp.status_code >= 400:
        try:
            detail = resp.json().get("detail", resp.text)
        except Exception:
            detail = resp.text
        st.error(detail)
        return None
    return resp.json()

if "token" not in st.session_state:
    st.session_state.token = None
if "profile" not in st.session_state:
    st.session_state.profile = None
if "mode" not in st.session_state:
    st.session_state.mode = "login"

st.title("Global Wellness Chatbot")

# navbar
col1, col2, col3 = st.columns([1,1,1])
with col1:
    if st.button("Login"):
        st.session_state.mode = "login"
with col2:
    if st.button("Register"):
        st.session_state.mode = "register"
with col3:
    if st.button("Profile"):
        st.session_state.mode = "profile"

st.write("---")

def show_login():
    st.subheader("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Sign in"):
        data = api_post("/login", {"email": email, "password": password})
        if data:
            st.session_state.token = data["access_token"]
            st.session_state.mode = "profile"
            st.rerun()

def show_register():
    st.subheader("Register")
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    if st.button("Create account"):
        data = api_post("/register", {
            "name": name,
            "email": email,
            "password": password,
            "confirm_password": confirm_password
        })
        if data:
            st.success("Registered successfully. Please login.")
            st.session_state.mode = "login"

def show_profile():
    token = st.session_state.token
    if not token:
        st.info("Please login to view your profile.")
        return

    if st.session_state.profile is None:
        prof = api_get("/me", token=token)
        if prof:
            st.session_state.profile = prof

    prof = st.session_state.profile or {}
    st.subheader("Your Profile")

    # Fields
    name = st.text_input("Name", value=prof.get("name", ""))

    age_group = st.selectbox(
        "Age Group",
        ["", "Under 18", "18-24", "25-34", "35-44", "45-54", "55+"],
        index=(["", "Under 18", "18-24", "25-34", "35-44", "45-54", "55+"].index(prof.get("age_group", "")) 
               if prof.get("age_group") in ["", "Under 18", "18-24", "25-34", "35-44", "45-54", "55+"] else 0)
    )

    gender = st.selectbox(
        "Gender",
        ["", "Male", "Female", "Other", "Prefer not to say"],
        index=(["", "Male", "Female", "Other", "Prefer not to say"].index(prof.get("gender", "")) 
               if prof.get("gender") in ["", "Male", "Female", "Other", "Prefer not to say"] else 0)
    )

    language = st.selectbox(
        "Preferred Language",
        ["", "English", "Spanish", "French", "German", "Chinese", "Hindi", "Other"],
        index=(["", "English", "Spanish", "French", "German", "Chinese", "Hindi", "Other"].index(prof.get("language", "")) 
               if prof.get("language") in ["", "English", "Spanish", "French", "German", "Chinese", "Hindi", "Other"] else 0)
    )

    new_password = st.text_input("New Password (optional)", type="password")

    if st.button("Save changes"):
        data = api_put(
            "/me",
            {
                "name": name,
                "new_password": new_password or None,
                "age_group": age_group or None,
                "gender": gender or None,
                "language": language or None,
            },
            token=token,
        )
        if data:
            st.success("Profile updated")
            st.session_state.profile = data
            st.rerun()

    st.write("")
    if st.button("Log out"):
        st.session_state.token = None
        st.session_state.profile = None
        st.session_state.mode = "login"
        st.rerun()

if st.session_state.mode == "login":
    show_login()
elif st.session_state.mode == "register":
    show_register()
else:
    show_profile()

