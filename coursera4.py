import requests_with_caching
import json

def get_movies_from_tastedive(movie_name):
    parameters = {"q": movie_name, "type": "movies", "limit": 5}
    responses = requests_with_caching.get("https://tastedive.com/api/similar", params=parameters)
    page = json.loads(responses.text)
    return page

def extract_movie_titles(dictionary):
    movie_list=[]
    for movie in dictionary["Similar"]["Results"]:
        movie_list.append(movie["Name"])
    return movie_list

def get_related_titles(movie_title_list):
    updated_lst=[]
    for title in movie_title_list:
        x=get_movies_from_tastedive(title)
        y=extract_movie_titles(x)
        for movie_title in y:
            if movie_title not in updated_lst:
                updated_lst.append(movie_title)
    return updated_lst

def get_movie_data(movie_name):
    parameters = {'t': movie_name, 'r': 'json'}
    resp = requests_with_caching.get('http://www.omdbapi.com/', params=parameters)
    data = json.loads(resp.text)
    return data

def get_movie_rating(movie_dict):
    if len(movie_dict['Ratings']) > 1:
        if movie_dict['Ratings'][1]['Source'] == 'Rotten Tomatoes':
            return int(movie_dict['Ratings'][1]['Value'][:2])
        else:
            return 0
    else:
        return 0

def get_sorted_recommendations(listMovieTitle):
    listMovie= get_related_titles(listMovieTitle)
    listMovie= sorted(listMovie, key = lambda movieName: (get_movie_rating(get_movie_data(movieName)), movieName), reverse=True)
    return listMovie
    
print(get_sorted_recommendations(["Bridesmaids", "Sherlock Holmes"]))

