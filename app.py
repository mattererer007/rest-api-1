from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import text
import os

# Initialize Flask
app = Flask(__name__)

#Database Configuration
DB_USER = "postgres"
DB_PW = "oconnellcrew"
DB_NAME = "postgres"
DB_HOST = "postgres-1.c7uq26a4i035.us-east-2.rds.amazonaws.com"
DB_PORT = "5432"

# connect to database with a string in the format of dialect+driver://username:password@host:port/database 
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{DB_USER}:{DB_PW}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Disable tracking to use less memory and focus on core part of code

db = SQLAlchemy(app)
ma = Marshmallow(app)


@app.route('/')
def check_connection():
    try:
        print("Trying to connect to the database...")
        # Perform a simple query to check the connection
        result = db.session.execute(text('SELECT 1'))
        print("Database connection successful!")
    except Exception as e:
        print(f"Database connection failed: {e}")
    
class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    species = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100), nullable=False)
    origin = db.Column(db.String(100), nullable=False)
    current_location = db.Column(db.String(200), nullable=False)

    def __init__(self, name, type, species, status, origin, current_location):
        self.name = name
        self.type = type
        self.species = species
        self.status = status
        self.origin = origin
        self.current_location = current_location

class CharacterSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Character

character_schema = CharacterSchema()
characters_schema = CharacterSchema(many=True)

# Create the database tables
def create_tables():
    db.create_all()
    app.tables_created = True

# Create a way to add a new character (POST)

# Create a way to delete a character by ID

# Create a way to update a character 
