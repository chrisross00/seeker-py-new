from datetime import datetime
from sqlalchemy.orm import backref
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
    searches = db.relationship('Search', backref=backref('searchparameters'))
    hashed_search = db.Column(db.String(200), nullable=False)

    # Create a string
    def __repr__(self):
        return '<id %r>' % self.id

def test_add_parameters(): # in future, pass params in instead
        
    search_str = "epoch, oliviaa, yugo" #PASS-IN PARAMETER
    search_str = search_str.replace(" ", "")

    # check if unique first
    params = SearchParameters( #PASS-IN PARAMETER
        site= 'reddit',
        subdomain= 'mechmarket',
        search_terms= search_str
    )
    hashed_params = search_result_hash(params)
    print(f'hashed_params {hashed_params}')
    previous_search_params = SearchParameters.query.filter_by(hashed_search=hashed_params).first()
    print(f'previous_search_params, {previous_search_params}')

    if previous_search_params:
        print(f'found this search param already')
        return previous_search_params
    else:
        params.hashed_search = hashed_params
        db.session.add(params)
        db.session.commit()
        return params

def add_parameters(): # PASS UI PARAMETERS HERE     
    search_str = "epoch, olivia, yugo" #PASS-IN PARAMETER
    search_str = search_str.replace(" ", "")

    # check if unique first
    params = SearchParameters( #PASS-IN PARAMETER
        site= 'reddit',
        subdomain= 'mechmarket',
        search_terms= search_str
    )
    hashed_params = search_result_hash(params)
    print(f'hashed_params {hashed_params}')
    previous_search_params = SearchParameters.query.filter_by(hashed_search=hashed_params).first()
    print(f'previous_search_params, {previous_search_params}')

    if previous_search_params:
        print(f'found this search param already')
        return previous_search_params
    else:
        params.hashed_search = hashed_params
        db.session.add(params)
        db.session.commit()
        return params

def search_result_hash(params):
    to_hash = str(params.site) + str(params.subdomain) + str(params.search_terms)
    hash_object = hashlib.sha256(to_hash.encode('utf-8')) #
    hex_dig = hash_object.hexdigest() # if SearchParameters.query.filter_by(hash=hex_dig)...
    return hex_dig