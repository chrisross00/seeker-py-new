# approach 2 - PRAW
# https://www.reddit.com/r/GoldTesting/comments/3cm1p8/how_to_make_your_bot_use_oauth2/

import utils
from models.SearchModel import clean_up_db, reddit_search
from models.MessageModel import Twilio

def runmain():
    utils.initialize_props()
    reddit = utils.get_auth_instance()

    # Search setup
    subreddit = reddit.subreddit("mechmarket") #set the subreddit object
    search_queries = ["owlabs","j-01","yugo"] #list of the queries to search for (move to config.json)
    limit = 1 #limit for the queries (move to config.json)

    search_result = reddit_search(search_queries, subreddit, limit)
    # eval()

    # Twilio stuff
    twilio = Twilio()
    twilio.message.build_message()
    twilio.message.send_message()
    # print('done!')

    return

def clean():
    clean_up_db()
    return

def test():
    # # Test search
    reddit = utils.get_auth_instance()

    # Search setup
    # subreddit = reddit.subreddit("mechmarket") #set the subreddit object
    # search_queries = ["owlabs","olivia","yugo"] #list of the queries to search for (move to config.json)
    # limit = 1 #limit for the queries (move to config.json)

    # search_result = reddit_search(search_queries, subreddit, limit)

    # # Test sending messages
    twilio = Twilio()
    # twilio.message.insert_test_messsage()
    twilio.message.build_message()
    twilio.message.send_message()
    return