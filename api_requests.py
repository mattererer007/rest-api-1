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







