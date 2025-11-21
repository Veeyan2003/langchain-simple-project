# langchain-simple-project
A basic interactive chat window on the command line built using python script using lanchain functions and firebase database to store chat history 
# 🔥 LangChain Manual Persistence Masterpiece (Gemini + Firestore)

This project demonstrates the core principle of **persistent LLM memory** by manually managing the conversation history and storing it directly in a **live Google Firebase Firestore database**. This is the fundamental architecture that automated LangChain Memory tools abstract away.

## 🚀 Mastery Concepts Demonstrated

* **Manual Persistence:** Implementing the full **Save/Load** cycle for chat history without using LangChain's built-in `ConversationBufferMemory`.
* **Serialization:** Converting complex LangChain `BaseMessage` objects (`HumanMessage`, `AIMessage`) into simple JSON/dictionary formats that are safe to store in Firestore.
* **External Integration:** Connecting to a live cloud database (Firestore) using the secure Firebase Admin SDK.
* **LLM Connection:** Using the newest `langchain-google-genai` package with the free **Gemini 2.5 Flash** model.

## 🛠️ Setup Guide

Follow these steps to run the application and connect it to your own Firebase project.

### Step 1: Clone and Install Dependencies

1.  Clone this repository: `git clone [repository-url]`
2.  Navigate to the directory: `cd [repository-name]`
3.  Create and activate a virtual environment:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use .venv\Scripts\activate
    ```
4.  Install the required Python packages:
    ```bash
    pip install langchain-google-genai firebase-admin python-dotenv langchain-core google-cloud-firestore
    ```
That's a fantastic idea! Turning your working code into a sharable GitHub project demonstrates not only coding mastery but also professional best practices.

Since you've mastered the Firebase persistence with your current script, the goal now is to package this code with the necessary documentation so others can run it easily.

Here is the final, organized script and the contents of a professional README.md file.

📁 Project Structure
Create these three files in your project directory:

/langchain-mastery-project
├── app.py 
├── .env           (For storing the GEMINI_API_KEY)
└── README.md      (The setup instructions)
🐍 1. app.py (The Final Script)
This is your complete, working script with minor structural improvements (all imports moved to the top, which is best practice).

Python

import os
from dotenv import load_dotenv
import firebase_admin 
from firebase_admin import credentials, firestore
from google.cloud.firestore import Client as FirestoreClient
from google.cloud.firestore import SERVER_TIMESTAMP
from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict, SystemMessage, AIMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# --- 1. CONFIGURATION AND AUTHENTICATION ---

# NOTE: REPLACE THESE WITH YOUR ACTUAL PATH/ID
SERVICE_ACCOUNT_PATH = r"C:\Users\david\langchain\langchain-c26af-firebase-adminsdk-fbsvc-a4ab06d55f.json"
YOUR_PROJECT_ID = "langchain-c26af"

# Firestore database configuration
COLLECTION_NAME = "ManualChatSessions"
DOCUMENT_ID = "user-session-manual-test" 

# Firebase Admin SDK Initialization
try:
    cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
    firebase_admin.initialize_app(cred, {'projectId': YOUR_PROJECT_ID})
    print("✅ Firebase Admin SDK Initialized.")
except ValueError:
    print("✅ Firebase Admin SDK already running.")
    pass
except FileNotFoundError:
    print(f"❌ ERROR: Service Account Key not found at {SERVICE_ACCOUNT_PATH}")
    exit()

db = firestore.client() 
print("✅ Firestore Client created successfully.")

# Load environment variables (for GEMINI_API_KEY)
load_dotenv()

# --- 2. FIREBASE I/O FUNCTIONS ---

def save_chat_history(history: list[BaseMessage]):
    """Saves the current list of LangChain messages to a Firestore document."""
    
    # Serialization: Convert complex objects to simple dictionaries/strings for Firestore
    serializable_history = [m.to_json() for m in history]
    
    data_to_save = {
        "history": serializable_history,
        "last_updated": SERVER_TIMESTAMP,
        "session_id": DOCUMENT_ID
    }
    
    try:
        # Write the data to your live database
        db.collection(COLLECTION_NAME).document(DOCUMENT_ID).set(data_to_save)
    except Exception as e:
        print(f"❌ ERROR saving history to Firestore: {e}")

def load_chat_history():
    """Loads the message history list from a Firestore document."""
    try:
        doc_ref = db.collection(COLLECTION_NAME).document(DOCUMENT_ID)
        doc = doc_ref.get()
        
        if doc.exists:
            data = doc.to_dict()
            serializable_history = data.get("history", [])
            
            # Deserialization: Convert simple dictionaries back into LangChain message objects
            history_list = messages_from_dict(serializable_history)
            print(f"✅ History loaded from Firestore ({len(history_list)} messages).")
            return history_list
        else:
            print("⚠️ No previous session found. Starting new session.")
            return []
    except Exception as e:
        print(f"❌ ERROR loading history: {e}")
        return []

# --- 3. LLM INITIALIZATION AND MAIN LOOP ---

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    temperature=0,
    google_api_key=os.getenv("GEMINI_API_KEY") 
)

# Load history from Firebase at startup
chart_history = load_chat_history()

# Ensure System Message is present if history was empty
if not chart_history or chart_history[0].type != "system":
    chart_history.insert(0, SystemMessage(content="You are an helpful assistant"))
    print("System message ensured at start of history.")

print("--- Live Firestore Chat Started (Type '0' to exit) ---")

while True:
    mess=input("You:")
    if mess=="0":
        save_chat_history(chart_history)
        print("Session has ended. History has been saved to Firebase.")
        break
    
    # 1. Append Human Message
    chart_history.append(HumanMessage(content=mess))
    
    # 2. Invoke LLM and get response
    result=llm.invoke(chart_history)
    
    print(f"GPT:{result.content}")
    
    # 3. Append AI Message (Crucial for Memory)
    result_save=AIMessage(content=result.content)
    chart_history.append(result_save)
    
    # 4. Save History (Persistence)
    save_chat_history(chart_history)
📝 2. README.md (Setup Instructions)
This file tells others how to set up the necessary credentials (the hardest part).

Markdown

# 🔥 LangChain Manual Persistence Masterpiece (Gemini + Firestore)

This project demonstrates the core principle of **persistent LLM memory** by manually managing the conversation history and storing it directly in a **live Google Firebase Firestore database**. This is the fundamental architecture that automated LangChain Memory tools abstract away.

## 🚀 Mastery Concepts Demonstrated

* **Manual Persistence:** Implementing the full **Save/Load** cycle for chat history without using LangChain's built-in `ConversationBufferMemory`.
* **Serialization:** Converting complex LangChain `BaseMessage` objects (`HumanMessage`, `AIMessage`) into simple JSON/dictionary formats that are safe to store in Firestore.
* **External Integration:** Connecting to a live cloud database (Firestore) using the secure Firebase Admin SDK.
* **LLM Connection:** Using the newest `langchain-google-genai` package with the free **Gemini 2.5 Flash** model.

## 🛠️ Setup Guide

Follow these steps to run the application and connect it to your own Firebase project.

### Step 1: Clone and Install Dependencies

1.  Clone this repository: `git clone [repository-url]`
2.  Navigate to the directory: `cd [repository-name]`
3.  Create and activate a virtual environment:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use .venv\Scripts\activate
    ```
4.  Install the required Python packages:
    ```bash
    pip install langchain-google-genai firebase-admin python-dotenv langchain-core google-cloud-firestore
    ```

### Step 2: Configure API Keys (.env)

Create a file named **`.env`** in the root directory and add your Gemini API Key:

GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"


### Step 3: Firebase Firestore Setup (CRITICAL)

This project connects to a live database and requires secure credentials.

1.  **Create Firebase Project:** Go to the [Firebase Console](https://console.firebase.google.com/) and create a new project.
2.  **Enable Firestore:** Under the "Build" section, enable the Firestore Database (start in **Test Mode** for easy setup).
3.  **Generate Service Account Key:**
    * Go to **Project settings** (gear icon next to "Project Overview").
    * Go to the **Service accounts** tab.
    * Click **Generate new private key** and download the JSON file. **SAVE THIS FILE SECURELY.**

### Step 4: Update Authentication Path

Open `app.py` and **update the two lines** at the very top of the script with your specific details:

```python
# 1. Update the path to your downloaded JSON file.
SERVICE_ACCOUNT_PATH = r"path/to/your/serviceAccountKey.json" 

# 2. Update the project ID (found in Project Settings -> General)
YOUR_PROJECT_ID = "your-firebase-project-id"
### Step 2: Configure API Keys (.env)

Create a file named **`.env`** in the root directory and add your Gemini API Key:
