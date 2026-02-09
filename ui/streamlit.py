import streamlit as st
import requests

st.set_page_config(page_title="FAQ Chatbot", layout="wide")
st.title("💬 FAQ Chatbot")

API_URL = "http://localhost:8001/chat"  # local backend

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

query = st.chat_input("Ask your question...")

if query:
    # User message
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.write(query)

    # Assistant message
    with st.chat_message("assistant"):
        with st.spinner("Generating answer..."):
            try:
                res = requests.post(
                    API_URL,
                    json={"question": query},
                    timeout=300
                )

                data = res.json()

                if isinstance(data, dict) and "answer" in data:
                    answer = data["answer"]
                else:
                    answer = f"Unexpected backend response: {data}"

            except requests.exceptions.RequestException as e:
                answer = f"Backend connection error: {e}"

            st.write(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )