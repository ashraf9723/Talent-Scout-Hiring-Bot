# TalentScout Hiring Assistant 🤖

## Project Overview

TalentScout Hiring Assistant is an intelligent chatbot designed to streamline the initial candidate screening process for the "TalentScout" recruitment agency. Built with Python, Streamlit, and Google's Gemini LLM, the chatbot interacts with candidates in a conversational manner to gather essential information and pose relevant technical questions based on their declared skills.

### Key Capabilities

* **Greeting & Introduction:** Starts the conversation with a friendly greeting.
* **Information Gathering:** Systematically collects candidate details (Name, contact info, experience, location, etc.).
* **Dynamic Technical Questions:** Generates 3-5 technical questions tailored to the candidate's specific tech stack.
* **Context-Aware Conversation:** Maintains the flow of dialogue using the LLM's context window.
* **Graceful Interaction:** Includes fallback mechanisms for unclear inputs and a polite conversation closing.

## ⚙️ Technical Details

* **Programming Language:** Python 3.9+
* **Frontend:** Streamlit
* **LLM:** Google Gemini 1.5 Flash
* **Core Logic:** The application's logic is primarily driven by a detailed **system prompt** that dictates the chatbot's persona, rules, and conversation flow. Context is maintained by passing the entire chat history back to the model with each turn, leveraging Streamlit's `st.session_state` to store this history.

## 🚀 Installation & Setup

Follow these steps to set up and run the application locally.

### 1. Clone the Repository

```bash
git clone [https://github.com/](https://github.com/)<your-username>/talent-scout-chatbot.git
cd talent-scout-chatbot
```

### 2. Create a Virtual Environment

It's recommended to use a virtual environment to manage dependencies.

```bash
# For Unix/macOS
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Dependencies

Create a `requirements.txt` file with the following content:

```text
streamlit
google-generativeai
python-dotenv
```

Then, install the packages:

```bash
pip install -r requirements.txt
```

### 4. Configure API Key

You need a Google AI API key to run the application.

1.  Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey).
2.  Create a file named `.env` in the root of your project directory.
3.  Add your API key to the `.env` file:
    ```
    GOOGLE_API_KEY="YOUR_API_KEY_HERE"
    ```
    *Note: The provided `app.py` is configured to use Streamlit Secrets for deployment. For local development, you would uncomment the `python-dotenv` lines in `app.py`.*

## 🏃‍♀️ Usage Guide

To run the application, execute the following command in your terminal:

```bash
streamlit run app.py
```

Your web browser will open a new tab with the chatbot interface. Simply start typing in the chat box to interact with the assistant.

## 🧠 Prompt Design Strategy

The effectiveness of this chatbot relies heavily on its **system prompt**. The prompt was engineered to be a comprehensive "instruction manual" for the LLM.

* **Persona Definition:** The prompt first establishes the chatbot's identity as "TalentScout Assistant," setting a professional and friendly tone.
* **Structured Flow:** It enforces a strict, step-by-step conversational flow (Greeting -> Info Gathering -> Questions -> Conclusion). This prevents the model from jumping ahead or getting stuck.
* **Constrained Behavior:** Rules like "ask one question at a time" and the "fallback mechanism" ensure the conversation stays on track and handles unexpected user inputs gracefully.
* **Dynamic Content Generation:** The prompt explicitly instructs the model to generate a specific number (3-5) of technical questions *based on* the tech stack provided by the user, making the screening relevant.
* **Safe Termination:** Keywords like "bye" or "exit" are defined as triggers for a clean conversation conclusion, improving user experience.

## 💡 Challenges & Solutions

* **Challenge:** Maintaining conversation context and state.
    * **Solution:** Instead of building a complex state machine in Python, we leverage the LLM's large context window. The entire chat history is stored in `st.session_state` and passed to the model with every request, allowing the model itself to track the conversation's state.

* **Challenge:** Ensuring the LLM adheres strictly to the defined conversational flow.
    * **Solution:** The system prompt is highly directive, using strong imperatives ("You will follow these exact steps," "Do NOT deviate"). This significantly constrains the model's output and keeps it focused on its task.

* **Challenge:** Handling sensitive candidate data.
    * **Solution:** The prompt explicitly forbids asking for information beyond the specified list. For a production application, this data would not be stored in `st.session_state` but would be immediately transmitted over HTTPS to a secure, GDPR-compliant backend database for storage and processing.

## ✨ Optional Enhancements (Bonus)

* **Sentiment Analysis:** Could be implemented by making a secondary, non-streaming call to the LLM after each user message, asking it to classify the sentiment (e.g., "Positive," "Neutral," "Negative") of the last user response.
* **Multilingual Support:** The system prompt could be modified to include: "First, detect the user's language. Then, conduct the entire conversation in that language."
* **UI Enhancements:** Using `st.columns` to structure the layout, adding a company logo with `st.image`, and applying custom CSS to improve the visual appeal.