import random
import re
import inflect
import copy
from datetime import datetime


class messify_json:

    ## mess the data UP so you can practice cleaning it
    def messifydata(json_input: list) -> list:

        p = inflect.engine()

        messy_list = copy.deepcopy(json_input)

        for char in messy_list:
            if random.choice([True, False]): # Mess with the case
                char['name'] = char['name'].upper()
            if random.choice([True, False]): # Mess with the space between words
                pattern = r'(\b\w+\b) (\b\w+\b)'
                replacement = r'\1' + ' ' * (random.randint(1,4)) + r'\2'
                if re.match(pattern, char["name"]): # Add space to the beginning of a name
                        char["name"] = re.sub(pattern, replacement,char["name"])
                else: char['name'] = "  " + char['name']
            if random.choice([True, False]): # create blank name
                char['name'] = None
            if random.choice([True, False]): # create blank status
                char['status'] = None
            if random.choice([True, False]): # Mess with the location
                char["origin"]["name"] = char["origin"]["name"].lower()
            if random.choice([True, False]): # create blank status
                char["origin"]["name"] = None
            if random.choice([True, False]):
                if random.choice([True, False]):
                    char["id"] = str(char["id"])
                else: char["id"] = p.number_to_words(char["id"])

        return messy_list

    def cleanifydata(json_input: list) -> list:

        cleaned_data = []
        inputs = set()

        for char in json_input:
            if char['name'] is not None: 
                cleaned_char = {}


                # Prepare id
                if isinstance(char['id'],int):
                    cleaned_char['id'] = char['id']
                elif isinstance(char['id'], str):
                    try:
                        cleaned_char['id'] = int(char['id'])
                    except ValueError:
                        continue

                # prepare name
                pattern = r'\s+'
                if isinstance(char['name'], str):
                    name = re.sub(pattern, ' ', char['name']).strip().title()
                    cleaned_char['name'] = name

                # prepare status
                if char['status'] is None or not isinstance(char['status'],str):
                    cleaned_char['status'] = 'Unknown'
                else: cleaned_char['status'] = char['status'].strip().title()

                # prepare species
                if char['species'] is None or not isinstance(char['species'],str):
                    cleaned_char['species'] = 'Unknown'
                else: cleaned_char['species'] = char['species'].strip().title()

                # prepare gender
                if char['gender'] is None or not isinstance(char['gender'],str):
                    cleaned_char['gender'] = 'Unknown'
                else: cleaned_char['gender'] = char['gender'].strip().title()

                # prepare origin
                if char['origin']['name'] is None or not isinstance(char['origin']['name'],str):
                    cleaned_char['origin'] = 'Unknown'
                else: cleaned_char['origin'] = char['origin']['name'].strip().title()

                # prepare current location
                if char['location']['name'] is None or not isinstance(char['location']['name'],str):
                    cleaned_char['current location'] = 'Unknown'
                else: cleaned_char['current location'] = char['location']['name'].strip().title()

                # grab episode for extra fun
                pattern = r'(\d+)$'
                match = re.search(pattern, char['url'])
                if not match:
                    cleaned_char['first episode'] = 0
                else: cleaned_char['first episode'] = int(match.group(1))

                if 'created' in char and isinstance(char['created'], str):
                    try:
                        current_dt = datetime.strptime(char['created'],'%Y-%m-%dT%H:%M:%S.%fZ')
                        cleaned_char['date found'] = current_dt.strftime('%Y-%m-%d')
                    except ValueError:
                        cleaned_char['date found'] = "0000-00-00"
                else: cleaned_char['date found'] = "0000-00-00" 
                

                # Check for duplicates
                single_string = cleaned_char['name'] + cleaned_char['status'] + cleaned_char['species'] + cleaned_char['gender']        
                
                if single_string not in inputs:
                    inputs.add(single_string)
                    cleaned_data.append(cleaned_char)
        
        return cleaned_data







                


                





               
            

            
                 

            



    ##cleanify
    # convert episode string into an integer  (i.e., https://rickandmortyapi.com/api/episode/27 > 27)
    # Standardize name
    # Standardize age to be an int
    # standardize date
    # Manage missing values > must have name and location
    # if location only missing change to 'Unknown'
    