import requests
import utils
from flask import Flask, render_template, request
from flask_ngrok import run_with_ngrok
from numpy import concatenate
from pandas import concat
from pyngrok import ngrok
from twilio.twiml.messaging_response import MessagingResponse

#https://www.twilio.com/blog/build-a-sms-chatbot-with-python-flask-and-twilio

# Create a Flask app
app = Flask(__name__)
run_with_ngrok(app)

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
    found = utils.check_sent_messages(incoming_msg)
    if found:
        final_body = "\n\n: \n\nConsumerBot: I will send a message on Reddit to the author of post ID, " + '"' + found['id'] + '".'
    else:
        final_body = '\n\n: \n\nConsumerBot: I did not find any posts matching post ID, ' + '"' + incoming_msg + '".' + ' It might not be saved or it was deleted.'

    resp = MessagingResponse() 
    msg = resp.message()
    msg.body(final_body)
    print(final_body)

    return str(resp)


# Start the web server when this file runs
# also run ngrok http 5000
if __name__ == "__main__":
    app.run()