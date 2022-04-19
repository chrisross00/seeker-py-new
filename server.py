from flask import Flask, render_template, request
from numpy import concatenate
from pandas import concat
import requests
from twilio.twiml.messaging_response import MessagingResponse

#https://www.twilio.com/blog/build-a-sms-chatbot-with-python-flask-and-twilio


# Create a Flask app
app = Flask(__name__)

# Create a route that just returns "In progress"
@app.route("/")
def serve_homepage():
    return "In progress!"

@app.route("/sms", methods=['POST'])
def handle_incoming_msg():
    incoming_msg = request.values.get('Body', '').lower() #store the body of the message into a variable
    
    # send the incoming message to something to the app server to analyze how to handle the message
    print(incoming_msg)

    # handle response from app server

    # send response to user
    resp = MessagingResponse() 
    msg = resp.message()
    final_body = "\nWhat's up it's Chris and Bentles from your computer hanging out at localhost:5000/sms. You just sent me this message, " + '"' + incoming_msg + '".'
    msg.body(final_body)

    return str(resp)


# Start the server when this file runs
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)