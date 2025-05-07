import streamlit as st
import openai

openai.api_key = st.secrets["OPENAI_API_KEY"]

SYSTEM_PROMPT = (
    "You are Medivise, a helpful, ethical, and supportive health information assistant. "
    "You provide general information about health, illness prevention, and illness management, "
    "but you can't diagnose or prescribe treatment. Always advise users to consult a healthcare provider for specific concerns. "
    "If a question is urgent or medical, remind the user to seek professional help."
)

def ask_gpt(question, chat_history):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
    ]
    for q, a in chat_history:
        messages.append({"role": "user", "content": q})
        messages.append({"role": "assistant", "content": a})
    messages.append({"role": "user", "content": question})

    # Correct way for openai >=1.0.0
    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=400,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()
st.image("aigrowthlane_logo.jpg", width=150)  # <-- Notice the closing parenthesis!
st.title("MediVise Health Advisor 🩺")
st.markdown(
    """
    👋 **Welcome to MediVise!**

    This is your virtual health advisor.  
    Ask any questions you have about staying healthy, preventing illness, or managing minor health concerns.

    **NOTE:**  
    This chatbot gives general information only and is **not a substitute for professional medical advice**. Always consult a healthcare provider for personal concerns.
    """
)
st.write("Ask health-related questions (illness prevention or management).")
st.warning(
    "This tool does NOT provide medical advice. "
    "It is a general information assistant only. "
    "Always consult a healthcare provider for medical concerns."
)

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("Your question:")

if st.button("Ask") and user_input.strip():
    answer = ask_gpt(user_input, st.session_state.history)
    st.session_state.history.append((user_input, answer))

for q, a in reversed(st.session_state.history):
    st.write(f"**You:** {q}")
    st.write(f"**Medivise:** {a}")