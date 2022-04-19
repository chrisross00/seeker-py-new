# approach 2 - PRAW
# https://www.reddit.com/r/GoldTesting/comments/3cm1p8/how_to_make_your_bot_use_oauth2/

# import pandas as pd
from search import eval_refactor, pure_search, generate_results
import utils
from time import process_time
from messenger import parse_results, Message
from Twilio import Twilio

t1_start = process_time()
utils.initialize_props()
reddit = utils.get_auth_instance()
twilio = Twilio()

# Search setup
subreddit = reddit.subreddit("mechmarket") #set the subreddit object
search_queries = ["jelly","olivia","yugo"] #list of the queries to search for (move to config.json)
limit = 4 #limit for the queries (move to config.json)

# does searches ever go deeper than [0] ANSWER: no
search_result = pure_search(search_queries, subreddit, limit)
result_ids = eval_refactor(search_result)
final_results = generate_results(search_result, result_ids, 'new', False)

# Twilio stuff
message_parts_list = twilio.message.parse_results(final_results)
message_list = twilio.message.build_message(message_parts_list)
twilio.message.send_message(message_list)

# commenting saving logic while adding in Twilio stuff
# if final_results:
#     utils.save_db(final_results, utils.prop('database.save_path'))
    
# utils.save_db(final_results, utils.prop('database.save_path'))

# Timer and teardown
t1_stop = process_time()
print(f'\nDone!\nTotal time (seconds): {t1_stop-t1_start}\nPress any key to close the program.')
input()
# sys.exit('Exit.')
exit()