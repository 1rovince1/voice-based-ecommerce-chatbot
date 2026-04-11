from uuid import uuid4
import streamlit as st
import requests

API_URL = "http://localhost:8000/agent/v1/chat"


st.set_page_config(
    page_title="E-commerce Bot",
    # page_icon="🚢",
    layout="centered"
)

st.title("E-commerce Bot")
st.caption(
    "Ask me about ecommerce data and/or ecommerce policy data, and I'll be glad to help you"
)

# ---------- Session ----------
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello! I am your e-commerce Assistant."
            )
        }
    ]

# ---------- Show chat ----------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------- Input ----------
if prompt := st.chat_input(
    "E.g. Which country's item is traded the most? Also, tell me the methods that can be used for payments."
):

    # show user
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    # call API
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            try:

                payload = {
                    "user_query": prompt
                }

                r = requests.post(
                    API_URL,
                    json=payload,
                    timeout=120,
                    headers={
                        "CHAT-SERVICE-AUTH-KEY": "chAT-SERVice_AUth-keY",
                        "session-id": str(st.session_state.session_id),
                    }
                )

                r.raise_for_status()
                data = r.json()
                ai_response = data["chat_agent_response"]
                st.markdown(ai_response)
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": ai_response
                    }
                )

            except Exception as e:
                error_msg = f"Error calling API: {e}"
                st.error(error_msg)
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_msg
                    }
                )