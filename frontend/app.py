import streamlit as st
import requests
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env", override=True)

API_URL = os.getenv("API_URL", "http://localhost:8000")
BUSINESS_NAME = os.getenv("BUSINESS_NAME") or "your business"

MOCK_FAQS = {
    "What is your return policy?": "You can return items within 30 days of purchase for a full refund.",
    "How do I contact support?": f"Email us at support@{BUSINESS_NAME}.com or call 1-800-555-0123.",
    "What are your business hours?": "We're open Monday-Friday 9am-6pm EST.",
    "Do you offer international shipping?": "Yes, we ship to over 50 countries worldwide.",
    "How can I track my order?": "Log into your account and go to 'My Orders' to see tracking info.",
}

st.set_page_config(page_title="BizBot", layout="centered")

st.markdown(
    """
    <style>
    :root {
        --ink: #ffffff;
        --muted: #c8c8c8;
        --line: #444444;
    }

    .stApp {
        color: var(--ink);
        background:
            radial-gradient(ellipse at 50% -20%, rgba(255, 255, 255, 0.12), transparent 48%),
            radial-gradient(ellipse at 100% 60%, rgba(255, 255, 255, 0.035), transparent 34%),
            linear-gradient(145deg, #080808 0%, #111111 48%, #050505 100%);
    }

    .stApp,
    .stApp p,
    .stApp label,
    .stApp h1,
    .stApp h2,
    .stApp h3,
    .stApp [data-testid="stMarkdownContainer"],
    .stApp [data-testid="stCaptionContainer"],
    .stApp [data-testid="stChatMessage"] {
        color: var(--ink);
    }

    [data-testid="stHeader"] {
        background: rgba(8, 8, 8, 0.88);
    }

    h1 {
        color: #ffffff;
        letter-spacing: -0.045em;
        text-shadow: 0 0 28px rgba(255, 255, 255, 0.22);
    }

    h1::after {
        content: "";
        display: block;
        width: 4rem;
        height: 3px;
        margin-top: 0.65rem;
        border-radius: 3px;
        background: linear-gradient(90deg, #ffffff, rgba(255, 255, 255, 0.12));
    }

    [data-testid="stCaptionContainer"] {
        color: var(--muted);
    }

    [data-testid="stChatMessage"] {
        border: 1px solid var(--line);
        border-radius: 18px;
        background: linear-gradient(145deg, rgba(31, 31, 31, 0.98), rgba(16, 16, 16, 0.98));
        box-shadow: 0 14px 36px rgba(0, 0, 0, 0.42), inset 0 1px rgba(255, 255, 255, 0.035);
        padding: 1.1rem 1.2rem;
        transition: border-color 150ms ease, transform 150ms ease;
    }

    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        border-color: #888888;
        background: linear-gradient(120deg, #242424, #151515 72%);
    }

    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
        border-color: #3f3f3f;
        background: linear-gradient(120deg, #171717, #0d0d0d 72%);
    }

    /* Style Streamlit's fixed composer area as well as the input itself. */
    [data-testid="stBottom"] {
        background: linear-gradient(180deg, #111111 0%, #090909 100%);
    }

    .stChatFloatingInputContainer {
        border-top: 1px solid #3f3f3f;
        padding: 1rem 0 1.2rem;
        background: linear-gradient(180deg, #151515 0%, #0b0b0b 100%);
        box-shadow: 0 -12px 32px rgba(0, 0, 0, 0.5);
    }

    [data-testid="stChatInput"] {
        border: 1px solid #777777;
        border-radius: 17px;
        background: linear-gradient(110deg, #1b1b1b, #101010);
        box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.025),
                    0 12px 34px rgba(0, 0, 0, 0.58);
        transition: border-color 150ms ease, box-shadow 150ms ease;
    }

    [data-testid="stChatInput"] textarea,
    [data-testid="stTextInput"] input,
    [data-testid="stNumberInput"] input {
        color: #ffffff;
        caret-color: #ffffff;
    }

    [data-testid="stChatInput"] textarea:focus,
    [data-testid="stChatInput"] textarea:focus-visible {
        outline: none !important;
        box-shadow: none !important;
    }

    [data-testid="stChatInput"] textarea::placeholder,
    [data-testid="stTextInput"] input::placeholder {
        color: #c8c8c8;
        opacity: 1;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #151515, #080808);
        border-right: 1px solid #3e3e3e;
    }

    [data-testid="stSidebar"] [data-testid="stAlert"] {
        background: linear-gradient(135deg, #222222, #141414);
        border-color: #555555;
    }

    [data-testid="stAlert"] {
        color: #ffffff;
        border: 1px solid #666666;
        border-radius: 13px;
        background: linear-gradient(135deg, #202020, #121212);
    }

    .stButton button {
        color: #ffffff;
        border: 1px solid #777777;
        border-radius: 12px;
        background: linear-gradient(135deg, #262626, #111111);
        font-weight: 700;
        transition: all 150ms ease;
    }

    .stButton button:hover {
        color: #ffffff;
        border-color: #ffffff;
        background: #333333;
        box-shadow: 0 0 20px rgba(255, 255, 255, 0.18);
        transform: translateY(-1px);
    }

    [data-testid="stChatInput"] button {
        color: #050505;
        border: 1px solid #ffffff;
        border-radius: 11px;
        background: #ffffff;
        transition: transform 150ms ease, background 150ms ease;
    }

    [data-testid="stChatInput"] button:hover {
        color: #000000;
        border-color: #ffffff;
        background: #d8d8d8;
        transform: scale(1.04);
    }

    [data-testid="stChatInput"] button svg {
        fill: currentColor;
    }

    :focus-visible {
        outline: 2px solid #ffffff !important;
        outline-offset: 2px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("BizBot")
st.caption("You Name The Query And I Will Find You The Solution!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type your question here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    f"{API_URL}/chat",
                    json={"message": prompt},
                    timeout=30
                )
                response.raise_for_status()
                data = response.json()
                answer = data["response"]
                source = data["source"]
                st.markdown(answer)
                st.caption(f"Source: {source}")
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to backend. Is the API running?")
            except Exception as e:
                st.error(f"Error: {str(e)}")

with st.sidebar:
    st.header("Settings")
    st.info(f"API: {API_URL}")

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

st.header("Quick Questions")
selected_faq = st.selectbox(
    "Select a common question:",
    options=[""] + list(MOCK_FAQS.keys()),
    format_func=lambda x: x if x else "— Choose a question —",
    key="faq_selector"
)

if selected_faq:
    if st.button("Ask this question", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": selected_faq})
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    f"{API_URL}/chat",
                    json={"message": selected_faq},
                    timeout=30
                )
                response.raise_for_status()
                data = response.json()
                answer = data["response"]
                source = data["source"]
                st.session_state.messages.append({"role": "assistant", "content": answer})
                st.rerun()
            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to backend. Is the API running?")
            except Exception as e:
                st.error(f"Error: {str(e)}")