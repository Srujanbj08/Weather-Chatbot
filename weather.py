import google.generativeai as genai
import requests
import streamlit as st

# Your API keys
GENAI_API_KEY = "AIzaSyD5EUl6qZ5b9s2XnLbPeVuqLfPTavMDDHw"
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
        temp = data['main']['temp']
        desc = data['weather'][0]['description']
        humidity = data['main']['humidity']
        wind = data['wind']['speed']
        icon = data['weather'][0]['icon']
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

st.set_page_config(page_title="Weather Chatbot", page_icon="☁")
st.title("🌤 Interactive Weather Chatbot")
st.write("🌎 Ask about the weather in any city around the world!")

# Initialize chat history if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Input box
user_input = st.text_input("You:", key="user_input", placeholder="What's the weather in Paris?")

if user_input:
    with st.spinner("🤖 Thinking..."):
        # Extract city name using Gemini
        prompt = f"""Extract the city name from this input: "{user_input}". 
If there's no city, respond with 'no city' only."""
        city_response = model.generate_content(prompt).text.strip()

        if city_response.lower() == "no city":
            bot_reply = "❗ Please specify a city in your question."
        else:
            weather_data = get_weather(city_response)
            if weather_data:
                # Format weather info string for chatbot prompt
                weather_info_str = (
                    f"Temperature: {weather_data['temp']}°C, "
                    f"Description: {weather_data['desc']}, "
                    f"Humidity: {weather_data['humidity']}%, "
                    f"Wind Speed: {weather_data['wind']} m/s"
                )

                # Generate bot reply
                reply_prompt = f"""User asked: "{user_input}"
Weather info: {weather_info_str}
Reply like a friendly weather chatbot."""
                bot_reply = model.generate_content(reply_prompt).text.strip()

                # Append user and bot messages to chat history
                st.session_state.messages.append({"role": "user", "content": user_input})
                st.session_state.messages.append({"role": "bot", "content": bot_reply})
            else:
                bot_reply = "❗ Couldn't fetch weather. Please check the city name."
                st.session_state.messages.append({"role": "user", "content": user_input})
                st.session_state.messages.append({"role": "bot", "content": bot_reply})

        # Clear input box after sending
        st.session_state.user_input = ""

# Display full chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"🧑‍💬 *You:* {msg['content']}")
    else:
        st.markdown(f"🤖 *Gemini:* {msg['content']}")
