import utils
from datetime import datetime

# Search
# Evaluate uniqueness (and store)
# Display new results


def eval_search(searches): 
    
    # Update search variables
    updated_search = previous_search =  utils.open_db(utils.prop('database.open_path'))
    current_searches = [] #holder for final storage; kept searches only

    previous_id_list = utils.get_db_ids(previous_search) 
    # search_queries['searches'][0][2]

    # Search
    for search in searches: #work through the list of queries
        results = [] #holder for handling the sets of search results stemming from each query
        for result in search['search_results']:
            #result_id = result.id
            #Evaluate the new id against the id in the database search results
            if result.id in previous_id_list: 
                break
            elif result.id not in previous_id_list:
                body = {
                    'author':result.author.name,
                    'title':result.title,
                    'created date': datetime.fromtimestamp(result.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                    'url':result.url
                }
                results.append({'result_id': str(result), 'body': body}) #just bundle the result_id and body into its own result object and add it to the the results list
        if results:
            current_searches.append({'query':query,'search_results':results})
    if current_searches:
        updated_search['searches'].append(current_searches) # update the stored_dictionary
    
    return updated_search


def pure_search(search_queries, subreddit, limit):
    search_results = {'searches':[]}
    
    # Update search variables
    current_searches = [] #holder for final storage; kept searches only

    # Search
    for query in search_queries: #work through the list of queries
        results = [] #holder for handling the sets of search results stemming from each query
        for result in subreddit.search(query, sort="new", limit=limit):
            body = {
                'author':result.author.name,
                'title': result.title,
                'created date': datetime.fromtimestamp(result.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                'url':result.url
            }
            results.append({'result_id': str(result), 'body': body}) #just bundle the result_id and body into its own result object and add it to the the results list
        current_searches.append({'query':query,'search_results':results})

    if current_searches:
        search_results['searches'].append(current_searches) # update the stored_dictionary
    
    return search_results

def og_search(search_queries, subreddit, limit): 
    
    # Update search variables
    updated_search = previous_search =  utils.open_db(utils.prop('database.open_path'))
    current_searches = [] #holder for final storage; kept searches only

    previous_id_list = utils.get_db_ids(previous_search) 

    # Search
    for query in search_queries: #work through the list of queries
        results = [] #holder for handling the sets of search results stemming from each query
        for result in subreddit.search(query, sort="new", limit=limit):
            result_id = result.id
            #Evaluate the new id against the id in the database search results
            if result_id in previous_id_list: 
                break
            elif result_id not in previous_id_list:
                body = {
                    'author':result.author.name,
                    'title':result.title,
                    'created date': datetime.fromtimestamp(result.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                    'url':result.url
                }
                results.append({'result_id': str(result), 'body': body}) #just bundle the result_id and body into its own result object and add it to the the results list
        if results:
            current_searches.append({'query':query,'search_results':results})
    if current_searches:
        updated_search['searches'].append(current_searches) # update the stored_dictionary
    
    return updated_search