
#----------------------------------------------------------------------------------------------------  
#----------------------------------------
#-------------------------------
#---------------------
#--------------
#######code for input taken
#------
import streamlit as st
#from pymongo import MongoClient
#from datetime import datetime
#import speech_recognition as sr

# MongoDB Configuration
#MONGO_URI = st.secrets["MONGO_URI"]
#client = MongoClient(MONGO_URI)
#db = client["GroceryStore"]
#collection = db["SalesRecords"]

import streamlit as st

audio_value = st.audio_input("Record a voice message")

if audio_value:
    st.audio(audio_value)

