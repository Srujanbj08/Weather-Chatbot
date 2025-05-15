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
        return f"Weather in {city}:\n- Temperature: {temp}°C\n- Description: {desc}\n- Humidity: {humidity}%\n- Wind Speed: {wind} m/s"
    else:
        return None

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Streamlit UI
st.set_page_config(page_title="Weather Chatbot", page_icon="☁")
st.title("🌤 Weather Chatbot")
st.markdown("Ask about the weather in any city and I'll respond like a smart assistant.")

# Display chat history
for msg in st.session_state.messages:
    role = msg["role"]
    content = msg["content"]
    if role == "user":
        st.markdown(f"🧑‍💬 **You:** {content}")
    else:
        st.markdown(f"🤖 **Gemini:** {content}")

# User input box
user_input = st.text_input("Type your message here", key="user_input")

if st.button("Send") and user_input.strip():
    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input.strip()})

    with st.spinner("Gemini is thinking..."):
        # Extract city using Gemini model
        city_prompt = f'Extract the city name from this input: "{user_input.strip()}". If no city, respond with "no city".'
        city_response = model.generate_content(city_prompt).text.strip()

        if city_response.lower() == "no city":
            bot_reply = "Please specify a city name so I can provide the weather."
        else:
            weather = get_weather(city_response)
            if weather:
                # Generate a friendly reply including weather info
                reply_prompt = f'User asked: "{user_input.strip()}"\nWeather info: {weather}\nReply like a helpful chatbot in one paragraph.'
                bot_reply = model.generate_content(reply_prompt).text.strip()
            else:
                bot_reply = "Sorry, I couldn't fetch the weather. Please check the city name."

        # Append bot reply
        st.session_state.messages.append({"role": "bot", "content": bot_reply})

    # Clear the input box by resetting the key in session_state
    st.session_state.user_input = ""

    # Rerun the app to update UI immediately with new messages and cleared input
    st.experimental_rerun()
