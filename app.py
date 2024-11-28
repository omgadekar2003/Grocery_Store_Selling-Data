
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

# Function to recognize speech from audio input
def recognize_speech(audio_data):
    recognizer = sr.Recognizer()

    # Convert audio data to text using SpeechRecognition
    with sr.AudioFile(audio_data) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Sorry, I could not understand the audio."
        except sr.RequestError:
            return "Sorry, there was an error with the speech recognition service."

# Function to parse the text and extract item description and price
def parse_message(text):
    # Regular expression to extract the item and price (assuming 'rupees' after price)
    match = re.search(r'(\d+)\s+(.*)\s+of\s+(\d+)\s+rupees', text)
    if match:
        quantity = match.group(1)
        description = match.group(2)
        price = match.group(3)
        return quantity, description, price
    else:
        return None, None, None

# Streamlit UI for audio input
audio_value = st.audio_input("Record a voice message")

if audio_value:
    # Convert audio to text
    text = recognize_speech(audio_value)

    if text:
        # Display the recognized text
        st.write(f"Recognized Text: {text}")

        # Parse the text for quantity, description, and price
        quantity, description, price = parse_message(text)

        if quantity and description and price:
            # Display parsed information
            st.write(f"Quantity: {quantity}")
            st.write(f"Description: {description}")
            st.write(f"Price: {price} Rupees")
        else:
            st.write("Could not parse the message correctly. Please try again.")


