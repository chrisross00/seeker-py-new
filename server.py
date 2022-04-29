import os
from runmain import runmain, clean_up_db, test
from application import create_app
from flask import Flask, request
from flask_ngrok import run_with_ngrok
from twilio.twiml.messaging_response import MessagingResponse
from models.MessageModel import handle_incoming_message
from dotenv import load_dotenv

# Check and set environment
is_prod = os.environ.get('IS_HEROKU', None)

if os.environ.get('IS_HEROKU', None):
    print('we are in prod') #no need to set envs
else:
    load_dotenv()

#https://www.twilio.com/blog/build-a-sms-chatbot-with-python-flask-and-twilio
app = create_app()

# Create a route that just returns "In progress"
@app.route("/")
def serve_homepage():
    return "This is a home page!"

@app.route("/runmain") #will loop the app.py script while on thie page
def run_main():
    runmain()
    return "Testing Reddit to Twilio connection!"

@app.route("/test")
def run_test():
    test()
    return "Test script!"

@app.route("/clean") #will loop the app.py script while on thie page
def clean():
    clean_up_db()
    return "Cleaning the database!"

@app.route("/sms", methods=['POST'])
def handle_incoming_msg():
    incoming_msg = request.values.get('Body', '').lower() #store the body of the message into a variable
    # handle response from app server
    found = handle_incoming_message(incoming_msg)
    if found:
        final_body = "\n\n: \n\nConsumerBot: I will send a message on Reddit to the author of post ID, " + '"' + found['id'] + '".'
    else:
        final_body = '\n\n: \n\nConsumerBot: I did not find any posts matching post ID, ' + '"' + incoming_msg + '".' + ' It might not be saved or it was deleted.'

    resp = MessagingResponse() 
    msg = resp.message()
    msg.body(final_body)
    
    print(final_body) #somewhere in here, need to save the inbound-message?
    return str(resp)

# Start the web server when this file runs
# also run ngrok http 5000
if __name__ == "__main__":
    if os.environ.get('IS_HEROKU', None) is None:
        run_with_ngrok(app)
    app.run()