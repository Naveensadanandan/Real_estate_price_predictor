import streamlit as st

if not hasattr(st, 'already_started_server'):
    # Hack the fact that Python modules (like st) only load once to
    # keep track of whether this file already ran.
    st.already_started_server = True

    st.write('''
        The first time this script executes it will run forever because it's
        running a Flask server.

        Just close this browser tab and open a new one to see your Streamlit
        app.
    ''')
    from flask import Flask, request, jsonify
    from flask_cors import CORS
    import util

    app = Flask(__name__)
    CORS(app)  # This will enable CORS for all routes

    @app.route('/bhp')
    def hello():
        return "Hi"

    @app.route('/get_location_names')
    def get_location_names():
        response = jsonify(util.get_location_names())
        return response

    @app.route('/predict_home_price', methods=['POST'])
    def predict_home_price():
        total_sqft = float(request.form['total_sqft'])
        location = request.form['location']
        bhk = int(request.form['bhk'])
        bath = int(request.form['bath'])

        response = jsonify({
            "estimated_price": util.estimated_price(location, total_sqft, bath, bhk)
        })
        return response

    if __name__ == "__main__":
        print("starting python flask server for home price prediction")
        app.run()


    app.run(port=8888)



# We'll never reach this part of the code the first time this file executes!

# Your normal Streamlit app goes here:
import streamlit as st
import requests

# CSS for background image and general styling
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://cdn.pixabay.com/photo/2021/10/07/15/23/real-estate-6688945_1280.jpg");
        background-size: cover;
        width: 100%;
        height: 100vh;
        animation: fadeIn 1s ease-in-out;
        background-color: gray;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title of the Streamlit app
st.title("🏠 Bangalore Real Estate Price Predictor")

# CSS to style the markdown text inside a box
st.markdown(
    """
    <style>
    .info-box {
        background-color: #f0f8ff;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #d6e9f9;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
        margin-bottom: 20px;
    }
    .info-box h2 {
        color: #0066cc;
    }
    .info-box p {
        color: #333333;
        line-height: 1.6;
    }
    .price-box {
        background-color: #fff3cd;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #ffeeba;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
        margin-top: 20px;
        text-align: center;
    }
    .price-box h3 {
        color: #856404;
        margin: 0;
    }
    .price-box p {
        font-size: 24px;
        color: #856404;
        margin: 0;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Introduction inside a styled box
st.markdown(
    """
    <div class="info-box">
        <h2>Welcome to the Bangalore Real Estate Price Predictor! 🏡</h2>
        <p>
            Are you looking to buy or sell a property in Bangalore and wondering about the current market prices? Our app uses a Machine Learning model to predict the prices of real estate based on various factors like location, size, number of bedrooms, bathrooms, and more.
        </p>
        <p>
            Simply enter the property details, and we'll provide you with an estimated market price. Let's help you make informed decisions in the dynamic Bangalore real estate market!
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# API URL to fetch location names and predict price
locations_url = 'http://127.0.0.1:5000/get_location_names'
predict_url = 'http://127.0.0.1:5000/predict_home_price'

# Fetch data for the dropdown from the API
try:
    response = requests.get(locations_url)
    if response.status_code == 200:
        options = response.json()
    else:
        st.error('Failed to retrieve data from API.')
        options = []
except Exception as e:
    st.error(f'Error: {e}')
    options = []

# Add some spacing before the dropdown
st.markdown("<br><br>", unsafe_allow_html=True)

# Create a dropdown list in Streamlit for location selection
selected_location = st.selectbox('Choose a Location:', options)

# Input field for entering the area of the real estate in square feet
area = st.number_input("Enter the area of the real estate in square feet:", min_value=500, step=100)

# Selection box for number of bedrooms (BHK)
bhk = st.selectbox('Select number of BHK:', [1, 2, 3, 4, 5])

# Selection box for number of bathrooms (Bath)
bath = st.selectbox('Select number of Bathrooms:', [1, 2, 3, 4, 5])

# Predict price button
if st.button('Predict Price'):
    # Prepare the data to be sent to the API
    data = {
        'total_sqft': area,
        'location': selected_location,
        'bhk': bhk,
        'bath': bath
    }

    # Make a POST request to the Flask API endpoint
    try:
        response = requests.post(predict_url, data=data)
        if response.status_code == 200:
            estimated_price = response.json().get('estimated_price', 'N/A')

            # Display the estimated price in a styled box
            st.markdown(
                f"""
                <div class="price-box">
                    <h3>Estimated Price</h3>
                    <p>₹{estimated_price} Lakhs</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.error('Failed to get a response from the prediction API.')
    except Exception as e:
        st.error(f'Error: {e}')
