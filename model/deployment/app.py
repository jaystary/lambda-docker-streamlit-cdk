import os
import fcntl

path = '/mnt/data/msg'

def lambdaHandler(event, context):
    input = event.get('body')
    try:
        add_data(input)        
        data = get_data()
    except Exception as e:
        print(str(e))
        return {'body': str(e), 'statusCode': 500}    
    
    return {'body': data, 'statusCode': 200}
   
def add_data(input):
    with open(path, 'a') as file:
        fcntl.flock(file, fcntl.LOCK_EX)
        file.write(input+ "\n")
        fcntl.flock(file, fcntl.LOCK_UN)
        
def get_data():
    try:
        with open(path, 'r') as file:
            fcntl.flock(file, fcntl.LOCK_SH)
            data = file.read()
            fcntl.flock(file, fcntl.LOCK_UN)
    except:
        data = 'No message yet.'
    return data