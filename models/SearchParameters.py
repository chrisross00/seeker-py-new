from datetime import datetime
from sqlalchemy.orm import backref
from sqlalchemy import desc
from models.base import db
import hashlib

class SearchParameters(db.Model):
    __tablename__ = "SearchParameters"
    id = db.Column(db.Integer, primary_key=True)
    site = db.Column(db.String(200), nullable=False)
    subdomain = db.Column(db.String(200), nullable=False)
    search_terms = db.Column(db.String(200), nullable=False)
    limit = db.Column(db.Integer, default=1)
    insert_date = db.Column(db.DateTime, default=datetime.utcnow)
    modified_date = db.Column(db.DateTime, default=datetime.utcnow)
    searches = db.relationship('Search', backref=backref('searchparameters'))
    hashed_search = db.Column(db.String(200), nullable=False)

    # Create a string
    def __repr__(self):
        return '<id %r>' % self.id

def add_parameters(site, subdomain, search_terms, limit=1): # PASS UI PARAMETERS HERE     
    print(f'received search_terms, {search_terms}')
    # check if unique first
    params = SearchParameters( #PASS-IN PARAMETER
        site= site,
        subdomain= subdomain,
        search_terms= search_terms,
        limit=limit
    )
    hashed_params = search_result_hash(params)
    print(f'hashed_params {hashed_params}')
    previous_search_params = SearchParameters.query.filter_by(hashed_search=hashed_params).first()
    print(f'previous_search_params, {previous_search_params}')

    if previous_search_params:
        print(f'found this search param already')
        previous_search_params.modified_date = datetime.utcnow()
        db.session.add(previous_search_params)
        db.session.commit()
        return previous_search_params
    else:
        print(f'NEW SEARCH PARAMS!')
        params.hashed_search = hashed_params
        db.session.add(params)
        db.session.commit()
        return params

def get_parameters():
    most_recent_parameters = SearchParameters.query.order_by(desc(SearchParameters.modified_date)).first()
    # print(f'most_recent_parameters {most_recent_parameters}')
    return most_recent_parameters

def search_result_hash(params):
    to_hash = str(params.site) + str(params.subdomain) + str(params.search_terms) + str(params.limit)
    hash_object = hashlib.sha256(to_hash.encode('utf-8')) #
    hex_dig = hash_object.hexdigest() # if SearchParameters.query.filter_by(hash=hex_dig)...
    return hex_dig