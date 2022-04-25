from models.base import db

# Model definition
class Message(db.Model): 
    __tablename__ = "Message"

    id = db.Column(db.Integer, primary_key=True)
    message_body = db.Column(db.String(2000), nullable=True)
    status = db.Column(db.Integer, nullable=False)
    scraped_title = db.Column(db.String(100), nullable=False)
    datediff_total_seconds = db.Column(db.Integer, nullable=False)
    datediff_days = db.Column(db.String(100), nullable=False)
    datediff_seconds = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    result_id = db.Column(db.String, nullable=False)

    # Create a string
    def __repr__(self):
        return '<id %r>' % self.id