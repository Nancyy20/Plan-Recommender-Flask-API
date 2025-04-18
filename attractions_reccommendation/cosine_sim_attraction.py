import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.metrics.pairwise import cosine_similarity
df = pd.read_csv(r"C:\Users\Salah Ashraf\PycharmProjects\TravelRecommeder_Flask\attractions_reccommendation\attractions_with_images.csv", encoding='latin1')
# 
#print(df.head())


# create a CountVectorizer object to transform the "keywords" column into a matrix of word counts
cv = CountVectorizer(stop_words='english')
count_matrix = cv.fit_transform(df["keywords"])

# compute the cosine similarity matrix between all pairs of attractions based on their keywords
similarity = cosine_similarity(count_matrix)

# create a function that takes in attraction ID and number of recommendations as inputs and returns a list of the most similar attractions in the same city
def get_recommendations(attraction_id, n=20, cosine_sim=similarity):
    # get the city of the attraction
    city = df[df['attraction_id'] == attraction_id]['city'].values[0]

    # select only the attractions that match the same city
    df_city = df[df['city'] == city]

    # get the index of the attraction that matches the attraction ID
    attraction_index = df_city.index[df_city['attraction_id'] == attraction_id].tolist()[0]

    # get the pairwise similarity scores of all attractions in the same city and sort the attractions based on the similarity scores
    sim_scores_all = sorted(list(enumerate(cosine_sim[attraction_index])), key=lambda x: x[1], reverse=True)

    # filter the attractions by city
    sim_scores_city = [(i, score) for i, score in sim_scores_all if df.iloc[i]['city'] == city]

    # check if recommendations are limited
    if n > 0:
        sim_scores_city = sim_scores_city[1:n + 1]

    # get the attraction indices of the top similar attractions
    attraction_indices = [i[0] for i in sim_scores_city]
    scores = [i[1] for i in sim_scores_city]

    # create a DataFrame of the top similar attractions and their similarity scores
    top_attractions_df = pd.DataFrame(df.iloc[attraction_indices][['attraction_id', 'attraction_name', 'city']])
    return top_attractions_df['attraction_id'].tolist()
# generate a list of recommendations for a specific attraction name
# attraction_name = 'The Hanging Church'
# top_attractions_df = get_recommendations(attraction_name, 20)
# attraction_name = 'The Hanging Church'
# top_attractions_df = get_recommendations(attraction_name, 20)

# print(type(top_attractions_df))
# print((top_attractions_df))



# list of attractions a user has liked
#attractions_list = ['Abdeen Palace Museum', 'Al-Azhar Park', 'Mosque of Muhammad Ali']

# create a copy of the attractions dataframe and add a column in which we aggregated the scores
#user_scores = pd.DataFrame(df['attraction_name'])
#user_scores['sim_scores'] = 0.0

# top number of scores to be considered for each attractions
#number_of_recommendations = 20
#for attraction_name in attractions_list:
 #   top_attractions_df, _ = get_recommendations(attraction_name, number_of_recommendations)
    # aggregate the scores
  #  user_scores = pd.concat([user_scores, top_attractions_df[['attraction_name', 'sim_scores']]]).groupby(['attraction_name'], as_index=False).sum({'sim_scores'})

# sort and print the aggregated scores
#top_attractions_per_user_df = user_scores.sort_values(by='sim_scores', ascending=False)[1:20]
#df = top_attractions_per_user_df[top_attractions_per_user_df.attraction_name.isin(attractions_list) == False]
#print(top_attractions_per_user_df)
#print(df)