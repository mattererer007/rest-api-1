from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database Configuration
DB_USER = "postgres"
DB_PW = "oconnellcrew"
DB_NAME = ""
DB_HOST = "postgres-1.c7uq26a4i035.us-east-2.rds.amazonaws.com"
DB_PORT = "5432"

# Construct the database URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PW}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Setup SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the User model
class RMCharacter(Base):
    __tablename__ = 'rmcharacters'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    status = Column(String, index=True)
    species = Column(String, index=True)
    gender = Column(String, index=True)
    origin = Column(String, index=True)
    current_location = Column(String, index=True)
    first_episode = Column(Integer, index=True)
    

# Create the database and tables
# Base.metadata.create_all(bind=engine)

# Create a database session
def get_db():
    db = SessionLocal()
    try:
        return db
    except Exception as e:
        db.close()
        raise e


# Create a function to test connection
def test_connection():
    try:
        engine = create_engine(DATABASE_URL)
        connection = engine.connect()
        print("Connection successful!")
        connection.close()
    except Exception as e:
        print(f"Error connecting to the database: {e}")


# Check if table exists... if not create it
def check_and_create_table():
    inspector = inspect(engine)
    if 'rmcharacters' not in inspector.get_table_names():
        print("Creating 'rmcharacters' table now")
        Base.metadata.create_all(bind=engine)
        print("table complete")
    else:
        print("'rmcharacters' table already exists")

# Function to create a new user
# Function to create a new character
def create_character(db, char_data):

    # Check if the character already exists
    existing_character = db.query(RMCharacter).filter_by(id=char_data["id"]).first()
    if existing_character:
        existing_character.name = char_data["name"]
        existing_character.status = char_data["status"]
        existing_character.species = char_data["species"]
        existing_character.gender = char_data["gender"]
        existing_character.origin = char_data["origin"]
        existing_character.current_location = char_data["current location"]
        existing_character.first_episode = char_data["first episode"]
        db.commit()
        db.refresh(existing_character)
        return existing_character

    new_character = RMCharacter(
        id=char_data["id"],
        name=char_data["name"],
        status=char_data["status"],
        species=char_data["species"],
        gender=char_data["gender"],
        origin=char_data["origin"],
        current_location=char_data["current location"],
        first_episode=char_data["first episode"],
    )
    db.add(new_character)
    db.commit()
    db.refresh(new_character)
    return new_character

# Setup Flask app
app = Flask(__name__)


@app.post("/rmcharacters/")
def add_rmcharacter():
    char_data = request.json
    db = get_db()
    character = create_character(db, char_data)
    db.close()
    return jsonify({
        "id": character.id,
        "name": character.name,
        "status": character.status,
        "species": character.species,
        "gender": character.gender,
        "origin": character.origin,
        "current location": character.current_location,
        "first episode": character.first_episode
    })

if __name__ == "__main__":
    check_and_create_table()
    app.run(debug=True)
