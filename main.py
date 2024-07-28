import api_requests as api
from app import db, check_connection, app, Character, create_tables
from json_cleanup import messify_json as mj
import sqlalchemy
import json

# Going forward proceed to use the CRUD tasks to push update and delete characters

# Create a way to identify duplicates dn delete

# Create a way to captialize all letters in Origin 

# Check for characters with a blank type "" and replace with unknown

## Tuesday
# Practice pushing

def main():
    # # Create an instance of the Base class
    character = api.Character()

    with app.app_context():

        # Check database connection
        check_connection()
        try: 
            result = character.get_page(2)

            for item in result['results']:
                character = Character(
                    name = item["name"],
                    type = item["type"],
                    species = item["species"],
                    status = item["status"],
                    origin = item["origin"]["name"],
                    current_location=item["location"]["name"]
                )
                db.session.add(character)
                print(item["name"], " added")
            db.session.commit()
        except Exception as e:
            print(f"An error occurred: {e}") 

def make_messy_data():

    characters = api.Character().get_and_combine_all_data()

    messy_characters = mj.messifydata(characters)

    with open("messy.txt", "w") as file:
        json.dump(messy_characters, file, indent=4)

    clean_characters = mj.cleanifydata(messy_characters)

    with open("clean.txt", "w") as file:
        json.dump(clean_characters, file, indent=4)



    

    


def see_database():
    with app.app_context():
        # Query all characters
        characters = Character.query.all()

        # Print each character
        for character in characters:
            print(f"ID: {character.id}, Name: {character.name}, Type: {character.type}, Species: {character.species}, Status: {character.status}, Origin: {character.origin}, Current Location: {character.current_location}")


if __name__ == '__main__':
    make_messy_data()      

