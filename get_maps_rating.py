import sys
import googlemaps
import pandas as pd
from tqdm import tqdm

gmaps = googlemaps.Client(key='GMAPS_API_KEY')


def read_raw_data(filename):
    kozvetito = pd.read_csv(filename)
    kozvetito = kozvetito.replace('\n', ' ', regex=True)
    return kozvetito


def read_previous_data(filename):
    kozvetito = pd.read_csv(filename)
    return kozvetito


def get_maps_rating(places):
    rating = []
    for place in tqdm(places["Name"]):
        try:
            result = gmaps.find_place(input=place, input_type="textquery",
                                      fields=["name", "formatted_address", "rating"])
            if result['status'] != 'ZERO_RESULTS':
                rating.append(result['candidates'][0].get('rating'))
            else:
                rating.append(0)
        except:
            print("Oops!", sys.exc_info()[0], "occurred.")
            print(f"Current query: {place}")
            print(f"API response: {result}")
            raise
    places['Rating'] = rating
    print(places.head(20))
    places.to_csv(r'Headhunters_with_Rating.csv', index=False)


def update_maps_rating(places):
    rating = []
    num_ratings = []
    for name, city, postcode in tqdm(zip(places["Name"], places["Postcode"],
                                         places["City"]), total=len(places["Name"])):
        query = f"{name} {city} {postcode}"
        try:
            result = gmaps.find_place(input=query, input_type="textquery",
                                      location_bias="circle:500000@47.18378010234081,19.49691383969245",
                                      fields=["name", "formatted_address", "rating", "user_ratings_total"])
            if result['status'] != 'ZERO_RESULTS':
                rating.append(result['candidates'][0].get('rating'))
                num_ratings.append(result['candidates'][0].get('user_ratings_total'))
            else:
                rating.append(0)
                num_ratings.append(0)
        except:
            print("Oops!", sys.exc_info()[0], "occurred.")
            print(f"Current query: {query}")
            print(f"API response: {result}")
            raise
    places['Rating'] = rating
    places['Total Ratings'] = num_ratings
    print(places.head(20))
    places.to_csv(r'Headhunters_with_Rating.csv', index=False)


FILENAME = r'Headhunters_with_Rating.csv'
update_maps_rating(read_previous_data(FILENAME))
