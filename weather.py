import google.generativeai as genai
import requests

# Your API keys
GENAI_API_KEY = "AIzaSyD5EUl6qZ5b9s2XnLbPeVuqLfPTavMDDHw"
WEATHER_API_KEY = "9d112b3aae1f0894636055a17f769607"

import streamlit as st


# Configure Gemini
genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

# Function to get weather data
def get_weather(city):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {'q': city, 'appid': WEATHER_API_KEY, 'units': 'metric'}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        desc = data['weather'][0]['description']
        humidity = data['main']['humidity']
        wind = data['wind']['speed']
        return f"Weather in {city}:\n- Temperature: {temp}°C\n- Description: {desc}\n- Humidity: {humidity}%\n- Wind Speed: {wind} m/s"
    else:
        return None

# Streamlit UI
st.set_page_config(page_title="Weather Chatbot", page_icon="☁")
st.title("🌤 Weather Chatbot")
st.write("Ask about the weather in any city!")

user_input = st.text_input("You:", "")

if user_input:
    with st.spinner("Thinking..."):
        # Step 1: Ask Gemini to extract city name
        prompt = f"""Extract the city name from this input: "{user_input}". 
If there's no city, respond with 'no city' only."""
        city_response = model.generate_content(prompt).text.strip()

        if city_response.lower() == "no city":
            st.error("🤖 Please specify a city in your question.")
        else:
            weather_info = get_weather(city_response)
            if weather_info:
                reply_prompt = f"""User asked: "{user_input}"
Weather info: {weather_info}
Reply like a smart chatbot in one paragraph."""
                reply = model.generate_content(reply_prompt).text
                st.success(f"🤖 {reply}")
            else:
                st.error("🤖 Couldn't fetch weather. Please check the city name.")