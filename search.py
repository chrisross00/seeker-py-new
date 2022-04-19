from collections import namedtuple
from re import T
from turtle import update
from jmespath import search
import utils
from datetime import datetime

# Search
# Evaluate uniqueness (and store)
# Display new results

class SearchResult:
    def __init__(self, search, query):
        self.search = search
        self.query = query
        self.search_result = []
        self.unique_result = []
        self.has_unique_result = False
        
        raw_results = []
        for result in self.search:
            raw_results.append(
                {
                    'result_id': str(result), 
                    'body':  {
                        'author': result.author.name,
                        'title': str(result.title),
                        'created_date_local': datetime.fromtimestamp(result.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                        'created_date_utc': result.created_utc,
                        'url': result.url
                    }
                }
            )
        self.search_result = (
            {   
                'search_parameters': {
                    'query': self.query,
                    'subreddit': result.subreddit.display_name, 
                    'subreddit_id': result.subreddit_id
                },
                'search_results': raw_results
            }
        ) 
        self.unique_result = self.search_result
        return None

    def get_unique_result(self, result_ids):
        unique_results = []
        for result in self.search_result['search_results']:
            if result['result_id'] in result_ids:
                unique_results.append(result)
        if unique_results:
            self.unique_result['search_results'] = unique_results
            self.has_unique_result = True
        else:
            return
        
def pure_search(search_queries, subreddit, limit):
    search_results = [] #holder for final storage; kept searches only
    for query in search_queries: #work through the list of queries
        new_search = subreddit.search(query, sort="new", limit=limit)
        sr = SearchResult(new_search, query)
        # sr.build_unique_result('test')
        search_results.append(sr)
    return search_results

def eval_refactor(search_result): #Given a list of searches, return the ids of results that are new
    t = search_result
    updated_search = utils.open_db(utils.prop('database.open_path'))
    previous_id_list = utils.get_db_ids(updated_search) # get the db ids

    results = []
    for i in range(len(search_result)):
        for result in search_result[i].search_result['search_results']:
            if result['result_id'] in previous_id_list:
                continue
            else:
                results.append(result['result_id'])
    return results

def generate_results(search_result, result_ids, mode):
    unique_results = []
    updated_search = utils.open_db(utils.prop('database.open_path'))
    for i in range(len(search_result)):
        search_result[i].get_unique_result(result_ids)
        if search_result[i].has_unique_result:
            unique_results.append(search_result[i].unique_result)
        else:  
            pass
    if unique_results:
        updated_search['searches'].append(unique_results)
    
    if mode == 'all':
        utils.save_db(updated_search, utils.prop('database.save_path'))
        return updated_search 
    elif mode == 'new':
        return unique_results