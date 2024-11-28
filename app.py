# import streamlit as st
# from pymongo import MongoClient
# import speech_recognition as sr
# from datetime import datetime, timedelta

# # MongoDB Atlas connection
# MONGO_URI = st.secrets["MONGO_URI"]
# client = MongoClient(MONGO_URI)
# db = client["GroceryStore"]
# collection = db["SalesRecords"]

# # Utility: Speech recognition
# def get_voice_input():
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         st.info("Listening... Speak now!")
#         try:
#             audio = recognizer.listen(source, timeout=5)
#             text = recognizer.recognize_google(audio)
#             return text
#         except sr.UnknownValueError:
#             st.error("Sorry, I could not understand the audio.")
#         except sr.RequestError:
#             st.error("Network error. Please check your connection.")
#     return None

# # Utility: Add a record to MongoDB
# def add_record(description, amount):
#     record = {
#         "date": datetime.now(),
#         "description": description,
#         "amount": amount,
#     }
#     collection.insert_one(record)

# # Utility: Fetch sales records
# def fetch_records(start_date=None, end_date=None):
#     query = {}
#     if start_date and end_date:
#         query["date"] = {"$gte": start_date, "$lte": end_date}
#     return list(collection.find(query))

# # Streamlit UI
# st.sidebar.title("Grocery Store App")
# menu = st.sidebar.radio("Navigation", ["Home", "Add Today's Sell", "History", "About Us"])

# if menu == "Home":
#     st.title("Welcome to the Grocery Store App!")
#     st.write("This application will help you manage your store's sales effectively.")
#     st.write("Navigate using the menu to get started.")

# elif menu == "Add Today's Sell":
#     st.title("Add Today's Sell")
#     st.write("Use voice input to add sales records.")
    
#     if st.button("Record Voice Input"):
#         voice_text = get_voice_input()
#         if voice_text:
#             st.success(f"Detected: {voice_text}")
#             # Parse the text (basic implementation; can be enhanced with NLP)
#             st.write("Split the text into description and amount.")
#             description = st.text_input("Description", value="Item description here")
#             amount = st.number_input("Amount", min_value=0.0)
#             if st.button("Add Record"):
#                 add_record(description, amount)
#                 st.success("Record added successfully!")

#     st.subheader("Sales Summary for Today")
#     today = datetime.now().date()
#     records = fetch_records(start_date=today, end_date=today + timedelta(days=1))
#     if records:
#         for i, record in enumerate(records, 1):
#             st.write(f"{i}. {record['description']} - ₹{record['amount']}")

#         total = sum([record["amount"] for record in records])
#         st.write(f"**Total Sales: ₹{total}**")

# elif menu == "History":
#     st.title("Sales History")
#     st.write("View sales history by date range.")
#     start_date = st.date_input("Start Date", value=datetime.now().date() - timedelta(days=7))
#     end_date = st.date_input("End Date", value=datetime.now().date())
    
#     if st.button("Fetch History"):
#         records = fetch_records(start_date=datetime.combine(start_date, datetime.min.time()),
#                                 end_date=datetime.combine(end_date, datetime.max.time()))
#         if records:
#             for i, record in enumerate(records, 1):
#                 st.write(f"{i}. {record['description']} - ₹{record['amount']} on {record['date'].strftime('%Y-%m-%d %H:%M:%S')}")
#         else:
#             st.write("No records found for the selected date range.")

# elif menu == "About Us":
#     st.title("About Us")
#     st.write("This page will provide information about the application and its purpose.")
  
#------
#######code for input taken
#------
import streamlit as st
from pymongo import MongoClient
from datetime import datetime, timedelta
import tempfile

# MongoDB Atlas connection
MONGO_URI = st.secrets["MONGO_URI"]
client = MongoClient(MONGO_URI)
db = client["GroceryStore"]
collection = db["SalesRecords"]

# Utility: Add a record to MongoDB
def add_record(description, amount):
    record = {
        "date": datetime.now(),
        "description": description,
        "amount": amount,
    }
    collection.insert_one(record)

# Utility: Fetch sales records
def fetch_records(start_date=None, end_date=None):
    query = {}
    if start_date and end_date:
        query["date"] = {"$gte": start_date, "$lte": end_date}
    return list(collection.find(query))

# Streamlit UI
st.sidebar.title("Grocery Store App")
menu = st.sidebar.radio("Navigation", ["Home", "Add Today's Sell", "History", "About Us"])

if menu == "Home":
    st.title("Welcome to the Grocery Store App!")
    st.write("This application will help you manage your store's sales effectively.")
    st.write("Navigate using the menu to get started.")

elif menu == "Add Today's Sell":
    st.title("Add Today's Sell")
    st.write("Record a voice message and add sales records.")
    
    audio_value = st.audio_input("Record a voice message")
    
    if audio_value:
        # Save the audio file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
            temp_audio_file.write(audio_value)
            temp_audio_path = temp_audio_file.name

        st.success(f"Audio recorded and saved temporarily at: {temp_audio_path}")
        st.audio(audio_value)

        # Placeholder: Process the audio file (you can integrate a speech-to-text solution here)
        # For now, ask the user for manual input
        st.write("Please manually input the description and amount based on your recording.")
        description = st.text_input("Description", value="Item description here")
        amount = st.number_input("Amount", min_value=0.0)
        
        if st.button("Add Record"):
            add_record(description, amount)
            st.success("Record added successfully!")

    st.subheader("Sales Summary for Today")
    today = datetime.now().date()
    records = fetch_records(start_date=today, end_date=today + timedelta(days=1))
    if records:
        for i, record in enumerate(records, 1):
            st.write(f"{i}. {record['description']} - ₹{record['amount']}")

        total = sum([record["amount"] for record in records])
        st.write(f"**Total Sales: ₹{total}**")

elif menu == "History":
    st.title("Sales History")
    st.write("View sales history by date range.")
    start_date = st.date_input("Start Date", value=datetime.now().date() - timedelta(days=7))
    end_date = st.date_input("End Date", value=datetime.now().date())
    
    if st.button("Fetch History"):
        records = fetch_records(start_date=datetime.combine(start_date, datetime.min.time()),
                                end_date=datetime.combine(end_date, datetime.max.time()))
        if records:
            for i, record in enumerate(records, 1):
                st.write(f"{i}. {record['description']} - ₹{record['amount']} on {record['date'].strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            st.write("No records found for the selected date range.")

elif menu == "About Us":
    st.title("About Us")
    st.write("This page will provide information about the application and its purpose.")

