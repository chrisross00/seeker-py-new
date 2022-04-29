import os
import requests
import utils
import time
from dateutil import parser 
import calendar
import datetime
from models.base import db
from twilio.rest import Client

# ==================================================================
# Database table definitions
# ==================================================================

class Message(db.Model): 
    __tablename__ = "Message"

    id = db.Column(db.Integer, primary_key=True)
    message_body = db.Column(db.String(2000), nullable=True)
    status = db.Column(db.Integer, nullable=False)
    search_query = db.Column(db.String(100),nullable=False)
    scraped_title = db.Column(db.String(100), nullable=False)
    datediff_total_seconds = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String(200), nullable=False)
    result_id = db.Column(db.String, nullable=False)
    user_replied = db.Column(db.Integer, nullable=True)

    # Create a string
    def __repr__(self):
        return '<id %r>' % self.id

# class MessageReply(db.Model):
#     __tablename__ = "MessageReply"
#     id =
#     message_body =


    # add messageREply table to model
## Steps 
    # Server gets response and pulls method from MessageModel to insert the reply as a MessageReply
        # Analyze the request.values object on server.py and see if it has anything distinct I can pull off
    # That method should pass the message to Reddit
    # Reddit uses result_id to look up the author and keyword? to build a message to the author
        # Send message to author
        # comment on original submission with "Pm"

    # alternative, could send a link with a randomized token on it, taking user to an API that uses the token to send the message to the reddit user
        # removes need for inbound SMS handling, keeps Twilio cost down
        # doesn't build out any SMS-command based functionality that I could reuse later
        # Does make it easier for the user to "reply" - typing the request_id is burdensome; could be replaced with a number/unique_id, but a link will always be easier
        


# ==================================================================
# Message related functions definition
# ==================================================================

def add_result(result):
    # check if unique first
    unique_messages = Message.query.filter_by(result_id=result.result_id).all()
    if unique_messages:
        return
    else:
        # do some date time math
        d = datetime.datetime.utcnow()
        utc_time = calendar.timegm(d.utctimetuple())

        datediff_obj = utc_time - result.post_date_utc

        result = Message(
            status=0,
            scraped_title=str(result.title),
            datediff_total_seconds=datediff_obj,
            search_query=result.search_query,
            url=result.url,
            result_id=result.result_id,
            user_replied=0
        )
        db.session.add(result)
        db.session.commit()
        return result

def handle_incoming_message(outside_id):
    m_id = Message.query.filter_by(result_id=outside_id).first()
    if m_id: # if the outside id matches a result_id in the Message table, it's a reply
        result = {'id': outside_id}
        m_id.user_replied = 1
        db.session.add(m_id)
        # kick off some reddit reply process
    else:
        result = False
    
    db.session.commit()
    return result

# ==================================================================
# App object definition
# ==================================================================

class Twilio:
    #https://www.twilio.com/docs/phone-numbers/api/incomingphonenumber-resource#read-multiple-incomingphonenumber-resources
    def __init__(self):
        self.twilio = Client(os.environ.get("TWILIO_ACCOUNT_SID", None), os.environ.get("TWILIO_AUTH_TOKEN", None))
        self.from_number = os.environ.get("TWILIO_FROM_NUMBER", None)
        self.to_number = os.environ.get("TWILIO_TO_NUMBER", None)
        self.message = self.Twilio_Message(self)
        self.ph_sid = self.get_phone_sid()
        self.webhook_url = self.twilio.api.incoming_phone_numbers(self.ph_sid).fetch()._properties['sms_url']
        self.ngrok_url = self.get_ngrok_url()

    def get_phone_sid(self):
        nums = self.twilio.incoming_phone_numbers.list() 
        for x in nums:
            self.ph_sid = x.sid
        return x.sid

    def get_ngrok_url(self):
        # get the ngrok public_url once the server is up
        # will fail if server is down - don't want to build handling rn
        local_url = os.environ.get("NGROK_LOCAL_URL", None)
        if os.environ.get('NGROK_LOCAL_URL', None): # if lower env, do this stuff
            response = requests.get(local_url)
            while response.status_code != 200:
                time.sleep(5)
                print('\nRetrying local endpoint...')
                response = requests.get(local_url)
            # print(f'\nDone! Got status code of {response.status_code}')
            data = response.json()
            ngrok_url = data['tunnels'][0]['public_url']
            self.ngrok_url = ngrok_url+'/sms'

            if ngrok_url != self.webhook_url:
                # print(f'\nCaught in IF: updating the webhook url from {self.webhook_url} to {ngrok_url}')
                self.update_webhook_url(self.ngrok_url)

        else: # otherwise, in prod, so there is no ngrok
            self.ngrok_url = None
            prod_sms_url = os.environ.get("TWILIO_WEBHOOK_URL", None)
            self.update_webhook_url(prod_sms_url)

        return ngrok_url
        
    def update_webhook_url(self, target_url):
        self.twilio.api.incoming_phone_numbers(self.ph_sid).update(sms_url=target_url)
        self.webhook_url = self.twilio.api.incoming_phone_numbers(self.ph_sid).fetch()._properties['sms_url']

    class Twilio_Message:
        def __init__(self, twilio):
            self.from_number = twilio.from_number
            self.to_number = twilio.to_number
            self.messages = twilio.twilio.messages
            self.messaging = twilio.twilio.messaging
            self.message_parts = []
            self.message_list = []

        def build_message(self): # Rewritten!
            #build body with message_parts_list
            messages = Message.query.filter_by(message_body=None).all()

            for message_parts in messages:
                s_ago = message_parts.datediff_total_seconds

                if s_ago < 86400:
                    if s_ago > 5400: #if greater than 1.5h ago, but less than a day, put it in hours
                        t = round(s_ago/3600)
                        t = str(t)
                        time_ago = t + ' hours ago'
                    elif 120 <= s_ago <= 5400: #if less than 1.5h ago, put it in minutes
                        t = round(s_ago/60)
                        t = str(t)
                        time_ago = t +' minutes ago' 
                    elif 60 <= s_ago < 120:
                        time_ago = 'about a minute ago'
                    elif s_ago < 60:
                        t = round(s_ago)
                        t = str(t)
                        time_ago = t + ' seconds ago'
                else:
                    t = round(s_ago/86400)
                    t = str(t)
                    time_ago = t + ' days ago'
                
                message = '\n\n: \n\nNew post found!\n\nQuery: ' + message_parts.search_query + '\n\nTitle: "' + message_parts.scraped_title + '".\n\nPosted ' + time_ago + '\n\nURL: ' + message_parts.url + '\n\nTo comment on the post and PM the author, reply with the ID: ' + message_parts.result_id
                message_parts.message_body = message
                db.session.add(message_parts)
            db.session.commit()
            return 

        def send_message(self): 
            messages = Message.query.filter_by(status=0).all()
            for message in messages:
                self.messages.create(body=message.message_body,from_=self.from_number,to=self.to_number)
                message.status = 1
                db.session.add(message)
            db.session.commit()
            return

        def insert_test_messsage(self): 
            Message.query.filter_by(result_id='test123').delete()
            result = Message(
                status=0,
                scraped_title='test title',
                datediff_total_seconds=1,
                search_query='test',
                url='test_url',
                result_id='test123',
                user_replied=0
            )
            db.session.add(result)
            db.session.commit()
            return