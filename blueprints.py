from flask import Blueprint
from models.base import db
from models.SearchModel import OutQuery, Search, SearchResultDb
from models.MessageModel import Message
from models.SearchParameters import SearchParameters

message = Blueprint('message',__name__)
outQuery = Blueprint('outQuery',__name__)
search = Blueprint('search',__name__)
searchResultDb = Blueprint('searchResultDb',__name__)
searchParameters = Blueprint('searchParameters', __name__)