import requests
import json
import pandas as pd
pd.set_option('display.max_columns', None)
from datetime import datetime
import streamlit as st


st.set_page_config(
    page_title="Weather Dashboard ",   
    page_icon="🌤️",                      
    layout="centered",                   
    initial_sidebar_state="expanded"    
)


st.title("Get The Current Weather in your City!")
country_code = st.text_input("Please Enter the Country Code: ")

city_name = st.text_input("Please Enter the City Name: ")

API_KEY = st.secrets["API_KEY"]

def get_weather():
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name},{country_code}&appid={API_KEY}"

    response = requests.get(url)

    if response.status_code == 200:

        json_response = response.json()

        if 'main' in json_response and 'sys' in json_response:

            description = json_response['weather'][0]['description']

            name = json_response['name']

            current_temp = int(json_response['main']['temp'])

            feels_like = int(json_response['main']['feels_like'])

            temp_min = int(json_response['main']['temp_min'])

            temp_max = int(json_response['main']['temp_max'])

            humidity = int(json_response['main']['humidity'])

            sunrise =  int(json_response['sys']['sunrise'])

            sunset =  int(json_response['sys']['sunset'])

            return description, current_temp, feels_like, temp_min, temp_max, humidity, name, sunrise, sunset
        
        else:
            st.warning("Failed to fetch data")
            return None

    else:
        st.warning("Failed to fetch data. Make sure you have entered the API key")
        return None
    

if st.button("Get Weather"): 
    if city_name and country_code:
        try: 
            description, current_temp, feels_like, temp_min, temp_max, humidity, name, sunrise, sunset = get_weather()

            sunrise_time = datetime.fromtimestamp(sunrise)
            sunset_time = datetime.fromtimestamp(sunset)

            df = pd.DataFrame({
                'Description': description.title(),
                'Current Temperature':  f"{current_temp - 273.15:.2f} C",
                'Feels Like': f"{feels_like - 273.15:.2f} C",
                'Minimum Temperature':  f"{(temp_min - 273.15):.2f} C",
                'Maximum Temperature':  f"{temp_max - 273.15:.2f} C",
                'Humidity': f"{humidity} %",
                'Sunrise Time': sunrise_time,
                'Sunset Time': sunset_time

            }, index = [name])


            # Beautifying
            df['Sunrise Time'] = df['Sunrise Time'].dt.strftime('%I:%M %p')
            df['Sunset Time'] = df['Sunset Time'].dt.strftime('%I:%M %p')


            df_transposed = df.T.reset_index()
            df_transposed.columns = ["Metric", city_name]
            st.table(df_transposed)

        except Exception as e:
            print(str(e))
