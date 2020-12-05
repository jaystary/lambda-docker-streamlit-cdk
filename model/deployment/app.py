import os
import fcntl
import datetime

path = '/mnt/data/msg'

def lambdaHandler(event, context):
    method = event['requestContext']['http']['method']
    input = event.get('body')
    dt_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if method == 'POST':        
        if input is None:
            input = "No Input"
        input = f'{dt_str}: {input}'
        print(input)
        
        try:
            add_data(input)        
            data = get_data()
        except Exception as e:
            print(str(e))
            return {'body': str(e), 'statusCode': 500}    
        
        return {'body': data, 'statusCode': 200}
    
    if method == 'GET':
        return {'body': get_data(), 'statusCode': 200}

"""Reading and Writing to mounted EFS example"""
def add_data(input):
    with open(path, 'a') as file:
        fcntl.flock(file, fcntl.LOCK_EX)
        file.write(str(input)+ "\n")
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