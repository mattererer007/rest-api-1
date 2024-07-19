import api_requests as api

# Create an instance of the Base class
character = api.Character()

# Call the api_info method and print the result
print(character.get_page(2))