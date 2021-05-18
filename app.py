from flask import Flask,render_template,request,redirect, flash
from flask_login import login_required, current_user, login_user, logout_user
from models import UserModel, db, login, apology, TravelModel, Distance, stations
import datetime 
from datetime import date

app = Flask(__name__)
app.secret_key = 'xyz'
app.debug = True
 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
db.init_app(app)
login.init_app(app)
login.login_view = 'login'

@app.before_first_request
def create_all():
    db.create_all()


@app.errorhandler(404)
def handle_404(error):
    # Response to wrong url
    return apology('Please, access correct URL!!', 404)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/register', methods=['POST', 'GET']) #register.html
def register():
    if current_user.is_authenticated:
        return redirect('/profile')
     
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        c_password = request.form['c_password']
 
        if UserModel.query.filter_by(email=email).first():
            return apology('Email already Taken', 404)

        # if (password != c_password):
        #     return apology('Your Passwords Do not Match!!!',404)
             
        user = UserModel(email = email, username = username, wallet = 10000)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("Your Account is Registered!")
        return redirect('/login')    
           
    return render_template('register.html')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect('/profile')
     
    if request.method == 'POST':
        email = request.form['email']
        user = UserModel.query.filter_by(email = email).first()
        if user is not None and user.check_password(request.form['password']):
            login_user(user)
            flash('Hello '+user.username+', Welcome back to your Profile')
            return redirect('/profile')
        else:
            return apology('BRO enter correct credentials or Register again!', 505)
     
    return render_template('login.html')

@app.route('/profile', methods = ['POST', 'GET'])
@login_required
def profile():
    history_rows = TravelModel.query.filter_by(user_id = current_user.id).all()
    upcoming_rows = []
    over_rows = []
    for trip in history_rows:
        if (trip.travel_date >= date.today()):
            upcoming_rows.append(trip)
        else:
            over_rows.append(trip)
    u_trips = len(upcoming_rows)
    o_trips = len(over_rows)

    return render_template('profile.html', upcoming = upcoming_rows, u_trips = u_trips, over_rows = over_rows, o_trips = o_trips)
     
@app.route('/book', methods = ['POST', 'GET'])
@login_required
def book():
    if request.method == 'POST':
        departure = request.form['departure']
        destination = request.form['destination']
        t_date = request.form['date']

        if departure not in stations:
            return apology("We are Yet to start ou services at " + departure, 404)

        if destination not in stations:
            return apology("We are Yet to start ou services at " + departure, 404)

        if(departure == destination):
            return apology("Take auto dude!!!", 403)

        # format_str = '%Y-%m-%d' # The format
        # datetime_obj = datetime.datetime.strptime(t_date, format_str)
        # if not datetime_obj:
        #     return apology("Yo Enter correct Date u fool", 404)

        # if(datetime_obj.date() < date.today()):
        #     return apology("We don't give services for time travel", 403) 

        # t_date = datetime_obj
        return redirect(f"/confirm/{departure}/{destination}/{t_date}")

    return render_template('book.html', stations=stations)

@app.route('/confirm/<departure>/<destination>/<t_date>', methods = ['POST', 'GET'])
@login_required
def confirm(departure, destination, t_date):

    format_str = '%Y-%m-%d' # The format
    datetime_obj = datetime.datetime.strptime(t_date, format_str)
    if not datetime_obj:
        return apology("Yo Enter correct Date u fool", 404)

    if(datetime_obj.date() < date.today()):
        return apology("We don't give services for time travel", 403)
                
    apiObj = Distance(departure, destination)
    t_fare = round(apiObj['distance'] * 1.5, 2)
    fare = round(t_fare + (t_fare * 0.18), 2)

    if(fare > current_user.wallet):
        return apology("Contact Developer to topup your wallet", 404)

    o_time = apiObj['time'] # 8 times faster
    t_time = o_time / 8
    if (t_time >= 60):
        t_time = round(t_time / 60, 2)

    if (o_time >= 60):
        o_time = round(o_time / 60, 2)

    o_time = round(o_time - t_time,  2)

    if request.method == 'POST':
        new_wallet = round(current_user.wallet - fare, 2)
        num_rows_updated =  UserModel.query.filter_by(id=current_user.id).update(dict(wallet=new_wallet))
        travel = TravelModel(user_id = current_user.id, departure=departure, destination=destination, travel_date=datetime_obj.date(), booking_date=date.today(), distance=apiObj['distance'], fare=fare)
        db.session.add(travel)
        db.session.commit()
        flash('Your Ticket to '+ destination +' is Confirmed, Happy Journey :)')
        return redirect('/profile')

    return render_template('confirm.html', departure=departure, destination=destination, travel_date=datetime_obj.date(), distance=round(apiObj['distance'], 2), fare=fare, o_time=o_time, t_time=t_time)
    

@app.route('/cancel', methods = ['POST', 'GET'])
@login_required
def cancel():
    history_rows = TravelModel.query.filter_by(user_id = current_user.id).all()
    upcoming = []
    for trip in history_rows:
        if (trip.travel_date >= date.today()):
            upcoming.append(trip)

    u_trips = len(upcoming)

    if request.method == 'POST':
        t_id = request.form['t_id']

        trav = TravelModel.query.filter_by(travel_id = t_id).first()
        if(trav == None):
            return apology("Enter correct Travel ID!!", 404)

        else:
            new_wallet = round((current_user.wallet + (trav.fare/2)), 2)
            num_rows_updated =  UserModel.query.filter_by(id=current_user.id).update(dict(wallet=new_wallet))
            db.session.delete(trav)
            db.session.commit()
            flash("Your Ticket is Cancelled :(")
            
        
        return redirect('/profile')
        
    
    return render_template('cancel.html', upcoming = upcoming, u_trips = u_trips)

@app.route('/topup', methods = ['GET', 'POST'])
@login_required
def topup():
    return render_template('add_card.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged Out Succesfully!')
    return redirect('/login')

