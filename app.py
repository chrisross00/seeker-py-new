# approach 2 - PRAW
# https://www.reddit.com/r/GoldTesting/comments/3cm1p8/how_to_make_your_bot_use_oauth2/

from turtle import update
import pandas as pd
from search import eval_refactor, pure_search, generate_results
import utils
from time import process_time
import itertools

t1_start = process_time()
utils.initialize_props()
reddit = utils.get_auth_instance()

# Search setup
subreddit = reddit.subreddit("mechmarket") #set the subreddit object
search_queries = ["jelly","olivia","yugo"] #list of the queries to search for (move to config.json)
limit = 3 #limit for the queries (move to config.json)

# does searches ever go deeper than [0] ANSWER: no
search_result = pure_search(search_queries,subreddit,limit)
print('\nSearch Result objects: ', (search_result))
print('\nSearch Result object dir(): ', dir(search_result[0]))

result_ids = eval_refactor(search_result)
finalized_results = generate_results(search_result, result_ids)
utils.save_db(finalized_results, utils.prop('database.save_path'))


# # print(updated_search)
# # print(type(updated_search))

# utils.save_db(finalized_results, utils.prop('database.save_path'))

# Timer and teardown
t1_stop = process_time()
print(f'\nDone!\nTotal time (seconds): {t1_stop-t1_start}\nPress any key to close the program.')
input()
# sys.exit('Exit.')
exit()