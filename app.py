
#----------------------------------------------------------------------------------------------------  
#----------------------------------------
#-------------------------------
#---------------------
#--------------
#######code for input taken
#------

#from pymongo import MongoClient
#from datetime import datetime
#import speech_recognition as sr

# MongoDB Configuration
#MONGO_URI = st.secrets["MONGO_URI"]
#client = MongoClient(MONGO_URI)
#db = client["GroceryStore"]
#collection = db["SalesRecords"]

#
import streamlit as st
import speech_recognition as sr
import re

# Function to parse the text and extract item description and price
def parse_message(text):
    # Improved regex to handle 'of', 'for', and 'to' as valid separators
    match = re.search(r'(\d+|one|two|three|four|five|six|seven|eight|nine|ten)\s+([a-zA-Z\s]+)\s+(of|for|to)\s+(\d+)\s*(rupees)?', text, re.IGNORECASE)
    
    if match:
        quantity_text = match.group(1)
        description = match.group(2).strip()
        price = match.group(4)
        
        # Handling for words like "one", "two", etc.
        quantity_dict = {
            'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
            'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10
        }

        # Convert quantity text to integer if it's a word, otherwise keep the numeric value
        quantity = quantity_dict.get(quantity_text.lower(), quantity_text)
        
        return quantity, description, price
    else:
        return None, None, None


# Function to convert voice input to text
def transcribe_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening for your input...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)  # Listen for the audio
        st.write("Got it! Now transcribing...")

    try:
        # Recognize speech using Google's API
        text = recognizer.recognize_google(audio)
        st.write(f"Recognized Text: {text}")
        return text
    except sr.UnknownValueError:
        st.error("Sorry, I couldn't understand the audio. Please try again.")
        return None
    except sr.RequestError:
        st.error("Could not request results from Google Speech Recognition service.")
        return None


# Streamlit UI
st.title("Voice Input to Item Description Parser")
st.write("Speak your input clearly, and the system will process it automatically.")

# Listen for the voice input
text = transcribe_audio()

if text:
    # Parse the transcribed text
    quantity, description, price = parse_message(text)
    
    if quantity and description and price:
        st.write(f"Quantity: {quantity}")
        st.write(f"Description: {description}")
        st.write(f"Price: {price} Rupees")
    else:
        st.error("Could not parse the message correctly. Please try again.")



