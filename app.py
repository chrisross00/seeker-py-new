# approach 2 - PRAW
# https://www.reddit.com/r/GoldTesting/comments/3cm1p8/how_to_make_your_bot_use_oauth2/

import pandas as pd
from search import pure_search, og_search
import utils
from time import process_time

t1_start = process_time()
utils.initialize_props()
reddit = utils.get_auth_instance()

# Search setup
subreddit = reddit.subreddit("mechmarket") #set the subreddit object
search_queries = ["jelly","olivia","yugo"] #list of the queries to search for (move to config.json)
limit = 10 #limit for the queries (move to config.json)
# x = pure_search(search_queries,subreddit,limit)

updated_search = og_search(search_queries,subreddit,limit)
# Save the database with the updated searches
utils.save_db(updated_search, utils.prop('database.save_path')) #replace path after implementing json and props

t1_stop = process_time()
print(f'\nDone!\nTotal time (seconds): {t1_stop-t1_start}\nPress any key to close the program.')
input()
sys.exit('Exit.')