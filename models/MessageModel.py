import requests
import utils
import time
from dateutil import parser 
import calendar
import datetime
from models.base import db
from models.SearchModel import SearchResultDb
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
        auth_config = utils.get_auth_config_parameters()
        self.twilio = Client(auth_config["TWILIO_ACCOUNT_SID"], auth_config["TWILIO_AUTH_TOKEN"])
        self.from_number = auth_config["TWILIO_FROM_NUMBER"]
        self.to_number = auth_config["TWILIO_TO_NUMBER"]
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
        local_url = 'http://localhost:4040/api/tunnels'
        response = requests.get(local_url)
        while response.status_code != 200:
            time.sleep(5)
            print('\nWaited 5 s, retrying...')
            response = requests.get(local_url)
        # print(f'\nDone! Got status code of {response.status_code}')
        data = response.json()
        ngrok_url = data['tunnels'][0]['public_url']
        self.ngrok_url = ngrok_url+'/sms'

        if ngrok_url != self.webhook_url:
            # print(f'\nCaught in IF: updating the webhook url from {self.webhook_url} to {ngrok_url}')
            self.update_webhook_url(self.ngrok_url)

        return ngrok_url
        
    def update_webhook_url(self, target_url):
        self.twilio.api.incoming_phone_numbers(self.ph_sid).update(sms_url=target_url)
        # print(f'\nUpdate_webhook_url: received request to update webhook url from {self.webhook_url} to {target_url}')
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
                print('done building!!')
            db.session.commit()
            return 

        def send_message(self): #Rewritten!
            messages = Message.query.filter_by(status=0).all()
            for message in messages:
                self.messages.create(body=message.message_body,from_=self.from_number,to=self.to_number)
                message.status = 1
                db.session.add(message)
            db.session.commit()
            print('done sending messages')
            return