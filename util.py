import json
import pickle
import numpy as np

__location = None
__data_columns = None
__model = None


def estimated_price(location, total_sqft, bath, bhk):
    load_artifacts()
    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1
    x = np.zeros(len(__data_columns))
    x[0] = bath
    x[1] = bhk
    x[2] = total_sqft
    if loc_index >= 0:
        x[loc_index] = 1

    return round(__model.predict([x])[0], 2)

def get_location_names():
    load_artifacts()
    return __location

def load_artifacts():
    print("loading required artifacts")
    global __location
    global __data_columns
    global __model

    with open(r"columns.json", 'r') as f:
        __data_columns = json.load(f)['data_columns']
        __location = __data_columns[3:]

    with open(r"banglore_home_prices_model.pickle", 'rb') as f:
        __model = pickle.load(f)
    print("loaded saved artifacts")





if __name__ == "__main__":
    load_artifacts()
    print(get_location_names())
    print(estimated_price('1st phase jp nagar', 1000, 2, 2))
