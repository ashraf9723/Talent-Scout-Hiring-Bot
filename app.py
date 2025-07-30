import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# --- Configuration ---
# Load environment variables from a .env file for local development
load_dotenv()

# Configure the Gemini API key from environment variables or Streamlit secrets
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
    except (KeyError, FileNotFoundError):
        st.error("API Key not found. Please set it in your environment variables or Streamlit secrets.")
        st.stop()

genai.configure(api_key=api_key)

# --- System Prompt (Enhanced for Multilingual & Personalization) ---
system_prompt = """
You are "TalentScout Assistant," a friendly and professional AI hiring assistant for the recruitment agency "TalentScout." Your purpose is to conduct an initial screening of job candidates. Do NOT deviate from this role.

**Primary Directive: Detect the user's language at the very beginning and conduct the entire conversation in that language.** All your greetings, questions, and responses must be localized.

Your conversation will follow these exact steps in order:
1.  **Greeting:** Start with a warm greeting in the user's detected language, introduce yourself, and briefly state your purpose.
2.  **Information Gathering:** Collect the following information from the candidate, one piece at a time, in their language.
    * Full Name
    * Email Address
    * Phone Number
    * Years of Professional Experience
    * Desired Position(s)
    * Current Location (City, Country)
    * Primary Tech Stack (Ask the candidate to list programming languages, frameworks, databases, and other tools they are proficient in).
3.  **Acknowledge and Transition:** After gathering all the information, summarize the key details (Name, Experience, Position, Tech Stack) and inform the candidate you will now ask a few technical questions based on their stack.
4.  **Technical Questions:** Based on the user's declared tech stack, generate exactly 3-5 relevant technical questions. Present all questions at once in a numbered list.
5.  **Conclusion:** Once the candidate has responded, thank them for their time. **Add a personalized touch by mentioning one of the technologies they listed** (e.g., "Your experience with Python looks very interesting."). Inform them that a human recruiter from TalentScout will review their responses. Then, wish them a good day.

**Rules of Engagement:**
* **Be Conversational but Professional:** Use a friendly tone. Keep responses concise.
* **One Question at a Time:** During information gathering, only ask for the next piece of information after the candidate provides the current one.
* **Fallback Mechanism:** If the user's input is unclear or off-topic, gently guide them back to the current question in their language.
* **Ending the Conversation:** If the user uses a conversation-ending keyword (like "bye," "exit," "adios," etc.), immediately proceed to the conclusion step.
"""

# --- Model Initialization ---
chat_model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_prompt
)
sentiment_model = genai.GenerativeModel(model_name="gemini-1.5-flash")


# --- Helper Function for Sentiment Analysis ---
def analyze_sentiment(text):
    if not text:
        return "Not applicable"
    try:
        prompt = f"Analyze the sentiment of the following text. Respond with only one word: Positive, Negative, or Neutral.\n\nText: \"{text}\""
        response = sentiment_model.generate_content(prompt)
        sentiment = response.text.strip().capitalize()
        if sentiment in ["Positive", "Negative", "Neutral"]:
            return sentiment
        return "Could not determine"
    except Exception as e:
        print(f"Sentiment analysis failed: {e}")
        return "Could not determine"


# --- UI Customization ---
def load_css():
    st.markdown("""
    <style>
        /* General body styling with background image */
        .stApp {
            /* Replace the URL below with your own image URL */
            background-image: url("https://images.unsplash.com/photo-1528459801416-a9e53bbf4e17?q=80&w=1912&auto=format&fit=crop");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
        }

        /* Chat bubble styling */
        .st-emotion-cache-1c7y2kd {
            background-color: rgba(255, 255, 255, 0.9); /* Slightly transparent white */
            border-radius: 0.75rem;
            padding: 1rem;
            margin-bottom: 1rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border: 1px solid #e0e0e0;
        }

        /* Assistant chat bubble */
        .st-emotion-cache-4oy321 {
             background-color: rgba(225, 245, 254, 0.95); /* Slightly transparent light blue */
        }

        /* User chat bubble */
        div[data-testid="chat-bubble-stream-user"] {
            background-color: rgba(255, 255, 255, 0.95); /* Slightly transparent white */
        }

        /* Info box for sentiment */
        .stAlert {
            border-radius: 0.5rem;
            background-color: rgba(232, 245, 253, 0.8);
        }

        /* Title styling */
        h1 {
            color: #1e3a8a;
            background-color: rgba(255, 255, 255, 0.7);
            padding: 10px;
            border-radius: 10px;
        }
    </style>
    """, unsafe_allow_html=True)


# --- Streamlit App UI ---
st.set_page_config(page_title="TalentScout Pro", page_icon="🚀")
load_css()

# Sidebar for branding and info
with st.sidebar:
    st.image("D:\PythonProject\PGAGI_AI_INTERN_ASSIGNMENT\images.jpeg", use_column_width=True)
    st.title("Pro Hiring Assistant")
    st.info("This chatbot conducts initial candidate screenings. It is multilingual and gauges candidate sentiment.")
    st.markdown("---")
    st.write("Built with Streamlit & Gemini")

st.title("🚀 TalentScout Hiring Assistant")
st.write(
    "Welcome! I'm here to help with the initial screening process. Please start by saying 'hello' in your preferred language.")
st.markdown("---")

# Initialize chat and sentiment history
if "chat_session" not in st.session_state:
    st.session_state.chat_session = chat_model.start_chat(history=[])
if "sentiment_history" not in st.session_state:
    st.session_state.sentiment_history = []

# Display chat history
for i, message in enumerate(st.session_state.chat_session.history):
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)
        if role == 'user':
            # Display sentiment for past user messages
            sentiment_index = i // 2
            if sentiment_index < len(st.session_state.sentiment_history):
                sentiment = st.session_state.sentiment_history[sentiment_index]
                st.info(f"Sentiment: {sentiment}", icon="😊")

# Handle user input
if prompt := st.chat_input("Your message..."):
    # Display user message and sentiment
    with st.chat_message("user"):
        st.markdown(prompt)
        with st.spinner("Analyzing tone..."):
            sentiment = analyze_sentiment(prompt)
            st.session_state.sentiment_history.append(sentiment)
            st.info(f"Sentiment: {sentiment}", icon="😊")

    # Get and display assistant's response
    try:
        with st.spinner("Thinking..."):
            response = st.session_state.chat_session.send_message(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.info("Please try again or refresh the page.")
