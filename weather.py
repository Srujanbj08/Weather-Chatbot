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

# Streamlit UI
st.set_page_config(page_title="Weather Chatbot", page_icon="☁")
st.title("🌤 Interactive Weather Chatbot")
st.write("🌎 Ask about the weather in any city around the world!")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Use this key to control the input text value
user_input = st.text_input("You:", key="user_input", placeholder="What's the weather in Paris?")

if user_input:
    # Clear previous chat history on new input
    st.session_state.messages = []

    with st.spinner("🤖 Thinking..."):
        # Extract city name
        prompt = f"""Extract the city name from this input: "{user_input}". 
If there's no city, respond with 'no city' only."""
        city_response = model.generate_content(prompt).text.strip()

        if city_response.lower() == "no city":
            st.error("❗ Please specify a city in your question.")
        else:
            weather_data = get_weather(city_response)
            if weather_data:
                st.session_state.messages.append({"role": "user", "content": user_input})

                # Show weather info
                st.image(f"https://openweathermap.org/img/wn/{weather_data['icon']}@2x.png", width=100)
                st.success(f"🌡️ **Weather in {weather_data['city'].title()}**")
                st.write(f"Temperature: {weather_data['temp']}°C")
                st.write(f"Description: {weather_data['desc'].capitalize()}")
                st.write(f"Humidity: {weather_data['humidity']}%")
                st.write(f"Wind Speed: {weather_data['wind']} m/s")

                weather_info_str = (
                    f"Temperature: {weather_data['temp']}°C, "
                    f"Description: {weather_data['desc']}, "
                    f"Humidity: {weather_data['humidity']}%, "
                    f"Wind Speed: {weather_data['wind']} m/s"
                )

                reply_prompt = f"""User asked: "{user_input}"
Weather info: {weather_info_str}
Reply like a friendly weather chatbot."""
                reply = model.generate_content(reply_prompt).text.strip()

                st.session_state.messages.append({"role": "bot", "content": reply})

                # Display current chat only
                for msg in st.session_state.messages:
                    if msg["role"] == "user":
                        st.markdown(f"🧑‍💬 *You:* {msg['content']}")
                    else:
                        st.markdown(f"🤖 *Gemini:* {msg['content']}")

                # CLEAR the input box after processing
                st.session_state.user_input = ""
            else:
                st.error("❗ Couldn't fetch weather. Please check the city name.")
