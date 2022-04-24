from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

# create a Flask instance
app = Flask(__name__)

# add database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///searches.db'
# secret key
app.config['SECRET_KEY'] = 'supersecretkey'
# initialize db
db = SQLAlchemy(app)

# Create a Model - required to create a database
class Query(db.Model): # a list of searches makes a query... it's a "query" to Reddit's API
    id = db.Column(db.Integer, primary_key=True)
    searches = db.relationship('Search', backref='query',lazy=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Create a string
    def __repr__(self):
        return '<id %r>' % self.id

class Search(db.Model): # an object with search parameters and search results is a search
    id = db.Column(db.Integer, primary_key=True)
    query_id = db.Column(db.Integer, db.ForeignKey('query.id'), nullable=False)
    search_results = db.relationship('SearchResultDb', backref=backref('search',order_by=id))

    # Create a string
    def __repr__(self):
        return '<id %r>' % self.id

class SearchResultDb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    result_id = db.Column(db.String(100), nullable=False)
    search_id = db.Column(db.Integer, db.ForeignKey('search.id'), nullable=False)
    search_query = db.Column(db.String(100),nullable=False)
    subreddit = db.Column(db.String(100),nullable=False)
    subreddit_id = db.Column(db.String(100),nullable=False)
    author = db.Column(db.String(200), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    post_date_local = db.Column(db.String(200), nullable=False)
    post_date_utc = db.Column(db.String(200), nullable=False)
    evaluated = db.Column(db.Integer, nullable=False)

    # Create a string
    def __repr__(self):
        return '<id %r>' % self.id

@app.route('/')
def index():
    return "<h1>Hello</h1>"

# app.run()

# example Model
# class Users(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(200), nullable=False)
#     email = db.Column(db.String(200), nullable=False, unique=True)
#     date_added =db.Column(db.DateTime, default=datetime.utcnow)

#     # Create a string
#     def __repr__(self):
#         return '<Name %r>' % self.name
# def example_add_user():
#     name = None
#     form = UserForm()
#     if form.validate_on_submit():
#         user = Users.query.filter_by(email=form.email.data) #query the database, get all the users who have the email matching what is passed to the email parameter
#         if user is None: #if user doesn't exist, create one
#             user = Users(name=form.name.data, email=form.email.data)
#             db.session.add(user)
#             db.session.commit()
#         name = form.name.data
#         form.name.data = ''
#         form.email.data = ''
#         flash("User added successfully!")

# To query db and add to page
## https://youtu.be/Q2QmST-cSwc?t=1130


# This file is getting close to convert to a db model setup

# basically the below is how you add different stuff to a model, which you can then commit to the database
## To keep foreign key linkages, you can references the backref obj on the child
# q = Query()
# s = Search(query=q)
# sp = SearchParameters(search=s, query='jelly', subreddit='mechmarket', subreddit_id='t5_2vgng') 
# sr = SearchResultRefactor(search=s, result_id='u6nh9a', author="deputy1234", title="[CA-ON] [H] Jelly Epoch SSE Hotswap [W] PayPal or Local Cash/E-transfer", created_date="2022-04-18 15:02:21",url="https://www.reddit.com/r/mechmarket/comments/u6nh9a/caon_h_jelly_epoch_sse_hotswap_w_paypal_or_local/")

## commit it
# db.session.add()
## db.session.add_all([list of stuff])
# db.session.commit()

# from playground.search2 import pure_search, eval


# from playground.playground import db

# import utils
# from models.SearchModel import pure_search, eval
# reddit = utils.get_auth_instance()
# subreddit = reddit.subreddit("mechmarket") #set the subreddit object
# search_queries = ["jelly","olivia","botanical"] #list of the queries to search for (move to config.json)
# limit = 1 #limit for the queries (move to config.json)
# search_result = pure_search(search_queries, subreddit, limit)