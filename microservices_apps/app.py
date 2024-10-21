from flask import Flask, render_template, request, redirect, url_for, session
from flask import Flask, render_template, request, redirect, url_for, session, make_response
app = Flask(__name__, template_folder='custom_templates')
import random 
import os
app.secret_key = 'your_secret_key'
from flask_mail import Mail, Message
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify,json
import hashlib
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash, check_password_hash
# Dummy user data
from urllib.parse import quote_plus
from pymongo import MongoClient
from flask import Flask
from flask_pymongo import PyMongo
users_file = 'users.json'
from pymongo import MongoClient
from urllib.parse import quote_plus
import requests
import logging
from logging.handlers import RotatingFileHandler
log_file = 'app.log'
# Rotating file handler (5MB per file, keep 3 backups)
handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Set up application logging
app.logger.setLevel(logging.INFO)
app.logger.addHandler(handler)

# Set up Werkzeug (Flask's request logger) logging
werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.setLevel(logging.INFO)
werkzeug_logger.addHandler(handler)
from db import users_collection
# Route for the home page
# config.py or app.py

{
  "users": []
}


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'tradingcontentdrive@gmail.com'
app.config['MAIL_PASSWORD'] = 'cgrv wptp tldo gujp'
#app.config['MAIL_PASSWORD'] = 'wxch wxxj xmeg vjpi'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)  # Initialize Flask-Mail
  # Redirect to home on success

registered_users = {}
otp_store = {}  # Store OTPs for users

if not os.path.isfile(users_file):
    with open(users_file, 'w') as f:
        json.dump({"users": []}, f)

def read_users():
    """Read users from the JSON file."""
    try:
        with open(users_file, 'r') as f:
            data = json.load(f)
            print(f"Successfully read users: {data}")  # Debugging output
            return data
    except Exception as e:
        print(f"Error reading users file: {e}")
        return {"users": []}   # Return an empty users list if there's an error

def write_users(users):
    """Write users to the JSON file."""
    try:
        with open(users_file, 'w') as f:
            json.dump(users, f, indent=4)  # Pretty print the JSON with indent
    except Exception as e:
        print(f"Error writing to users file: {e}")

def hash_password(password):
    """Hash the password for secure storage."""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_otp():
    """Generate a random 6-digit OTP."""
    return str(random.randint(100000, 999999))

@app.route('/otp', methods=['POST'])
def send_otp():
    data = request.get_json()
    username = data.get('username').lower()

    if not username:
        return jsonify({'message': 'Email is required to send OTP.'}), 400

    otp = generate_otp()
    otp_store[username] = otp

    # Send OTP email
    msg = Message('Your OTP for Registration',
                  sender='your-email@gmail.com',
                  recipients=[username])
    msg.body = f"Your One-Time Password (OTP) is {otp}."

    try:
        mail.send(msg)
        return jsonify({'message': 'OTP sent to your email. Please check your inbox.'})
    except Exception as e:
        print(f'Error sending OTP: {e}')
        return jsonify({'message': 'Error sending OTP. Please try again later.'}), 500



@app.route('/get_otp', methods=['POST'])
def get_otp():
    data = request.get_json()
    username = data.get('username')

    users_data = read_users()  # Read users from the JSON file
    users = users_data['users']  # Get the list of users

    if any(user['username'] == username for user in users):  # Check if user exists
        otp = generate_otp()  # Generate OTP
        otp_store[username] = otp  # Store OTP for later verification

        # Send the OTP via email
        msg = Message('Your OTP for Login',
                      sender='your-email@gmail.com',
                      recipients=[username])
        msg.body = f"Your One-Time Password (OTP) is {otp}."
        try:
            mail.send(msg)
            print(f"OTP sent to {username}: {otp}")  # Debugging line
            return jsonify({'message': 'OTP sent to your email.'})
        except Exception as e:
            print(f"Failed to send OTP: {e}")  # Log error
            return jsonify({'message': 'Failed to send OTP.'})

    print(f"User not found: {username}")  # Debugging line
    return jsonify({'message': 'User not found.'})



@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    username = data.get('username').lower()
    otp = data.get('otp').strip()

    if username in otp_store and otp_store[username] == otp:
        del otp_store[username]  # Clear OTP after successful verification
        session['username'] = username  # Log in the user
        return jsonify({'success': True, 'redirect_url': url_for('home')})

    return jsonify({'success': False, 'error': 'Invalid OTP.'})

@app.route('/users', methods=['GET'])
def view_users():
    users = users_collection.find({}, {'_id': 0, 'username': 1})  # Fetch all users without displaying the '_id'
    
    user_list = [user['username'] for user in users]  # Create a list of usernames
    print("Registered Users:", user_list)  # Debugging output to see all registered users

    if user_list:
        return render_template('users.html', users=user_list)  # Render the template with the list of users
    else:
        return render_template('users.html', users=[])


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')  # Get the name
        username = request.form.get('username').lower()
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        otp = request.form.get('otp')

        # Check if passwords match
        if password != confirm_password:
            return render_template('register.html', error='Passwords do not match')

        # Check if the OTP is valid
        if username in otp_store and otp_store[username] == otp:
            hashed_password = generate_password_hash(password)

            # Safely remove the OTP after successful use
            otp_store.pop(username, None)

            users_data = read_users()
            existing_user = next((user for user in users_data['users'] if user['username'] == username), None)

            if existing_user:
                return render_template('register.html', error='User already exists')

            # Append the new user data including name
            users_data['users'].append({'name': name, 'username': username, 'password': hashed_password})
            write_users(users_data)

            # Insert the new user into MongoDB
            users_collection.insert_one({
                'name': name,
                'username': username,
                'password': hashed_password
            })

            # Send confirmation email
            msg = Message('Registration Successful',
                          sender='your-email@gmail.com',
                          recipients=[username])
            msg.body = ('Thank you for registering!\n '
                        'Your account has been successfully created.\n' 

                        'Happy shopping, you can buy books, Electronics and Household items.')
            try:
                mail.send(msg)
                flash('Registration successful! A confirmation email has been sent to your email.', 'success')
            except Exception as e:
                print(f'Error sending confirmation email: {e}')
                flash('Registration successful, but failed to send confirmation email.', 'warning')

            return redirect(url_for('login'))

        return render_template('register.html', error='Invalid OTP or user not found')

    return render_template('register.html')

# After inserting user in MongoDB
print("Current users in database:")
for user in users_collection.find():
    print(user)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username').lower()
        password = request.form.get('password')

        print(f"Attempting to log in user: '{username}'")  # Debugging output

        users_data = read_users()  # Read users from the JSON file
        print(f"Users fetched from file: {users_data}")  # Debugging output

        # Attempt to find the user
        user = next((user for user in users_data['users'] if user['username'] == username), None)
        print(f"User found in login attempt: {user}")  # Debugging output

        if user and check_password_hash(user['password'], password):
            session['username'] = username
            session['name'] = user['name']
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'error')
            print("Invalid username or password")  # Debugging output

    return render_template('login.html')




@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')


@app.route('/reset_password/<email>', methods=['GET', 'POST'])
def reset_password(email):
    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if new_password != confirm_password:
            flash_message = 'Passwords do not match. Please try again.'
            flash_category = 'error'
            return render_template('reset_password.html', email=email, flash_message=flash_message, flash_category=flash_category)

        if update_password(email, new_password):  # Implement this function to update the password
            flash_message = 'Password successfully reset!'
            flash_category = 'success'
            return render_template('reset_password.html', email=email, flash_message=flash_message, flash_category=flash_category)
        else:
            flash_message = 'Error updating password. Please try again.'
            flash_category = 'error'
            return render_template('reset_password.html', email=email, flash_message=flash_message, flash_category=flash_category)

    return render_template('reset_password.html', email=email)

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email'].lower()  # Convert email to lowercase for consistency
        
        users_data = read_users()  # Read users from the JSON file
        users = users_data['users']  # Get the list of users

        # Check if the email exists in the user list
        if any(user['username'] == email for user in users):  # Assuming usernames are emails
            return redirect(url_for('reset_password', email=email))
        else:
            flash('Email not found.', 'error')
            return redirect(url_for('forgot_password'))

    return render_template('forgot_password.html')


def hash_password(password):
    """ Hash the password using a hashing algorithm. """
    return hashlib.sha256(password.encode()).hexdigest()

def update_password(email, new_password):
    """ Update the user's password. """
    users_data = read_users()  # Load users from the JSON file
    users = users_data['users']  # Get the list of users

    # Check if the user exists and update the password
    for user in users:
        if user['username'] == email:  # Assuming usernames are emails
            # Hash the new password before storing it
            user['password'] = hash_password(new_password)
            write_users(users_data)  # Write updated users back to the JSON file
            return True
            
    return False


def generate_otp():
    return str(random.randint(100000, 999999))






# Dummy data for items





books = [
    {"id": 1, "title": "1984", "author": "George Orwell", "price": 12.99, "image": "1984.jpg"},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee", "price": 10.99, "image": "mockingbird.jpg"},
    {"id": 3, "title": "Pride and Prejudice", "author": "Jane Austen", "price": 14.99, "image": "pride_prejudice.jpg"},
    {"id": 4, "title": "The Catcher in the Rye", "author": "J.D. Salinger", "price": 13.49, "image": "catcher_rye.jpg"},
    {"id": 5, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "price": 11.99, "image": "gatsby.jpg"},
    {"id": 6, "title": "Moby Dick", "author": "Herman Melville", "price": 15.99, "image": "moby_dick.jpg"},
    {"id": 7, "title": "War and Peace", "author": "Leo Tolstoy", "price": 19.99, "image": "war_peace.jpg"},
    {"id": 8, "title": "Crime and Punishment", "author": "Fyodor Dostoevsky", "price": 17.99, "image": "crime_punishment.jpg"},
    {"id": 9, "title": "The Hobbit", "author": "J.R.R. Tolkien", "price": 16.99, "image": "hobbit.jpg"},
    {"id": 10, "title": "Brave New World", "author": "Aldous Huxley", "price": 12.49, "image": "brave_new_world.jpg"}
]

electronics = [
    {"id": 1, "name": "Smartphone", "price": 299.99, "image": "smartphone.jpg"},
    {"id": 2, "name": "Laptop", "price": 799.99, "image": "laptop.jpg"},
    {"id": 3, "name": "Tablet", "price": 199.99, "image": "tablet.jpg"},
    {"id": 4, "name": "Smartwatch", "price": 149.99, "image": "smartwatch.jpg"},
    {"id": 5, "name": "Headphones", "price": 89.99, "image": "headphones.jpg"},
    {"id": 6, "name": "Camera", "price": 499.99, "image": "tv.jpg"},
    {"id": 7, "name": "Bluetooth Speaker", "price": 129.99, "image": "bluetooth_speaker.jpg"},
    {"id": 8, "name": "Printer", "price": 119.99, "image": "printer.jpg"},
    {"id": 9, "name": "Monitor", "price": 219.99, "image": "monitor.jpg"},
    {"id": 10, "name": "External Hard Drive", "price": 89.99, "image": "external_hard_drive.jpg"}
]

household = [
    {"id": 1, "name": "Vacuum Cleaner", "price": 149.99, "image": "vacuum.jpg"},
    {"id": 2, "name": "Blender", "price": 89.99, "image": "blender.jpg"},
    {"id": 3, "name": "Microwave", "price": 129.99, "image": "microwave.jpg"},
    {"id": 4, "name": "Air Fryer", "price": 159.99, "image": "air_fryer.jpg"},
    {"id": 5, "name": "Washing Machine", "price": 499.99, "image": "washing_machine.jpg"},
    {"id": 6, "name": "Refrigerator", "price": 899.99, "image": "refrigerator.jpg"},
    {"id": 7, "name": "Dishwasher", "price": 349.99, "image": "dishwasher.jpg"},
    {"id": 8, "name": "Coffee Maker", "price": 79.99, "image": "coffee_maker.jpg"},
    {"id": 9, "name": "Iron", "price": 49.99, "image": "iron.jpg"},
    {"id": 10, "name": "Electric Kettle", "price": 39.99, "image": "electric_kettle.jpg"}
]

# Dummy cart
cart = {
    'books': [],
    'electronics': [],
    'household': []
}


@app.route('/books-page')
def books_page():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('books.html', books=books)

@app.route('/electronics-page')
def electronics_page():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('electronics.html', electronics=electronics)

@app.route('/household-page')
def household_page():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('household.html', household=household)

@app.route('/cart')
def cart_page():
    if 'username' not in session:
        return redirect(url_for('login'))

    total_books = sum(item['price'] for item in cart['books'])
    total_electronics = sum(item['price'] for item in cart['electronics'])
    total_household = sum(item['price'] for item in cart['household'])
    total_amount = total_books + total_electronics + total_household

    if request.method == 'POST':
        # Get the selected location from the form
        location = request.form.get('location')
        
        if location:
            # Split the location into latitude and longitude
            lat, lon = map(float, location.split(','))
            
            # Make a request to the Nominatim API
            response = requests.get(f'https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json')
            address_data = response.json()
            
            # Check if the address was found
            if 'display_name' in address_data:
                address = address_data['display_name']
            else:
                address = 'Unable to retrieve address.'
        else:
            address = 'No location selected.'
        
        # Flash the address message
        flash(f'Selected Address: {address}')

    return render_template('cart.html', cart=cart, total_amount=total_amount)

@app.route('/add_to_cart/<item_type>/<int:item_id>', methods=['POST'])
def add_to_cart(item_type, item_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    item = None
    if item_type == 'books':
        item = next((b for b in books if b['id'] == item_id), None)
        if item:
            cart['books'].append(item)
    elif item_type == 'electronics':
        item = next((e for e in electronics if e['id'] == item_id), None)
        if item:
            cart['electronics'].append(item)
    elif item_type == 'household':
        item = next((h for h in household if h['id'] == item_id), None)
        if item:
            cart['household'].append(item)

    return redirect(url_for('cart_page'))

@app.route('/get_address')
def get_address():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    
    headers = {
        'User-Agent': 'YourAppName/1.0 (tradingcontentdrive.com)'  # Change this to your app's name and your email
    }

    try:
        response = requests.get(f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json", headers=headers)

        if response.status_code == 200:
            address_data = response.json()
            return jsonify(address_data)
        else:
            print(f"Error: {response.status_code}, Response: {response.text}")
            return jsonify({"error": "Unable to retrieve address."}), 500
    except Exception as e:
        print(f"Exception occurred: {e}")
        return jsonify({"error": str(e)}), 500




@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Calculate the total amount from the cart
    total_books = sum(item['price'] for item in cart['books'])
    total_electronics = sum(item['price'] for item in cart['electronics'])
    total_household = sum(item['price'] for item in cart['household'])
    total_amount = total_books + total_electronics + total_household
    
    # Get cart items to display in the payment bill
    cart_items = {
        'books': cart['books'],
        'electronics': cart['electronics'],
        'household': cart['household']
    }
    
    if request.method == 'POST':
        card_number = request.form.get('card_number')
        expiry = request.form.get('expiry')
        cvv = request.form.get('cvv')
        msg = Message('Order Confirmation',
                          sender='your-email@gmail.com',
                          recipients=[session['username']])  # Use the user's email
        msg.body = (
                f'Thank you for your order!\n\n'
                f'Order Summary:\n'
                f'Books: {total_books}\n'
                f'Electronics: {total_electronics}\n'
                f'Household: {total_household}\n'
                f'Total Amount: ${total_amount}\n\n'
                'Happy shopping! You can buy more books, electronics, and household items anytime.'
            )   
        try:
                mail.send(msg)
                flash('Confirmation email sent!', 'success')
        except Exception as e:
                print(f'Error sending email: {e}')  # Log the error
                flash('Failed to send confirmation email.', 'error')    
        # Dummy payment processing logic
        if card_number and expiry and cvv:
            return render_template('payment_bill.html', cart_items=cart_items, total_amount=total_amount)
        else:
            return render_template('checkout.html', cart_items=cart_items, total_amount=total_amount, error='Please fill all fields.')
    
    return render_template('checkout.html', cart_items=cart_items, total_amount=total_amount)

@app.route('/remove_from_cart/<item_type>/<int:item_id>', methods=['POST'])
def remove_from_cart(item_type, item_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    if item_type in cart:
        cart[item_type] = [item for item in cart[item_type] if item['id'] != item_id]

    return redirect(url_for('cart_page'))

@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')

servicemen = {
    'serviceman1': {'name': 'Manohar shetty', 'work': 'Electrician', 'place': 'Ashok nagar'},
    'serviceman2': {'name': 'Ramesh kapoor', 'work': 'Plumber', 'place': 'koramangala'},
    'serviceman3': {'name': 'Dinesh', 'work': 'Carpenter', 'place': 'Bellandur'}
}

@app.route('/support', methods=['GET', 'POST'])
def support():
    serviceman_details = None
    if request.method == 'POST':
        serviceman = request.form.get('serviceman')
        date = request.form.get('date')
        if serviceman in servicemen:
            serviceman_details = servicemen[serviceman]
        return render_template('serviceman_details.html', serviceman=serviceman_details, selected_date=date)
    return render_template('support.html', servicemen=servicemen)

@app.route('/book_serviceman', methods=['POST'])
def book_serviceman():
    if request.method == 'POST':
        serviceman = request.form.get('serviceman')
        place = request.form.get('place')
        date = request.form.get('date')
        
        # Redirect to booking confirmation page
        return redirect(url_for('booking_confirmation', serviceman=serviceman, place=place, date=date))

@app.route('/booking_confirmation')
def booking_confirmation():
    serviceman = request.args.get('serviceman')
    place = request.args.get('place')
    date = request.args.get('date')
    
    # Construct the confirmation email
    msg = Message('Booking Confirmation',
                  sender='your-email@gmail.com',
                  recipients=[session['username']])  # Replace with the user's email

    msg.body = (
        f'Your booking has been confirmed!\n'
        f'Serviceman: {serviceman}\n'
        f'Place: {place}\n'
        f'Date: {date}\n'
        'Thank you for choosing our service!'
    )
    
    try:
        mail.send(msg)
        flash('Confirmation email sent!', 'success')
    except Exception as e:
        print(f'Error sending confirmation email: {e}')
        flash('Failed to send confirmation email.', 'error')

    return render_template('booking_confirmation.html', serviceman=serviceman, place=place, date=date)


  # Set your secret key for session management

# Initialize user_data dictionary
# Initialize user_data dictionary
@app.route('/account_info', methods=['GET', 'POST'])
def account_info():
    # Initialize user_data in session if it doesn't exist
    if 'user_data' not in session:
        session['user_data'] = {
            'username': 'default_username',
            'email': 'default_email@example.com',
            'phone': 'default_phone',
            'address': 'default_address'
        }

    if request.method == 'POST':
        # Handle form submission
        username = request.form.get('username')
        email = request.form.get('email')
        phone = request.form.get('phone')  # New field for phone number
        address = request.form.get('address')  # New field for address
        password = request.form.get('password')  # Assuming you want to handle passwords

        # Update user information in session
        session['user_data']['username'] = username
        session['user_data']['email'] = email
        session['user_data']['phone'] = phone  # Store phone number
        session['user_data']['address'] = address  # Store address

        # Optionally, handle password storage here

        flash('Account information updated successfully.')
        return redirect(url_for('profile'))

    # Pass user data to the template for GET request
    return render_template('account_info.html', user=session['user_data'])

@app.route('/profile')
def profile():
    return render_template('profile.html', user=session['user_data'])


@app.route('/orders', methods=['GET', 'POST'])
def orders():
    if 'username' not in session:
        return redirect(url_for('login'))

    total_books = sum([item['price'] for item in cart['books']])
    total_electronics = sum([item['price'] for item in cart['electronics']])
    total_household = sum([item['price'] for item in cart['household']])
    
    total_price = total_books + total_electronics + total_household

    return render_template('orders.html', cart=cart, total_price=total_price)


if __name__ == '__main__':
    app.run(debug=True)