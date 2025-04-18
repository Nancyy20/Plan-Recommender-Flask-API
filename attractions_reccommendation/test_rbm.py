from rbm import *
import pandas as pd

def recommend_attraction_place(user_id, city):
    attractions_data = pd.read_csv('attractions.csv')
    ratings_data = pd.read_csv('user_profiling3010.csv')  # all ratings 5

    df = rbm(attractions_data, ratings_data, city, user_id)
    # print(type(df))
    df = df['attraction_id']
    return df


d = recommend_attraction_place(1,'cairo')
d.count()