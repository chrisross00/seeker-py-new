# approach 2 - PRAW
from turtle import update
import dotenv
import requests
import praw
import pandas as pd
import hashlib
import json
import utils
from time import process_time
from datetime import datetime
from dateutil import tz
from collections import defaultdict
from dotenv import dotenv_values

t1_start = process_time()
utils.initialize_props()

previous_search = utils.open_db(utils.prop('database.open_path'))
auth_config = {
    **dotenv_values('.env') #load environment variables
}

# Establish authorized Reddit instance
reddit = praw.Reddit(
    client_id = auth_config["CLIENT_ID"],
    client_secret = auth_config["SECRET_TOKEN"],
    user_agent = auth_config["USER_AGENT"],
    username = auth_config["USERNAME"],
    password = auth_config["PASSWORD"]
)

# Variable setup and stuff
subreddit = reddit.subreddit("mechmarket") #set the subreddit object

updated_search = previous_search = utils.open_db('dbdict.json')

# Variable setup
previous_hash_list = [] #to store db hashes
current_searches = [] #holder for final storage; kept searches only
all_searches = [] #holder for analysis; all searches
i_len = len(previous_search['searches']) #length of the current db searches

#store db hashes
# Btw- doesn't work if db is empty
for i in range(i_len):
    j_len = len(previous_search['searches'][i]) #length of the j loop for some reason this works lol
    for j in range(j_len):
        k_len = len(previous_search['searches'][i][j]['search_results'])
        for k in range(k_len):
            previous_hash_list.append(previous_search['searches'][i][j]['search_results'][k]['body']['hash']) #store the hash to the previous_hash_list

search_queries = ["olivia","9009","hammerhead"] #list of the queries to search for (move to config.json)
limit = 3 #limit for the queries (move to config.json)

# Search
for query in search_queries: #work through the list of queries
    results = [] #holder for handling the sets of search results stemming from each query
    for result in subreddit.search(query,sort="new", limit=limit): #for each result in the search results, make a hash in the same way as 
        # Structure the data before storing - there has to be a better way than this... like converting to JSON upstream
        to_hash = str(result.author) + str(result.title) + str(result.url)
        hash_object = hashlib.sha256(to_hash.encode('utf-8')) #
        hex_dig = hash_object.hexdigest() #the hash for this search result
        # all_searches.append({'result_id': result_id, 'body': body}) #could delete this, don't really need it

        #Evaluate the new hash against the hash in the database search results
        
        # Check to see if this search result's hash is in the list. If yes ignore it, if it's not, add it to the db
        if hex_dig in previous_hash_list:
            break
        elif hex_dig not in previous_hash_list:
            body = {
                'author':result.author.name,
                'title':result.title,
                'created date': datetime.fromtimestamp(result.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                'url':result.url,
                'hash':hex_dig
            }
            results.append({'result_id': str(result), 'body': body}) #just bundle the result_id and body into its own result object and add it to the the results list
    if results:
        current_searches.append({'query':query,'search_results':results})
if current_searches:
    updated_search['searches'].append(current_searches) # update the stored_dictionary

# Save the database with the updated searches
utils.save_db(updated_search, utils.prop('database.save_path')) #replace path after implementing json and props

t1_stop = process_time()
print(f'\nDone!\nTotal time (seconds): {t1_stop-t1_start}\nPress any key to close the program.')
input()
sys.exit('Exit.')