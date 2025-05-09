import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
all_hotels = pd.read_csv(r"C:\Users\Salah Ashraf\PycharmProjects\TravelRecommeder_Flask\Hotels\AllhotelswithImg.csv", encoding='latin1')



def get_recommendation(hotel_id,number=20):

    hotel_ids = []
    count_vectorizer = CountVectorizer()
    count_matrix = count_vectorizer.fit_transform(all_hotels["amenities"].apply(lambda count_matrix: np.str_(count_matrix)))


    cosine_sim = cosine_similarity(count_matrix)
    hotel_index = hotel_id
    name = get_hotelName_from_index(hotel_index)
    city = get_city_from_hotelName(hotel_index)
    similar_hotels = list(enumerate(cosine_sim[hotel_index]))

    sorted_similar_hotels = sorted(similar_hotels, key=lambda x: x[1], reverse=True)

    hotel_name = get_hotelName_from_index(hotel_index)
    i = 0
    for hotel in sorted_similar_hotels:
        name_of_hotel = get_hotelName_from_index(hotel[0])
        city_of_hotel = get_city_from_hotelName(hotel[0])
        if( name_of_hotel == hotel_name or city_of_hotel != city):
            continue
        hotel_ids.append(hotel[0])

        i = i + 1
        if (i == number):
            break
    # for id in hotel_ids:
    #     print(id)
    return hotel_ids


def get_index_from_hotelName(name):
    return all_hotels[all_hotels.name == name]["ID"].values[0]

def get_city_from_hotelName(name):
    return all_hotels[all_hotels.ID == name]["City"].values[0]

def get_hotelName_from_index(index):
    return all_hotels[all_hotels.ID == index]["name"].values[0]

def print_hotel_details(name):
    return all_hotels[all_hotels.name == name]["name"].values[0],all_hotels[all_hotels.name == name]["ratings"].values[0],all_hotels[all_hotels.name == name]["Price Range"].values[0]



