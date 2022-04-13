import json
import logging
import xml.etree.ElementTree as ET

props = None

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


# Initialize the properties
def initialize_props(force=False):
    global props
    # Assumes there is a configuration file
    if props is None or force:
        with open('config.json', 'r') as f:
            props = json.load(f)
            logging.info('Read ' + str(len(props)) + ' properties')

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
    