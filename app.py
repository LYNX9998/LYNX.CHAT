import streamlit as st
import openai

openai.api_key = "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"

# Keep your original functions except UI replaced:

chat_history = []

def get_bot_response(prompt):
    name_queries = [
        "what is your name",
        "who are you",
        "your name",
        "tell me your name",
        "what's your name",
        "may i know your name"
    ]
    if any(phrase in prompt.lower() for phrase in name_queries):
        response_text = "My name is Lynx Bot."
    else:
        messages = []
        if chat_history:
            messages.extend(chat_history)
        messages.append({"role": "user", "content": prompt})

        try:
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.7,
                max_tokens=150,
            )
            response_text = response.choices[0].message.content.strip()
        except Exception as e:
            response_text = f"Error: {str(e)}"

    chat_history.append({"role": "user", "content": prompt})
    chat_history.append({"role": "assistant", "content": response_text})
    return response_text


st.title("Lynx Bot - Web Version")

if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.text_input("Type your message here:")

if st.button("Send") or (user_input and st.session_state.get("last_input") != user_input):
    if user_input.lower() == "exit":
        st.write("Goodbye!")
    else:
        st.session_state.messages.append(("You", user_input))
        reply = get_bot_response(user_input)
        st.session_state.messages.append(("Lynx Bot", reply))
    st.session_state.last_input = user_input

for sender, msg in st.session_state.messages:
    if sender == "You":
        st.markdown(f"**You:** {msg}")
    else:
        st.markdown(f"**Lynx Bot:** {msg}")
