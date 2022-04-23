from datetime import datetime
from flask import Flask, FlaskForm
from flask_sqlalchemy import SQLAlchemy

# create a Flask instance
app = Flask(__name__)

# add database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# secret key
app.config['SECRET_KEY'] = 'supersecretkey'
# initialize db
db = SQLAlchemy(app)

# Create a Model - required to create a database
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    date_added =db.Column(db.DateTime, default=datetime.utcnow)

    # Create a string
    def __repr__(self):
        return '<Name %r>' % self.name


def example_add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data) #query the database, get all the users who have the email matching what is passed to the email parameter
        if user is None: #if user doesn't exist, create one
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash("User added successfully!")

# To query db and add to page
## https://youtu.be/Q2QmST-cSwc?t=1130