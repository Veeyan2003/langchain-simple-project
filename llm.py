from dotenv import load_dotenv
import os
import firebase_admin 
from firebase_admin import credentials, firestore
from google.cloud.firestore import Client as FirestoreClient
from google.cloud.firestore import SERVER_TIMESTAMP
from langchain_core.messages import BaseMessage
SERVICE_ACCOUNT_PATH=r"C:\Users\david\langchain\langchain-c26af-firebase-adminsdk-fbsvc-a4ab06d55f.json"

YOUR_PROJECT_ID ="langchain-c26af"

# --- CONFIGURATION ---
COLLECTION_NAME = "ManualChatSessions"
DOCUMENT_ID = "user-session-manual-test" 
# ---------------------


def save_chat_history(history: list[BaseMessage]):
    """Saves the current list of LangChain messages to a Firestore document."""
    
    # 1. Convert LangChain message objects to simple dictionaries (Firestore-friendly format)
    # The .to_json() method converts the message objects (SystemMessage, HumanMessage, etc.) 
    # into a string containing the content and type, which is safe to save.
    serializable_history = [m.to_json() for m in history]
    
    data_to_save = {
        "history": serializable_history,
        "last_updated": SERVER_TIMESTAMP,
        "session_id": DOCUMENT_ID
    }
    
    try:
        # 2. Write the data to your live database
        db.collection(COLLECTION_NAME).document(DOCUMENT_ID).set(data_to_save)
        # print(f"DEBUG: History saved to Firestore.")
    except Exception as e:
        print(f"❌ ERROR saving history to Firestore: {e}")

from langchain_core.messages import message_to_dict, messages_from_dict

def load_chat_history():
    """Loads the message history list from a Firestore document."""
    try:
        # 1. Retrieve the document from Firestore
        doc_ref = db.collection(COLLECTION_NAME).document(DOCUMENT_ID)
        doc = doc_ref.get()
        
        if doc.exists:
            data = doc.to_dict()
            serializable_history = data.get("history", [])
            
            # 2. Convert simple dictionaries back into LangChain message objects
            # messages_from_dict handles the conversion back to SystemMessage, HumanMessage, etc.
            history_list = messages_from_dict(serializable_history)
            print(f"✅ History loaded from Firestore ({len(history_list)} messages).")
            return history_list
        else:
            print("⚠️ No previous session found in Firestore. Starting new session.")
            return []
    except Exception as e:
        print(f"❌ ERROR loading history: {e}")
        return []

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

load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage,AIMessage,HumanMessage

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    temperature=0,
    google_api_key=os.getenv("GEMINI_API_KEY") 
)

chart_history=load_chat_history()



if not chart_history:
    chart_history.append(SystemMessage(content="You are an helpful assistant"))
    print("System message added to history.")




while True:
    mess=input("You:")
    if mess=="0":
        save_chat_history(chart_history)
        print("Session has ended history has been saved ")
        break
    chart_history.append(HumanMessage(content=mess))
    result=llm.invoke(chart_history)
    print(f"GPT:{result.content}")
    result_save=AIMessage(content=result.content)
    chart_history.append(result_save)
    save_chat_history(chart_history)



