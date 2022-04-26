# approach 2 - PRAW
# https://www.reddit.com/r/GoldTesting/comments/3cm1p8/how_to_make_your_bot_use_oauth2/

import utils
from models.SearchModel import pure_search, clean_up_db, reddit_search
from time import process_time
from models.MessageModel import Twilio

def runmain():
    t1_start = process_time()
    utils.initialize_props()
    reddit = utils.get_auth_instance()

    # Search setup
    subreddit = reddit.subreddit("mechmarket") #set the subreddit object
    search_queries = ["jelly","olivia","yugo"] #list of the queries to search for (move to config.json)
    limit = 1 #limit for the queries (move to config.json)

    search_result = reddit_search(search_queries, subreddit, limit)
    # eval()

    # Twilio stuff
    twilio = Twilio()
    twilio.message.build_message()
    twilio.message.send_message()

    # Timer and teardown
    t1_stop = process_time()
    print(f'\nDone!\nTotal time (seconds): {t1_stop-t1_start}\nPress any key to close the program.')
    # input()
    # sys.exit('Exit.')
    return True

def clean():
    clean_up_db()
    return True