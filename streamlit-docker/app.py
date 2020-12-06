import streamlit as st
import fcntl
import os
import requests
import datetime
  
#Mount path
path = '/mnt/data/msg'

dt_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.title("Streamlit Container")

#API Gateway URL that can use all Methods (Post/Get/Delete ...)
st.write("API URL: " +os.environ['API_URL'])

#API connection:
post_api_request(f'{dt_str}: Hi from Streamlit')

#Demonstrate EFS Mount
add_message()        
messages = get_messages()
st.write(messages)

def add_message(payload):
    with open(path, 'a') as file:
        fcntl.flock(file, fcntl.LOCK_EX)
        file.write(payload+ "\n")
        fcntl.flock(file, fcntl.LOCK_UN)
        
def get_messages():
    try:
        with open(path, 'r') as file:
            fcntl.flock(file, fcntl.LOCK_SH)
            messages = file.read()
            fcntl.flock(file, fcntl.LOCK_UN)
    except:
        messages = 'No message yet.'
    return messages

def post_api_request(payload):
    #Exposed at stack creation
    url = os.environ['API_URL']

    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data = payload)
    st.write(response.text.encode('utf8'))
    
