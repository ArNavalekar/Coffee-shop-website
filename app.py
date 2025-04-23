






   

from flask import Flask, render_template, request, redirect, url_for, session, flash,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
import io
import jwt
import smtplib
from email.mime.text import MIMEText
import uuid
from datetime import datetime,timedelta
import matplotlib.pyplot as plt
import os
import base64
from calendar import month_name 
from datetime import datetime
from collections import Counter,defaultdict





app = Flask(__name__)

# Flask configuration
app.secret_key = 'b513b50a29079cb504cb57d2fdad74b2'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Database URI yahan set karein
app.config['SESSION_PERMANENT'] = True
#After sufficient time it delete
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # Automatically clear session on server restart


db = SQLAlchemy(app)
mail = Mail(app)


@app.before_request
def clear_session_on_restart():
    if not os.path.exists('session.txt'):
        open('session.txt', 'w').close()
        session.clear()
        
        
# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    reset_token = db.Column(db.String(200), nullable=True)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(128))  # Password hash for the reset functionality

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')  # Password hashing


#Order model
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    mobile = db.Column(db.String(100), nullable=False)
    coffee_type = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    payment = db.Column(db.String(100), nullable=False)
    date_ordered = db.Column(db.DateTime, default=datetime.utcnow)



# Admin Model
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.String(10), nullable=False)  # Format: YYYY-MM-DD
    place = db.Column(db.String(100), nullable=False)
    security_question = db.Column(db.String(200),nullable=False)
    security_answer = db.Column(db.String(200),nullable=False)
    
    def __repr__(self):
        return f'<Admin {self.name}>'

# Home Page
@app.route('/')
def index():
    if 'user_id' not in session:
        flash('You need to sign in to access this page.')
        return redirect(url_for('signin'))
    return render_template('index.html')


# Page
@app.route('/index2')
def index2():
    return render_template('index2.html')  # Ensure 'admin.html' exists in your templates folder


# Signup Page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match!')
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=hashed_password)
        try:
            db.session.add(new_user)
            db.session.commit()
            session['user_id'] = new_user.id
            session['username'] = username  # Store username in session
            session['email'] = email  # Store email in session
            flash('Account created successfully! Please log in.')
            return redirect(url_for('signin'))
        except Exception as e:
            db.session.rollback()
            flash('Email  or Username already exists! Please use a different email or username.')
            return redirect(url_for('signup'))

    return render_template('signup.html')



# Signin Page
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username_or_email = request.form['username_or_email']
        password = request.form['password']
        user = User.query.filter((User.username == username_or_email) | (User.email == username_or_email)).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username  # Store username in session
            session['email'] = user.email  # Store email in session
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials!')
    return render_template('signin.html')




#view users
@app.route('/users', methods=['GET', 'POST'])
def view_users():
    users = User.query.all()
    
    # Default Year: Current Year
    selected_year = request.form.get('year', str(datetime.now().year))  # Default: Current Year
    
    # Filter users by selected year
    signups = User.query.filter(db.extract('year', User.date_joined) == int(selected_year)).all()

    # Agar selected year me koi users nahi mile to users ko empty list set karo
    users = signups if signups else []

    # Month-wise count get
    signup_dates = [user.date_joined.strftime("%B") for user in signups]
    signup_counts = Counter(signup_dates)

    # Ensure all months are included
    months = list(month_name)[1:]  # Exclude empty first item
    month_counts = {month: signup_counts.get(month, 0) for month in months}

    
    plt.figure(figsize=(13, 4))
    plt.bar(month_counts.keys(), month_counts.values(), color='orange', width=0.4)
    plt.xlabel('Month')
    plt.ylabel('Signups')
    plt.title(f'Monthly Signups ({selected_year})')  # Selected Year Title

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()

    return render_template('users.html', users=users, graph_url=graph_url, selected_year=selected_year)

# Logout Page
@app.route('/logout')
def logout():
    user_id = session.get('user_id')  # Get current user ID 
    if user_id:
        user = User.query.get(user_id)  # Grt user from databae
        if user:
            db.session.delete(user)  # User  delete 
            db.session.commit()  # Changes  commit
    session.pop('user_id', None)  # Session se user ID  remove 
    flash('You have been logged out and your account has been deleted.')
    return redirect(url_for('index'))


#order page
@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        if 'cancelOrder' in request.form:
            # Fetch the latest order from the database based on user session
            user_id = session.get('user_id')  # Assume user_id is stored in session
            latest_order = Order.query.filter_by(user_id=user_id).order_by(Order.date_ordered.desc()).first()

            # Delete the latest order if it exists
            if latest_order:
                db.session.delete(latest_order)
                db.session.commit()
                flash('Order has been canceled and removed from the database.', 'success')
            return redirect('/order')
        
        # If no cancel button clicked, proceed with the order form submission
        coffee_type = request.form['coffee']
        quantity = request.form['quantity'] 
        name = request.form['name']
        email = request.form['email']    
        address = request.form['address']
        mobile = request.form['mobile']  
        price = request.form['price']   
        payment = request.form['payment']    
        user_id = session.get('user_id')  # Assume user_id is stored in session
        
        new_order = Order(user_id=user_id, coffee_type=coffee_type, quantity=quantity, name=name, email=email, address=address, mobile=mobile, price=price, payment=payment)
        db.session.add(new_order)
        db.session.commit()

        return redirect(url_for('index'))
    
    # Pass username and email to the order page
    username = session.get('username', '')  # Get username from session
    email = session.get('email', '')  # Get email from session
    return render_template('order.html', username=username, email=email)




#view order page
@app.route('/view_order', methods=['GET', 'POST'])
def view_orders():
    orders = []
    message = None
    pie_chart_url = None
    analysis_type = request.form.get('analysis_type')
    selected_month_name = None
    selected_year = None
    selected_day_from = None
    selected_month_from = None
    selected_year_from = None
    selected_day_to = None
    selected_month_to = None
    selected_year_to = None

    if request.method == 'POST':
        if analysis_type == 'month':
            selected_month = request.form['month']
            selected_month = int(selected_month)

            # Fetch orders for the selected month
            orders = Order.query.filter(db.extract('month', Order.date_ordered) == selected_month).all()

            # Set selected month name
            selected_month_name = datetime(2025, selected_month, 1).strftime('%B')

        elif analysis_type == 'month_year':
            selected_month = request.form['month_year']
            selected_year = request.form['year']
            selected_month = int(selected_month)
            selected_year = int(selected_year)

            # Fetch orders for the selected month and year
            orders = Order.query.filter(db.extract('month', Order.date_ordered) == selected_month,
                                        db.extract('year', Order.date_ordered) == selected_year).all()

            # Set selected month name and year
            selected_month_name = datetime(selected_year, selected_month, 1).strftime('%B')

        elif analysis_type == 'year':
            selected_year = request.form['year']
            selected_year = int(selected_year)

            # Fetch orders for the selected year
            orders = Order.query.filter(db.extract('year', Order.date_ordered) == selected_year).all()

            # Set selected year only
            selected_month_name = "All Months"

        elif analysis_type == 'from_to':
            selected_day_from = request.form['day_from']
            selected_month_from = request.form['month_from']
            selected_year_from = request.form['year_from']
            selected_day_to = request.form['day_to']
            selected_month_to = request.form['month_to']
            selected_year_to = request.form['year_to']

            # Convert to integers
            selected_day_from = int(selected_day_from)
            selected_month_from = int(selected_month_from)
            selected_year_from = int(selected_year_from)
            selected_day_to = int(selected_day_to)
            selected_month_to = int(selected_month_to)
            selected_year_to = int(selected_year_to)

            # Convert the selected range to datetime objects
            from_date = datetime(selected_year_from, selected_month_from, selected_day_from)
            to_date = datetime(selected_year_to, selected_month_to, selected_day_to)

            # Adjust to_date to include the entire day
            to_date = to_date + timedelta(days=1) - timedelta(seconds=1)
            
            # Fetch orders for the selected date range
            orders = Order.query.filter(Order.date_ordered >= from_date, Order.date_ordered <= to_date).all()

            # Set selected month name for the range
            selected_month_name = f"{from_date.strftime('%d-%B-%Y')} to {to_date.strftime('%d-%B-%Y')}"
            selected_year = None #year range already included

            

       #Based on cofee quantity     
        if orders:
            coffee_sales = defaultdict(int)  # Dictionary to store total quantity per coffee type
            for order in orders:
                coffee_sales[order.coffee_type] += order.quantity  # Summing quantity instead of count

            plt.figure(figsize=(8, 6))
            plt.pie(coffee_sales.values(), labels=coffee_sales.keys(), autopct='%1.1f%%')
            plt.title(f'Coffee Sales Analysis')

            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            pie_chart_url = base64.b64encode(img.getvalue()).decode()
        else:
            message = "No orders found for the selected criteria."    

    return render_template('view_order.html', orders=orders, analysis_type=analysis_type, pie_chart_url=pie_chart_url, message=message, selected_month_name=selected_month_name, selected_year=selected_year,
                           selected_day_from=selected_day_from,selected_month_from=selected_month_from,selected_year_from=selected_year_from,selected_day_to=selected_day_to,selected_month_to=selected_month_to,selected_year_to=selected_year_to)


@app.route('/view_bill', methods=['GET'])
def view_bill():
    # Fetch the latest order details based on user session
    user_id = session.get('user_id')  # Assume user_id is stored in session
    latest_order = Order.query.filter_by(user_id=user_id).order_by(Order.date_ordered.desc()).first()

    # Pass order details to the template
    if latest_order:
        return render_template('view_bill.html', order=latest_order)
    else:
        flash("No order found to display.", "warning")
        return redirect('/order')







#admin signup

@app.route('/admin_signup', methods=['GET', 'POST'])
def admin_signup():
    if request.method == 'POST':
        # Check if admin already exists
        existing_admin = Admin.query.first()
        if existing_admin:
            flash('An admin account already exists!', 'danger')
            return redirect(url_for('admin_login'))

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        reenter_password = request.form['reenter_password']
        date_of_birth = request.form['dob']
        place = request.form['place']
        security_question = request.form['security_question']
        security_answer = request.form['security_answer']

        if password != reenter_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('admin_signup'))

        new_admin = Admin(
            name=name,
            email=email,
            password=generate_password_hash(password),
            date_of_birth=date_of_birth,
            place=place,
            security_question=security_question,
            security_answer=security_answer
        )
        try:
            db.session.add(new_admin)
            db.session.commit()
            flash('Admin registered successfully!', 'success')
            return redirect(url_for('admin_login'))
        except:
            flash('Error in registration. Try again!', 'danger')
            return redirect(url_for('admin_signup'))
    return render_template('admin_signup.html')


# Admin Login route
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Ensure that only current admin's data is used for login
        admin = Admin.query.filter_by(email=email).first()
        

        if admin and check_password_hash(admin.password, password):
            return redirect(url_for('admin_dashboard', admin_id=admin.id))
        else:
            flash('Invalid login credentials or no admin account exists!', 'danger')
            return redirect(url_for('admin_login'))
    return render_template('admin_login.html')

# Admin Dashboard route (current admin details)
@app.route('/admin_dashboard/<int:admin_id>')
def admin_dashboard(admin_id):
    admin = Admin.query.get_or_404(admin_id)  # Get the current admin using their ID
    return render_template('admin_dashboard.html', admin=admin)




@app.route('/change_admin_step1', methods=['GET', 'POST'])
def change_admin_step1():
    admin = Admin.query.first()  # Get the current admin
    if request.method == 'POST':
        dob = request.form['dob']
        place = request.form['place']
        security_answer = request.form['security_answer']

        # Check if entered details match the current admin's details
        if dob == admin.date_of_birth and place == admin.place and security_answer == admin.security_answer:
            return redirect(url_for('change_admin_step2'))
        else:
            flash('Verification failed! Incorrect details provided.', 'danger')
            return redirect(url_for('change_admin_step1'))
    return render_template('change_admin_step1.html', admin=admin)
    
    

# Change Admin Details Route (Step 2)
@app.route('/change_admin_step2', methods=['GET', 'POST'])
def change_admin_step2():
    admin = Admin.query.first()  # Get the current admin
    if request.method == 'POST':
        new_name = request.form['new_name']
        new_email = request.form['email']
        new_password = request.form['password']
        reenter_password = request.form['reenter_password']
        new_dob = request.form['new_dob']
        new_place = request.form['new_place']
        new_security_question = request.form['security_question']
        new_security_answer = request.form['security_answer']

        # Check if passwords match
        if new_password != reenter_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('change_admin_step2'))

        # Update admin details
        admin.name = new_name
        admin.email = new_email
        admin.password = generate_password_hash(new_password)
        admin.date_of_birth = new_dob
        admin.place = new_place
        admin.security_question = new_security_question
        admin.security_answer = new_security_answer

        db.session.commit()
        flash('Admin details updated successfully!', 'success')
        return redirect(url_for('admin_dashboard', admin_id=admin.id))
    return render_template('change_admin_step2.html', admin=admin)

    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(host='0.0.0.0', port=8000, debug=True)    
    
    
    

