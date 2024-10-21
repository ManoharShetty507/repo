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

username = 'admin123'  # Your MongoDB username
password = 'admin123'  # Replace with your actual password

# URL encode the password to handle special characters
password_encoded = quote_plus(password)

# Use the encoded password in the connection string
client = MongoClient(f"mongodb+srv://{username}:{password_encoded}@cluster0.yfy4u.mongodb.net/myDatabaseName?retryWrites=true&w=majority&appName=Cluster0")
# If using Flask, this would be your MONGO_URI configuration
app.config["MONGO_URI"] = f"mongodb+srv://{username}:{password_encoded}@cluster0.yfy4u.mongodb.net/myDatabaseName?retryWrites=true&w=majority&appName=Cluster0"

db = client['myDatabaseName']
try:
    client.admin.command('ping')
    print("MongoDB connection successful!")
except Exception as e:
    print(f"Error while connecting to MongoDB: {e}")

@app.route('/check_mongo')
def check_mongo_connection():
    # Additional logic for checking MongoDB connection can go here
    return "MongoDB connection checked!"
users_collection = db['users']  