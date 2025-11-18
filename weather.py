import google.generativeai as genai
import requests
import streamlit as st

# Your API keys
GENAI_API_KEY = "AIzaSyAF8KqyLPT2wvgalZnLoEDYqNK8ehS15Ko"
WEATHER_API_KEY = "9d112b3aae1f0894636055a17f769607"

# Configure Gemini
genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

def get_weather(city):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {'q': city, 'appid': WEATHER_API_KEY, 'units': 'metric'}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        # Extract details
        temp = data['main']['temp']
        desc = data['weather'][0]['description']
        humidity = data['main']['humidity']
        wind = data['wind']['speed']
        icon = data['weather'][0]['icon']
        # Return dictionary for easier usage
        return {
            'city': city,
            'temp': temp,
            'desc': desc,
            'humidity': humidity,
            'wind': wind,
            'icon': icon
        }
    else:
        return None

# Streamlit UI setup
st.set_page_config(page_title="Weather Chatbot", page_icon="☁")
st.title("🌤 Interactive Weather Chatbot")
st.write("🌎 Ask about the weather in any city around the world!")

user_input = st.text_input("You:", placeholder="What's the weather in Paris?")

if user_input:
    with st.spinner("🤖 Thinking..."):
        # Extract city with Gemini
        prompt = f"""Extract the city name from this input: "{user_input}". 
If there's no city, respond with 'no city' only."""
        city_response = model.generate_content(prompt).text.strip()

        if city_response.lower() == "no city":
            st.error("❗ Please specify a city in your question.")
        else:
            weather_data = get_weather(city_response)
            if weather_data:
                # Display weather info
                st.image(f"https://openweathermap.org/img/wn/{weather_data['icon']}@2x.png", width=100)
                st.success(f"🌡️ Weather in {weather_data['city'].title()}")
                st.write(f"Temperature: {weather_data['temp']}°C")
                st.write(f"Description: {weather_data['desc'].capitalize()}")
                st.write(f"Humidity: {weather_data['humidity']}%")
                st.write(f"Wind Speed: {weather_data['wind']} m/s")

                # Generate chatbot reply
                reply_prompt = f"""User asked: "{user_input}"
Weather info: Temperature: {weather_data['temp']}°C, Description: {weather_data['desc']}, Humidity: {weather_data['humidity']}%, Wind Speed: {weather_data['wind']} m/s
Reply like a friendly weather chatbot."""
                reply = model.generate_content(reply_prompt).text.strip()
                st.info(f"🤖 {reply}")
            else:
                st.error("❗ Couldn't fetch weather. Please check the city name.")

