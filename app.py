# approach 2 - PRAW
# https://www.reddit.com/r/GoldTesting/comments/3cm1p8/how_to_make_your_bot_use_oauth2/

import utils
from search import eval_refactor, pure_search, generate_results
from time import process_time
from Twilio import Twilio

t1_start = process_time()
utils.initialize_props()
reddit = utils.get_auth_instance()
twilio = Twilio()

# Search setup
subreddit = reddit.subreddit("mechmarket") #set the subreddit object
search_queries = ["jelly","olivia","yugo"] #list of the queries to search for (move to config.json)
limit = 1 #limit for the queries (move to config.json)

# does searches ever go deeper than [0] ANSWER: no
search_result = pure_search(search_queries, subreddit, limit)
result_ids = eval_refactor(search_result)
final_results = generate_results(search_result, result_ids, 'new', False)

# Twilio stuff
message_parts_list = twilio.message.parse_results(final_results)
message_list = twilio.message.build_message(message_parts_list)

# store the messages sent BEFORE sending so you guarantee the id is already in the db before the user responds
twilio.message.store_messages()

#send the messages
twilio.message.send_message(message_list)


# Timer and teardown
t1_stop = process_time()
print(f'\nDone!\nTotal time (seconds): {t1_stop-t1_start}\nPress any key to close the program.')
input()
# sys.exit('Exit.')
exit()