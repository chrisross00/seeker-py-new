import twilio
from twilio.rest import Client
import utils
from dateutil import parser 
from datetime import datetime

# https://www.twilio.com/blog/phone-verification-with-twilio-for-python-developers
# https://www.twilio.com/docs/sms/api/message-resource

class Message:
    def __init__(self, twilio):
        self.twilio = twilio.twilio
        self.from_number = twilio.from_number
        self.to_number = twilio.to_number

    def build_message(self, message_parts_list):
        body_list = []
        #build body with message_parts_list
        for i in range(len(message_parts_list)):
            # day in s = 86400
            days_ago = message_parts_list[i]['datediff_total_seconds']/86400
            days_around_round = round(days_ago)
            message = 'New post found with title: "' + str(message_parts_list[i]['title']) + '".\nThis was posted about ' + str(days_around_round) + ' days ago.\n\nUrl: ' + message_parts_list[i]['url'] + '\n\nTo comment on the post and PM the author, reply with the ID: ' + str(message_parts_list[i]['id'])
            body_list.append(message)

        return body_list

    def send_message(self,body):
        #build body with message_parts_list
        for b in body:
            self.twilio.messages.create(body=b,from_=self.from_number,to=self.to_number)

def parse_results(final_results):
    message_parts_list = []
    current_time = parser.parse(str(datetime.now()))
    for i in range(len(final_results)):
        for j in range(len(final_results[i]['search_results'])):
            datediff_obj = current_time - parser.parse(str(final_results[i]['search_results'][j]['body']['created_date_local']))
            message_parts_list.append(
                {
                    'title': str(final_results[i]['search_results'][j]['body']['title']),
                    'datediff_total_seconds': datediff_obj.total_seconds(),
                    'datediff_days' : datediff_obj.days,
                    'datediff_seconds' : datediff_obj.seconds,
                    'url': final_results[i]['search_results'][j]['body']['url'],
                    'id': final_results[i]['search_results'][0]['result_id']
                })
    return message_parts_list