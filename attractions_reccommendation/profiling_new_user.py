import pandas as pd


def intersection(lst1, lst2):
    if lst1 in lst2:
        return True
    else:
        return False
    


def profiling_new_user(user_id, preferences):
    attractions = pd.read_csv(r'C:\Users\Salah Ashraf\PycharmProjects\TravelRecommeder_Flask\attractions_reccommendation\attractions.csv', encoding='latin-1')

    attraction_types = {1: 'Museum', 2: 'Park', 3: 'Historical landmark', 4: 'Beach', 5: 'Garden', 6: 'Art Gallery',
                        7: 'Palace', 8: 'Mosque', 9: 'Church', 10: 'Shopping mall', 11: 'Temple', 12: 'Bazar',
                        13: 'island', 14: 'Zoo', 15: 'Library'}

    preferred_types = []
    print("Preferences: ")
    print(preferences)
    for i in preferences:
        try:
            # print(i + " " + attraction_types[i])
            preferred_types.append(attraction_types[i])
            # print(attraction_types[i])
        except KeyError:
            print("Error")
            print(KeyError)

    user_rating_df = []
    print(preferred_types)

    for ind, col in attractions.iterrows():
        if pd.isna(col[4]):
            continue
        attraction_types = col[4]
        # row_attractions = attraction_types.split(",")
        # print(row_attractions)

        if intersection(attraction_types, preferred_types):
            rating = 5
        else:
            rating = int(1)
        if rating > 1:
            user_rating_df.append(
                {
                    'user_id': user_id,
                    'attraction_id': col[0],
                    'rating': rating,
                    'flag': 'F',
                    'city': col[8]

                }
            )

    pd.DataFrame(user_rating_df).to_csv('user_profiling3011.csv', index=False, mode='a', header=False)


# profiling_new_user(5555, [1,3])
