import requests
import utils
import time
from dateutil import parser 
from datetime import datetime
from twilio.rest import Client

class Twilio:
    #https://www.twilio.com/docs/phone-numbers/api/incomingphonenumber-resource#read-multiple-incomingphonenumber-resources
    def __init__(self):
        auth_config = utils.get_auth_config_parameters()
        self.twilio = Client(auth_config["TWILIO_ACCOUNT_SID"], auth_config["TWILIO_AUTH_TOKEN"])
        self.from_number = auth_config["TWILIO_FROM_NUMBER"]
        self.to_number = auth_config["TWILIO_TO_NUMBER"]
        self.message = self.Message(self)
        self.ph_sid = self.get_phone_sid()
        print(f'self.ph_sid, {self.ph_sid}')
        self.webhook_url = self.twilio.api.incoming_phone_numbers(self.ph_sid).fetch()._properties['sms_url']
        self.ngrok_url = self.get_ngrok_url()

    def get_phone_sid(self):
        print('get_phone_sid hit', self.twilio)
        nums = self.twilio.incoming_phone_numbers.list() 
        print('nums hit', nums)
        for x in nums:
            print(f"x, {x.sid}")
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
        print(f'\nDone! Got status code of {response.status_code}')
        data = response.json()
        ngrok_url = data['tunnels'][0]['public_url']
        self.ngrok_url = ngrok_url

        if ngrok_url != self.webhook_url:
            print(f'\nCaught in IF: updating the webhook url from {self.webhook_url} to {ngrok_url}')
            self.update_webhook_url(self.ngrok_url)

        return ngrok_url
        
    def update_webhook_url(self, target_url):
        self.twilio.api.incoming_phone_numbers(self.ph_sid).update(sms_url=target_url)
        print(f'\nUpdate_webhook_url: received request to update webhook url from {self.webhook_url} to {target_url}')
        self.webhook_url = self.twilio.api.incoming_phone_numbers(self.ph_sid).fetch()._properties['sms_url']

    class Message:
        def __init__(self, twilio):
            self.from_number = twilio.from_number
            self.to_number = twilio.to_number
            self.messages = twilio.twilio.messages
            self.messaging = twilio.twilio.messaging
            self.message_parts = []
            self.message_list = []

        def build_message(self, message_parts_list):
            #build body with message_parts_list
            for i in range(len(message_parts_list)):
                # day in s = 86400
                s_ago = message_parts_list[i]['datediff_total_seconds']

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
                
                message = '\n\n: \n\nNew post found!\n\nQuery: ' + message_parts_list[i]['query'] + '\n\nTitle: "' + str(message_parts_list[i]['title']) + '".\n\nPosted ' + time_ago + '\n\nURL: ' + message_parts_list[i]['url'] + '\n\nTo comment on the post and PM the author, reply with the ID: ' + str(message_parts_list[i]['id'])
                self.message_list.append(message)

            return self.message_list

        def send_message(self,body):
            #build body with message_parts_list
            for b in body:
                self.messages.create(body=b,from_=self.from_number,to=self.to_number)

        def parse_results(self, final_results):
            current_time = parser.parse(str(datetime.now()))
            for i in range(len(final_results)):
                for j in range(len(final_results[i]['search_results'])):
                    datediff_obj = current_time - parser.parse(str(final_results[i]['search_results'][j]['body']['created_date_local']))
                    self.message_parts.append(
                        {
                            'title': str(final_results[i]['search_results'][j]['body']['title']),
                            'datediff_total_seconds': datediff_obj.total_seconds(),
                            'datediff_days' : datediff_obj.days,
                            'datediff_seconds' : datediff_obj.seconds,
                            'url': final_results[i]['search_results'][j]['body']['url'],
                            'id': final_results[i]['search_results'][0]['result_id'],
                            'query': final_results[i]['search_parameters']['query'],
                            'status':0
                        })
            return self.message_parts #could just add the full message as another key in the message_parts object
        
        def store_messages(self):
            messages = utils.open_db(utils.prop('message_db.open_path'))
            messages['messages'].append(self.message_parts)
            utils.save_db(messages, utils.prop('message_db.save_path'))
            return

