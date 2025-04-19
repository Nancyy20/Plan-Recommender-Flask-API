import os
import logging

    # Set up logging
logging.basicConfig(level=logging.INFO)

    # Get JAVA_HOME environment variable
java_home = os.environ.get('JAVA_HOME')

    # Log the JAVA_HOME value
logging.info(f"JAVA_HOME is set to: {java_home}")
from Plan.planMultipleDays import plan_multiple_days
# from Restaurants.cosine_sim_restaurants import get_recommendations
# from Hotels.cosine_similiarity_hotels import get_recommendation
# from attractions_reccommendation.cosine_sim_attraction import get_recommendations
# from attractions_reccommendation.profiling_new_user import profiling_new_user
# from Restaurants.restaurants_user_profiling import user_profile_restaurant
# from Hotels.initial_user_profiling import user_profile
from flask import Flask, request, jsonify
# from Hotels import test_env
# from Hotels.test_env import *
import jsonpickle
app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to my Flask app!"

#
#
# @app.route("/hotel/user-profile/<userId>", methods=['POST'])
# def add_user_for_hotel(userId):
#     assert userId == request.view_args['userId']
#     data = request.get_json(force=True)
#     user_profile(data, userId)
#     return ("Done ")
#
#
# @app.route('/hotel/<userId>/<city>', methods=['GET'])
# def hotel_recommednation(userId, city):
#     assert userId == request.view_args['userId']
#     assert city == request.view_args['city']
#     df = recommend_hotel(userId, city)
#     return df
#
#
# @app.route('/attraction/<userId>/<city>', methods=['GET'])
# def attraction_recommednation(userId, city):
#     assert userId == request.view_args['userId']
#     assert city == request.view_args['city']
#     city = city.lower()
#     df = recommend_attraction_place(int(userId), city)
#     return df.tolist()
#
#
# @app.route("/attraction/user-profile/<userId>", methods=['POST'])
# def add_user_for_attraction(userId):
#     assert userId == request.view_args['userId']
#     data = request.json
#     profiling_new_user(userId, data)
#     return ("Done ")
#
#
# @app.route('/restaurant/<userId>/<city>', methods=['GET'])
# def restaurant_recommednation(userId, city):
#     assert userId == request.view_args['userId']
#     assert city == request.view_args['city']
#     df = recommend_restaraurnat(userId, city)
#     try:
#         return df.tolist()
#     except:
#         return df
#
#
# @app.route("/restaurant/user-profile/<userId>", methods=['POST'])
# def add_user_for_restaurant(userId):
#     assert userId == request.view_args['userId']
#     data = request.json
#     user_profile_restaurant(data, userId)
#     return ("Done ")
#
#
# @app.route('/attraction/cosine/<int:attraction_id>', methods=['GET'])
# def attraction_recommednation_cosine(attraction_id):
#     assert attraction_id == request.view_args['attraction_id']
#     df = get_recommendations(attraction_id)
#     return df
#
#
# @app.route('/hotel/cosine/<int:hotel_id>', methods=['GET'])
# def hotel_recommednation_cosine(hotel_id):
#     assert hotel_id == request.view_args['hotel_id']
#     df = get_recommendation(hotel_id)
#     return df
#
#
# @app.route('/restaurant/cosine/<int:restaurant_id>', methods=['GET'])
# def restaurant_recommednation_cosine(restaurant_id):
#     assert restaurant_id == request.view_args['restaurant_id']
#     df = get_recommendations(restaurant_id)
#     return df


@app.route('/recommend/plan/<userId>/<city>', methods=['POST'])
def plan_recommednation(userId, city):
    print('plan recommendation=======================================')
    assert userId == request.view_args['userId']
    assert city == request.view_args['city']
    data = request.get_json()
    start_time = data.get('startTime', str)
    end_time = data.get('endTime', str)
    long = data.get('longitude', float)
    lat = data.get('latitude', float)
    no_days = data.get('noOfDays', int)
    return jsonify(plan_multiple_days(no_days, city, (lat, long), userId, start_time, end_time))


@app.route('/recommend/plan/<userId>/<city>', methods=['GET'])
def plan_recommendation(userId, city):
    print('plan recommendation=======================================')
    assert userId == request.view_args['userId']
    assert city == request.view_args['city']

    # Get data from query parameters
    start_time = request.args.get('startTime')
    end_time = request.args.get('endTime')
    long = request.args.get('longitude')
    lat = request.args.get('latitude')
    no_days = request.args.get('noOfDays')

    # Validate data (important!)
    try:
        lat = float(lat)
        long = float(long)
        no_days = int(no_days)
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid input parameters"}), 400  # Bad Request

    # Call your plan_multiple_days function
    # result = plan_multiple_days(2,"cairo", (30.0444, 31.2357), 1, "8AM", "8PM")
    result = plan_multiple_days(no_days, city, (lat, long), userId, start_time, end_time)

    # Return the result as JSON
    return jsonify(result)


if __name__ == '__main__':


    app.run(debug=True,port=os.getenv("PORT", default=5000)) # in deployment removed debug=True --> it is only for development
