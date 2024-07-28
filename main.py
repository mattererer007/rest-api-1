import api_requests as api
from app2 import test_connection, check_and_create_table, create_character, RMCharacter, get_db
from json_cleanup import messify_json as mj
import json

# To pull a smple of data
def display_data():
    characters = api.Character().get_and_combine_all_data()

    messy_characters = mj.messifydata(characters)

    clean_characters = mj.cleanifydata(messy_characters)

    with open("file.txt", "w") as file:
        json.dump(clean_characters, file, indent=4)

# ensure that database connection is working
def test_db():

    # check_and_create_table()
    test_connection()
    check_and_create_table()

# actually run program
def main():
    # # Create an instance of the Base class
    characters = api.Character().get_and_combine_all_data()

    messy_characters = mj.messifydata(characters)

    clean_characters = mj.cleanifydata(messy_characters)

    test_connection()

    # Input all characters from clean 
    db = get_db()
    for character in clean_characters:
        try:
            create_character(db, character)
        except Exception as e:
            print(f"Error when adding {character['name']}: {e}")
    db.close()

if __name__ == '__main__':
    main()