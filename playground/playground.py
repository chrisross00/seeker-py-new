from collections import namedtuple

class MyObject:
    def __init__(self, d=None):
        if d is not None:
            for key, value in d.items():
                setattr(self, key, value)

search = {
    'result_id': 'asdf2423', 
    'body':  {
        'author': 'asdf',
        'title': 'title',
        'created_date': 'date',
        'url': 'website'
    }
}

obj_dict = {}
o = MyObject(search) #one way to convert to object
dict_object = namedtuple("DictObject", search.keys())(*search.values()) #another way to convert to object

# if i'm passing a dict, I need to flatten it; the original object retrieved in search is flat, the dict is layered

for key, value in search.items():
    if type(value) is dict:
        # newthing = namedtuple("newThing", value.keys())(*value.values())
        for k, v in value.items():
            obj_dict[k] = v
    else:
        obj_dict[key] = value

# can I just call dict_object.key3 and replace that with the namedtuple assignment

# dict_object.key3 = sub_object


# Result = namedtuple('Result', ['x', 'y'])
# result = Result(5, 6)\




# convert list of objects to one big object?
