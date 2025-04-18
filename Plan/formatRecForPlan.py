import os
from datetime import datetime
from Hotels.Hotels_MF_ALS import *
from Restaurants.Restaurants_MF_ALS import *
from Restaurants.Restaurants_MF_ALS import hello
import pandas as pd
from attractions_reccommendation import rbm
from datetime import datetime

script_dir = os.path.dirname(os.path.abspath(__file__))  # Path to the 'Plan' directory
project_root = os.path.dirname(script_dir)  # Path to the project root

def getRecommendationForPlanRest (userID, City):
    csvRestInfo = os.path.join(project_root, 'Plan','Allrestaurants2.csv')
    timesCsv = os.path.join(project_root, 'Plan','Allrestaurants3.csv')
    timesSpark = spark.read.csv(timesCsv, header=True)
    csvRatingInfoRest = os.path.join(project_root, 'Restaurants','user_profiling_rest.csv')
    # when entering a new user we do have to retrain the entire model
    ratingsSparkRest, rest = initial_files_Rest(csvRestInfo, csvRatingInfoRest)
    calculateSparsityRest(ratingsSparkRest)
    trainR, testR = dataSplit_Rest(ratingsSparkRest)
    print('train r and test r===================================')
    print(trainR.count())
    print(testR.count())
    best_model = MF_ALS_Rest(trainR, testR)

    df = recommendationsRestPlan(best_model, userID, rest, City, timesSpark)
    print('getRecommendationForPlanRest+++++++++++\n', df.count())
    return df


def convert_time_format(time_str):
    try:
        # try parsing with format '%I:%M%p'
        time_obj = datetime.strptime(str(time_str), '%I:%M%p')
    except ValueError:
        try:
            # try parsing with format '%I:%M %p'
            time_obj = datetime.strptime(str(time_str), ' %I:%M %p ')
        except ValueError:
            # raise an error if time string cannot be parsed
            try:
                # try parsing with format '%I:%M %p'
                time_obj = datetime.strptime(str(time_str), '%I:%M %p')
            except ValueError:
                # raise an error if time string cannot be parsed
                try:
                    # try parsing with format '%I:%M %p'
                    time_obj = datetime.strptime(str(time_str), ' %I:%M %p')
                except ValueError:
                # raise an error if time string cannot be parsed
                  raise ValueError(f"Invalid time format: {time_str}")
    return time_obj.strftime('%I%p')

def changeTimeFormat(df):
    df['open_time'] = df['open_time'].apply(convert_time_format).str.replace('^0', '', regex=True)
    df['close_time'] = df['close_time'].apply(convert_time_format).str.replace('^0', '', regex=True)

def formatRecommendations (city,id):
    restaurants_df = getRecommendationForPlanRest(id, city)


    attractions_data_path = os.path.join(project_root, 'attractions_reccommendation', 'attractions.csv')
    print(f"Attempting to load attractions data from: {attractions_data_path}")
    print(f"Attempting to load attractions data from: {script_dir}")
    print(f"Attempting to load attractions data from: {os.path.abspath(__file__)}")

    attractions_data = pd.read_csv(attractions_data_path)
    print('data================>\n',attractions_data.head())

    ratings_data_path=os.path.join(project_root, 'attractions_reccommendation','user_profiling3010.csv')
    ratings_data = pd.read_csv(ratings_data_path)
    attractions_df = rbm.rbm(attractions_data, ratings_data, str.lower(city), id)
    restaurants_df_pandas = restaurants_df.toPandas()
    changeTimeFormat(restaurants_df_pandas)
    data = {
        "restaurants": [],
        "attractions": []
    }
    # Extract information from restaurants dataframe and add to dictionary
    for _, row in restaurants_df_pandas.iterrows():
        restaurant = {
            "name": row['name'],
            "location": (row['latitude'], row['longitude']),
            "open_time": row['open_time'],
            "close_time": row['close_time'],
            "city": row['city']
        }
        data['restaurants'].append(restaurant)
    # print('data================>\n',data.values())

    timesAttract_path= os.path.join(project_root, 'attractions_reccommendation','Attractions open hours.csv')
    timesAttract = pd.read_csv(timesAttract_path)

    # select = timesAttract.loc[:, ['attraction_id', 'open_time', 'close_time']]

    joinedTimes = attractions_df.merge(timesAttract[['attraction_id', 'attraction_name','open_time', 'close_time', 'Latitude', 'Longitude', 'city']], on='attraction_id', how='inner')
    #print(joinedTimes.columns)
    #print(joinedTimes)
    changeTimeFormat(joinedTimes)
    # Extract information from attractions dataframe and add to dictionary
    for _, row in joinedTimes.iterrows():
        attraction = {
            "attraction_name": row['attraction_name_x'],
            "location": (row['Latitude_x'], row['Longitude_x']),
            "open_time": row['open_time'],
            "close_time": row['close_time'],
            "city": row['city_x']
        }
        data['attractions'].append(attraction)
    print('data================>\n', data['attractions'])

    return data


d=formatRecommendations('Cairo', 1)

###########JUST #printING THE DICTIONARY ##################
#print("Restaurants:")
# for restaurant in d['restaurants']:
    #print("- Name: {}, Location: {}, Open Time: {}, Close Time: {}, City: {}".format(restaurant['name'], restaurant['location'], restaurant['open_time'], restaurant['close_time'], restaurant['city']))

# print the attractions
# #print("\nAttractions:")
# for attraction in d['attractions']:
#     #print("- Name: {}, Location: {}, Open Time: {}, Close Time: {}, City: {}".format(attraction['attraction_name'],
#                                                                                      attraction['location'], attraction['open_time'], attraction['close_time'], attraction['city']))