from datetime import datetime
from sqlalchemy.orm import backref
from models.base import db

# ==================================================================
# Database table definitions
# ==================================================================

class OutQuery(db.Model): # a list of searches makes a query... it's a "query" to Reddit's API
    __tablename__ = "OutQuery"
    id = db.Column(db.Integer, primary_key=True)
    searches = db.relationship('Search', backref='outquery',lazy=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Create a string
    def __repr__(self):
        return '<id %r>' % self.id

class Search(db.Model): # an object with search parameters and search results is a search
    __tablename__ = "Search"
    id = db.Column(db.Integer, primary_key=True)
    query_id = db.Column(db.Integer, db.ForeignKey('OutQuery.id'), nullable=False)
    search_results = db.relationship('SearchResultDb', backref=backref('search',order_by=id))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Create a string
    def __repr__(self):
        return '<id %r>' % self.id

class SearchResultDb(db.Model):
    __tablename__ = "SearchResultDb"
    id = db.Column(db.Integer, primary_key=True)
    result_id = db.Column(db.String(100), nullable=False)
    search_id = db.Column(db.Integer, db.ForeignKey('Search.id'), nullable=False)
    search_query = db.Column(db.String(100),nullable=False)
    subreddit = db.Column(db.String(100),nullable=False)
    subreddit_id = db.Column(db.String(100),nullable=False)
    author = db.Column(db.String(200), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    post_date_local = db.Column(db.String(200), nullable=False)
    post_date_utc = db.Column(db.Integer, nullable=False)
    evaluated = db.Column(db.Integer, nullable=False)
    insert_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Create a string
    def __repr__(self):
        return '<id %r>' % self.id


# ==================================================================
# App object definition
# ==================================================================

from models.MessageModel import add_result

class SearchResult:
    def __init__(self, search, query, db_q):
        self.search = search
        self.query = query
        self.search_result = []
        self.unique_result = []
        self.has_unique_result = False
        
        s = Search(query_id=db_q)

        for result in self.search:
            sr = SearchResultDb(
                search=s, 
                result_id=str(result),
                search_query=query, 
                subreddit=result.subreddit.display_name,
                subreddit_id=result.subreddit_id,
                author=result.author.name, 
                title=str(result.title), 
                post_date_local=datetime.fromtimestamp(result.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                post_date_utc=result.created_utc,
                url=result.url,
                evaluated=0
            )
            s.search_results.append(sr)
        self.search_result = s
        
        return None
        
def reddit_search(search_queries, subreddit, limit):

    # Run the search
    db_q = OutQuery()
    db.session.add(db_q)
    for query in search_queries: #work through the list of queries
        new_search = subreddit.search(query, sort="new", limit=limit)
        s = SearchResult(new_search, query, db_q)
        db_q.searches.append(s.search_result)
    db.session.commit()

    # Evaluate against db
    unevaluated = SearchResultDb.query.filter_by(evaluated=0).all()
    evaluated = SearchResultDb.query.filter_by(evaluated=1).all()
    evaluated_list = []

    for e in evaluated:
        evaluated_list.append(e.result_id)

    for u in unevaluated: # remove if the unevaluated row is in the list of evaluated rows
        if u.result_id in evaluated_list:
            SearchResultDb.query.filter_by(result_id=u.result_id, evaluated=0).delete()
        elif u.result_id not in evaluated_list:
            u.evaluated = 1
            db.session.add(u)
            add_result(u)
    db.session.commit()
    
    # Dump Search tables if no children
    SearchTable = Search.query.all()
    for u in SearchTable:
        if SearchResultDb.query.filter_by(search_id=u.id).all():
            pass
        else:
            Search.query.filter_by(id=u.id).delete()
    db.session.commit()
    
    # Dump OutQuery tables if no children
    OutQueryTable = OutQuery.query.all()
    for u in OutQueryTable:
        if Search.query.filter_by(query_id=u.id).all():
            pass
        else:
            OutQuery.query.filter_by(id=u.id).delete()
    db.session.commit()
    
    return None

def clean_up_db():
    SearchTable = Search.query.all()
    for u in SearchTable:
        if SearchResultDb.query.filter_by(search_id=u.id).all():
            pass
        else:
            Search.query.filter_by(id=u.id).delete()
    db.session.commit()

    return True