import datetime
import json
import requests
from flask import render_template
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

login = LoginManager()
db = SQLAlchemy()

#api_key ='TkRtMRayroocbr0U8bNbtta1Z83Ty'
api_key ='JqgRxWl2TyhpuWy73zuAf9JToyGiE'

stations = ['Bengaluru', 'Delhi', 'Mumbai', 'Chennai', 'Kolkata',
 'Pune', 'Mangalore', 'Hubli', 'Hyderabad', 'Chandigarh']

class UserModel(UserMixin, db.Model):
    __tablename__ = 'users'
 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(), nullable=False)
    wallet = db.Column(db.Integer, nullable=False)
    travels = db.relationship('TravelModel', backref='user', lazy=True)

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)
     
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)


class TravelModel(UserMixin, db.Model):
    __tablename__ = 'travel'

    travel_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    departure = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    travel_date = db.Column(db.Date, nullable=False)
    booking_date = db.Column(db.Date, default=datetime.datetime.now, nullable=False)
    distance = db.Column(db.Integer)
    fare = db.Column(db.Integer)

def apology(message, code):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.
        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message))

def Distance(source, end):
    url ='https://api.distancematrix.ai/maps/api/distancematrix/json?'

    req = requests.get(url + 'origins=' + source + '&destinations=' + end + '&key=' + api_key)
    obj = req.json()

    distApi = {}
    distApi["distance"] = obj['rows'][0]['elements'][0]['distance']['value'] / 1000
    distApi["time"] = obj['rows'][0]['elements'][0]['duration']['value']
    return distApi
 
@login.user_loader
def load_user(id):
    return UserModel.query.get(int(id))
