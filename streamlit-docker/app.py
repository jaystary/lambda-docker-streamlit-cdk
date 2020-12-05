import streamlit as st
import fcntl
import os

#Mount path
path = '/mnt/data/msg'

def add_message():
    with open(path, 'a') as file:
        fcntl.flock(file, fcntl.LOCK_EX)
        file.write("test"+ "\n")
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

st.title("Streamlit Container")
#API Gateway URL that can use all Methods (Post/Get/Patch ...)
st.write("API GW URL: " os.environ['API_URL'])

#Demonstrate EFS Mount
add_message()        
messages = get_messages()
st.write(messages)

