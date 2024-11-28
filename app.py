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
#*----------------------------------------------------------------------------------------------------  
#------
#######code for input taken
#------
# import streamlit as st
# from pymongo import MongoClient
# from datetime import datetime
# import speech_recognition as sr

# # Load MongoDB URI from secrets.toml
# MONGO_URI = st.secrets["MONGO_URI"]
# client = MongoClient(MONGO_URI)
# db = client["GroceryStore"]
# collection = db["SalesRecords"]

# # Function to save data to MongoDB
# def save_to_db(description, price, date):
#     record = {
#         "description": description,
#         "price": price,
#         "date": date
#     }
#     collection.insert_one(record)

# # Function to retrieve history
# def get_history(date_filter=None):
#     if date_filter:
#         records = list(collection.find({"date": {"$regex": date_filter}}))
#     else:
#         records = list(collection.find())
#     return records

# # Navigation
# menu = ["Home", "Sell Today", "History", "About Us"]
# choice = st.sidebar.selectbox("Navigation", menu)

# if choice == "Home":
#     st.title("Welcome to Grocery Store Sales Tracker!")
#     st.write("Navigate through the sidebar to record and view sales data.")
#     st.image("https://via.placeholder.com/400x200", caption="Your sales assistant!")

# elif choice == "Sell Today":
#     st.title("Sell Today")
#     st.write("Record your sales here.")

#     # Audio input
#     audio_recognizer = sr.Recognizer()
#     audio_value = st.audio_input("Record a voice message", type="wav")

#     if audio_value:
#         st.audio(audio_value)

#         with sr.AudioFile(audio_value) as source:
#             try:
#                 audio = audio_recognizer.record(source)
#                 transcript = audio_recognizer.recognize_google(audio)
#                 st.write(f"Detected Speech: {transcript}")

#                 # Parsing description and price
#                 parts = transcript.split("for")
#                 if len(parts) == 2:
#                     description = parts[0].strip()
#                     price = parts[1].strip()
#                     st.write(f"Description: {description}")
#                     st.write(f"Price: {price}")

#                     # Save data
#                     today_date = datetime.now().strftime("%Y-%m-%d")
#                     save_to_db(description, price, today_date)
#                     st.success("Record saved successfully!")
#                 else:
#                     st.error("Could not parse description and price from your input.")
#             except Exception as e:
#                 st.error(f"Error processing audio: {e}")

# elif choice == "History":
#     st.title("Sales History")
#     filter_date = st.text_input("Enter a date (YYYY-MM-DD) to filter, or leave blank to view all records:")
#     records = get_history(filter_date)

#     if records:
#         for record in records:
#             st.write(f"**Date:** {record['date']}")
#             st.write(f"**Description:** {record['description']}")
#             st.write(f"**Price:** {record['price']}")
#             st.write("---")
#     else:
#         st.write("No records found.")

# elif choice == "About Us":
#     st.title("About Us")
#     st.write("""
#     Welcome to the Grocery Store Sales Tracker!
#     This app allows you to record daily sales through voice input and manage sales history.
#     """)

#----------------------------------------------------------------------------------------------------  
#----------------------------------------
#-------------------------------
#---------------------
#--------------
#######code for input taken
#------

import streamlit as st
from pymongo import MongoClient
from datetime import datetime
import speech_recognition as sr

# MongoDB Configuration
MONGO_URI = st.secrets["MONGO_URI"]
client = MongoClient(MONGO_URI)
db = client["GroceryStore"]
collection = db["SalesRecords"]

# Function to save data to MongoDB
def save_to_db(description, price):
    record = {
        "description": description,
        "price": price,
        "date": datetime.now().strftime("%Y-%m-%d")
    }
    collection.insert_one(record)

# Streamlit App
st.title("Voice to Text Sales Recorder")
st.write("Upload your voice note to record sales information.")

# Audio input
audio_recognizer = sr.Recognizer()
audio_file = st.file_uploader("Upload a voice note (.wav format)", type=["wav"])

if audio_file:
    st.audio(audio_file)

    with sr.AudioFile(audio_file) as source:
        try:
            # Recognize audio using SpeechRecognition
            audio = audio_recognizer.record(source)
            transcript = audio_recognizer.recognize_google(audio)
            st.write(f"Detected Speech: {transcript}")

            # Parse description and price
            parts = transcript.split("for")
            if len(parts) == 2:
                description = parts[0].strip()
                price = parts[1].strip()
                st.write(f"Description: {description}")
                st.write(f"Price: {price}")

                # Save to MongoDB
                save_to_db(description, price)
                st.success("Record saved successfully!")
            else:
                st.error("Could not parse description and price from the audio input.")
        except Exception as e:
            st.error(f"Error processing audio: {e}")

