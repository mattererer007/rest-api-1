import requests
import json

"""This file provides a series of classes that will enable a user to pull data from the official Rick and Morty to then clean the data and post to a database """

base_url = "https://rickandmortyapi.com/api"
characters_url = base_url + "/character"
locations_url = base_url + "/location"
episodes_url = base_url + "/episode"

class Base:
    def __init__(self):
        self.base_url = base_url
    
    # Determine the different URLs avaialble to source data from in Rick and Morty API
    def api_info(self):
        return requests.get(url=self.base_url).json()

class Character:
    def __init__(self):
        self.char_url = characters_url
        self.page_count = requests.get(url=self.char_url).json()['info']['pages']

    # Get summary view of api call
    def schema(self):
        temp = requests.get(url=self.char_url).json()
        return temp['info']

    # Pull entire JSON file in form of dicitonary (hashmap) organized by page 
    def get_all(self) -> dict:

        map = {}
        for i in range(1, self.page_count+1):
            map[i] = requests.get(url=self.char_url + "/?page=" + str(i)).json()

        return map
    
    # Pull single page
    def get_page(self, number: int = None) -> dict:

        if number is None:
            return requests.get(url=self.char_url).json()
        
        if number > self.page_count or number < 1:
            return None
        
        return requests.get(url=self.char_url + "/?page=" + str(number)).json()
    
    def get_single_character(self, id: int) -> dict:
        
        if id is None:
            return None
        
        result = requests.get(url=self.char_url + "/" + str(id)).json()

        return result
    
    # Pull API data in a single JSON file
    def get_and_combine_all_data(self):

        pages_data = []
        page = 1

        while page <= self.page_count:
            try:
                response = requests.get(url=self.char_url + "/?page=" + str(page))
                response.raise_for_status() # Make sure that request was made
                data = response.json()
                results = data["results"]
                for char in results:
                    pages_data.append(char)
            except requests.exceptions.HTTPError as http_err:
                    print(f"HTTP error occurred: {http_err}")
            except Exception as e:
                print(f"Other error occurred: {e}")
            
            page += 1

        return pages_data

















