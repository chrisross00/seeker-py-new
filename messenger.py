import twilio
from twilio.rest import Client
import utils
from dateutil import parser 
from datetime import datetime

# https://www.twilio.com/blog/phone-verification-with-twilio-for-python-developers
# https://www.twilio.com/docs/sms/api/message-resource


class Message:
    def __init__(self, twilio):
        print(twilio)
        self.twilio = twilio[0]
        self.from_phone = twilio[1]
        self.to_phone = twilio[2]

    def build_message(self, message_parts_list):
        body_list = []
        #build body with message_parts_list
        for i in range(len(message_parts_list)):
            # day in s = 86400
            days_ago = message_parts_list[i]['datediff_total_seconds']/86400
            days_around_round = round(days_ago)
            message = 'New post found with title: "' + str(message_parts_list[i]['title']) + '".\nThis was posted about ' + str(days_around_round) + ' days ago.\nUrl: ' + message_parts_list[i]['url']
            body_list.append(message)

        return body_list

    def send_message(self,body):
        #build body with message_parts_list
        for b in body:
            self.twilio.messages.create(body=b,from_=self.from_phone,to=self.to_phone)



# Pipeline
## App gets final-results and updates the json database
## app uses modules from messenger to:
    ## pass in final_results and process each result for the parts needed to build a message
    ## build a message
    ## 
    ## send a message for each new result in final_results




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
                    'url': final_results[i]['search_results'][j]['body']['url']
                })
    return message_parts_list

    
    # final_results[0]['search_results'][0]['body']['title'] 
    # convert final_results into a list of message bodies or 



#parser.parse(str(final_results[0]['search_results'][0]['body']['created_date_local']))








# def default(results_dict):
#     print(results_dict)
#     return

# m = Message(utils.get_twilio_instance()) #get and pass a Twilio auth object to make a new Message class
# body="This is a test body as a variable"
# m.send_message(body)


# message = m.twilio.messages.create(body="Hi there from Chris's app",from_='+12393269841',to='+16175832854')
