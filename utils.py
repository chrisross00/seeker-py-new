import json
import logging
import praw
from dotenv import dotenv_values
from twilio.rest import Client

props = None

# Initialize the properties
def initialize_props(force=False):
    global props
    # Assumes there is a configuration file
    if props is None or force:
        with open('config.json', 'r') as f:
            props = json.load(f)
            logging.info('Read ' + str(len(props)) + ' properties')

def get_auth_instance():
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
    return reddit

def get_auth_config_parameters():
    auth_config = {
    **dotenv_values('.env') #load environment variables
    }
    return auth_config

def open_db(filepath):
    with open(filepath) as f: #load it to f
        t = f.read() #read it to t
    return json.loads(t) #turn t into a dictionary and store it

def save_db(update_chonk, filepath):
    # Store dictionary somewhere
    # Save dictionary
    data = json.dumps(update_chonk) #the final updated database
    f = open(filepath,"w")
    f.write(data)
    f.close()
    return True

# Get the property for a key
def prop(key):
    global props
    if key is None:
        return None
    
    if props is None:
        initialize_props()
    nests = key.split('.')
    value = props
    for nest in nests:
        value = value.get(nest)
    return value

# Set a property for a key
def setProp(key, value):
    global props
    if props is None:
        initialize_props()

    nests = key.split('.')
    v = props
    i = 0
    for nest in nests:
        if i == len(nests) - 1:
            break
        i += 1
        v = v.get(nest)
    #v[key] = value
    props[nests[0]][nests[1]] = value #hardedcoded to go two layers deep for now
    path = props['input']['config']
    update_file(props, path)

def printy(thing):
    print('\ndir():\n' , dir(thing))
    print('\n')
    print('-'*40)
    print('\nvars():\n', vars(thing))
    print('\n')

# Migrate timer to utils?
    # t1_start = process_time()
    # # Timer and teardown
    # t1_stop = process_time()
    # # print(f'\nDone!\nTotal time (seconds): {t1_stop-t1_start}\nPress any key to close the program.')
    # # input()
    # # sys.exit('Exit.')