import requests

def fetch_anime_info(anime_name):
    url = 'https://api.jikan.moe/v4/anime'
    params = {'q': anime_name, 'limit': 1}
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        return None, f"Failed to fetch data from Jikan API: {response.status_code}"
    
    data = response.json().get('data', [])
    if not data:
        return None, "No data found for the given anime name."
    
    return data[0], None  
