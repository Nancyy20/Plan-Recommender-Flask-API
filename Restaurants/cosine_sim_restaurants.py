import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.metrics.pairwise import cosine_similarity


df = pd.read_csv(r"E:\FCIS\GP\GP\TravelRecommeder_Flask-master\Restaurants\Allrestaurants.csv", encoding='latin1')

#print(df.head())

# fill missing values in the "cuisines" column
df["cuisines"].fillna("", inplace=True)

# create a CountVectorizer object to transform the "cuisines" column into a matrix of word counts
cv = CountVectorizer(stop_words='english')
count_matrix = cv.fit_transform(df["cuisines"])

# compute the cosine similarity matrix between all pairs of restaurants based on their cuisine
similarity = cosine_similarity(count_matrix)

# create a function that takes in restaurant ID and number of recommendations as inputs and returns a list of the most similar restaurants in the same city
def get_recommendations(restaurant_id, n=20, cosine_sim=similarity):
    # get the city of the restaurant
    city = df[df['restID'] == restaurant_id]['city'].values[0]

    # select only the restaurants that match the same city
    df_city = df[df['city'] == city]

    # get the index of the restaurant that matches the restaurant ID
    restaurant_index = df_city.index[df_city['restID'] == restaurant_id].tolist()[0]

    # get the pairwise similarity scores of all restaurants in the same city and sort the restaurants based on the similarity scores
    sim_scores_all = sorted(list(enumerate(cosine_sim[restaurant_index])), key=lambda x: x[1], reverse=True)

    # filter the restaurants by city
    sim_scores_city = [(i, score) for i, score in sim_scores_all if df.iloc[i]['city'] == city]

    # check if recommendations are limited
    if n > 0:
        sim_scores_city = sim_scores_city[1:n + 1]

    # get the restaurant indices of the top similar restaurants
    restaurants_indices = [i[0] for i in sim_scores_city]
    scores = [i[1] for i in sim_scores_city]

    # create a DataFrame of the top similar restaurants and their similarity scores
    top_restaurants = pd.DataFrame(df.iloc[restaurants_indices][['restID', 'name', 'city']])
    top_restaurants['sim_scores'] = scores
    top_restaurants['ranking'] = range(1, len(top_restaurants) + 1)
    return top_restaurants['restID'].tolist()

