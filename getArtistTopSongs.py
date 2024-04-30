# Written by Owen Finucan
# Note: Need .env that contains string of client_id and client_secret - not including for obvious reasons

from dotenv import load_dotenv
import os
import base64
import json
from requests import post, get

load_dotenv()

# retrieving the client id & secret
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# accessing the token from spotify
def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization" : "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}

    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

# getting the authorization header w/ inputted token
def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

token = get_token()

# searching for the artist given your token & a string of the artists name
def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)

    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]

    if len(json_result) == 0:
        print("Artist does not exist")
        return None
    
    return json_result[0]

# retrieving the artist data
# input your token, the artist's id, and arguement (what data to retrieve)
def get_artist_data(token, artist_id, arguement):

    headers = get_auth_header(token)
    if arguement == "tracks":
        url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
        result = get(url, headers=headers)
        json_result = json.loads(result.content)
        return json_result['tracks']
    else:
        url = f"https://api.spotify.com/v1/artists/{artist_id}"
        result = get(url, headers=headers)
        json_result = json.loads(result.content)
        if arguement == "genres":
            return json_result['genres']
        elif arguement == "followers":
            return json_result['followers']['total']
    

# get & print top ten songs given your token & artist id
def print_top_ten_songs(token, artist_id):

    songs = get_artist_data(token, artist_id, 'tracks')

    for idx, song in enumerate(songs):
        print(f"{idx + 1}.{song['name']}")


# get & print the artists genres given your token & artist id
def print_artist_genres(token, artist_id):

    genres = get_artist_data(token, artist_id, 'genres')

    print("Genres: ")

    for genre in genres:
        print(f"- {genre}")

# get & print the number of followers given your token & artist id
def print_num_followers(token, artist_id):

    followers = get_artist_data(token, artist_id, 'followers')

    print(f"Number of Followers: " + str(followers))

# ---------------------------------------------------------------------------------------------------------------------
# main loop

while True:
    artist_name = input("Enter an artist's name exactly (with appropriate capital letters when applicable) on one line or exit to exit ")

    # if exit --> exit
    if artist_name == "exit":
        break

    # search for the artist then get the artist's id
    result = search_for_artist(token, artist_name)
    artist_id = result["id"]

    # if not artist exists under than name --> print error message
    if result == None:
        print("No artist was found under that name ")
        
    # if artist if found...
    else:

        # loop to continue to access inputted artist's data
        while True:

            # option for what data to print out from given artist
            print("1. Top 10 most streamed songs by " + artist_name)
            print("2. " + artist_name + "'s genres according to Spotify")
            print("3. Number of followers " + artist_name + " has on Spotify")
            print("4. Exit")

            arguement = input("What would you like to see from " + artist_name + "? Press the number you want to see ")
            
            # dependent on what was inputted --> print that data or exit
            if arguement == "1":
                print_top_ten_songs(token, artist_id)

            elif arguement == "2":
                print_artist_genres(token, artist_id)
                
            elif arguement == "3":
                print_num_followers(token, artist_id)

            elif arguement == "4":
                break

            elif arguement == "exit":
                break

            # catch all --> if invalid number is entered
            else:
                print("Try a different number")

            print("")