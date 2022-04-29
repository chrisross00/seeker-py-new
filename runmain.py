# approach 2 - PRAW
# https://www.reddit.com/r/GoldTesting/comments/3cm1p8/how_to_make_your_bot_use_oauth2/

import utils
from models.SearchModel import clean_up_db, reddit_search
from models.MessageModel import Twilio
from models.SearchParameters import add_parameters

def runmain():
    
    reddit = utils.get_auth_instance()

    # get parameters to pass to add_parameters
    search_params = add_parameters() #get stuff from the UI and pass it to the DB - if you've seen it, use the search param from before: if not store it and use the new one
    reddit_search(search_params, reddit)

    # Twilio stuff
    # twilio = Twilio()
    # twilio.message.build_message()
    # twilio.message.send_message()
    # print('done!')

    return

def clean():
    clean_up_db()
    return

def test():
    # # Test search
    # reddit = utils.get_auth_instance()

    # Search setup
    # subreddit = reddit.subreddit("mechmarket") #set the subreddit object
    # search_queries = ["owlabs","olivia","yugo"] #list of the queries to search for (move to config.json)
    # limit = 1 #limit for the queries (move to config.json)

    # search_result = reddit_search(search_queries, subreddit, limit)

    # # Test sending messages
    # twilio = Twilio()
    # twilio.message.insert_test_messsage()
    # twilio.message.build_message()
    # twilio.message.send_message()
    
    return

