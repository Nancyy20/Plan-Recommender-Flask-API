from Hotels.Hotels_MF_ALS import *
import pandas as pd

#TEST CODE FOR HOTELS
from Restaurants.Restaurants_MF_ALS import*
from attractions_reccommendation.rbm import rbm

csvHotelInfo = "Hotels/Allhotels.csv"
csvRatingInfo = 'Hotels/user_profiling.csv'

newUser = []

newUser.append(
               {
                   'user_id': 2709,
                   'hotel_id':3,
                   'rating': 5,
                   'flag': 'F',
                   'city':'Cairo'

               })
# pd.DataFrame(newUser).to_csv('Hotels/user_profile_Data/user_profiling_AlFay.csv', index=False, mode='a', header=False)
#when entering a new user we do have to retrain the entire model
ratingsSpark,hotels = initial_files(csvHotelInfo, csvRatingInfo)
calculateSparsity(ratingsSpark)
train,test= dataSplit(ratingsSpark)
best_model =MF_ALS(train,test)

# recommendations(best_model,1,hotels,'Al-Fayyum')


def recommend_hotel(user_id, city):
    csvHotelInfo = "Hotels/Allhotels.csv"
    csvRatingInfo = 'Hotels/user_profile_Data/user_profiling307.csv'

    # pd.DataFrame(newUser).to_csv('Hotels/user_profile_Data/user_profiling_AlFay.csv', index=False, mode='a',
    #                              header=False)
    # when entering a new user we do have to retrain the entire model
    ratingsSpark, hotels = initial_files(csvHotelInfo, csvRatingInfo)
    calculateSparsity(ratingsSpark)
    train, test = dataSplit(ratingsSpark)
    best_model = MF_ALS(train, test)
    # df=pd.DataFrame(recommendations(best_model,user_id,hotels,city))
    # arr=df.to_numpy()
    return recommendations(best_model,user_id,hotels,city)


def recommend_restaraurnat(user_id, city):
    csvRestaurantInfo = "Restaurants/Cairo_Final_Clean_Updated.csv"
    csvRatingInfo = 'Restaurants/user_profiling_rest.csv'
    ratingsSpark, restaurants = initial_files_Rest(csvRestaurantInfo, csvRatingInfo)
    calculateSparsityRest(ratingsSpark)
    train, test = dataSplit_Rest(ratingsSpark)

    best_model = MF_ALS_Rest(train, test)
    print("-----------------")
    print(best_model)
    return recommendationsRest(best_model,user_id,restaurants, city)



def recommend_attraction_place(user_id, city):
    attractions_data = pd.read_csv('attractions_reccommendation/attractions.csv')
    ratings_data = pd.read_csv('attractions_reccommendation/user_profiling3011.csv')  # all ratings 5

    df = rbm(attractions_data, ratings_data, city, user_id)
    # print(type(df))
    # df = df['attraction_id']

    print("Data frame: ")
    print("---------------------------------")
    print(df)
    print("-------------------")
    # restID_array = [row.restID for row in user_recs_array]
    return df['attraction_id']

#TEST CODE FOR RESTAURANTS

#TEST CODE FOR ATTRACTIONS