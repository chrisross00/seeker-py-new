from time import time
import utils
import twilio
from dateutil import parser 
from datetime import datetime
from twilio.rest import Client

class Twilio:
    def __init__(self):
        auth_config = utils.get_twilio_instance_parameters()
        self.twilio = Client(auth_config["TWILIO_ACCOUNT_SID"], auth_config["TWILIO_AUTH_TOKEN"])
        self.from_number = auth_config["TWILIO_FROM_NUMBER"]
        self.to_number = auth_config["TWILIO_TO_NUMBER"]
        self.message = self.Message(self)

    test_to_number = 1

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
                
                message = '\n\nNew post found\n\nTitle: "' + str(message_parts_list[i]['title']) + '".\n\nPosted ' + time_ago + '\n\nURL: ' + message_parts_list[i]['url'] + '\n\nTo comment on the post and PM the author, reply with the ID: ' + str(message_parts_list[i]['id'])
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
                            'id': final_results[i]['search_results'][0]['result_id']
                        })
            return self.message_parts
        
        def store_messages(self):
            messages = utils.open_db(utils.prop('message_db.open_path'))
            messages['messages'].append(self.message_parts)
            utils.save_db(messages, utils.prop('message_db.save_path'))
            return

        def review_ids(self, outside_id):
            m = utils.open_db(utils.prop('message_db.open_path'))
            results = []
            
            for i in range(len(m['messages'])):
                for j in range (len(m['messages'][i])):
                    if m['messages'][i][j]['id'] == outside_id:
                        results.append({
                            'id': m['messages'][i][j]['id']
                        })

            #twilio.message.message_parts[0]['id'] #wherever you do this, this is basically how you get to the ids on the message object once message_parts is set
            return results