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

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

st.set_page_config(page_title="Weather Chatbot", page_icon="☁")
st.title("🌤 Interactive Weather Chatbot")
st.markdown("Ask about the weather in any city and I'll respond like a smart assistant.")

# Clear chat history button
if st.button("🧹 Clear chat history"):
    st.session_state.messages = []

# Display chat messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"🧑‍💬 **You:** {msg['content']}")
    else:
        content = msg['content']
        # If weather info is included with icon URL, show icon
        if "icon_url" in msg:
            st.image(msg["icon_url"], width=80)
        st.markdown(f"🤖 **Gemini:** {content}")

# User input form for smoother UX
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message here", placeholder="E.g. What's the weather in London?")
    submit = st.form_submit_button("Send")

if submit and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("Gemini is thinking..."):
        # Extract city name using Gemini
        city_prompt = f"""Extract the city name from this input: "{user_input}". 
If there's no city, respond with 'no city' only."""
        city_response = model.generate_content(city_prompt).text.strip()

        if city_response.lower() == "no city":
            bot_reply = "❗ Please specify a city name so I can provide the weather."
            st.session_state.messages.append({"role": "bot", "content": bot_reply})
        else:
            weather = get_weather(city_response)
            if weather:
                weather_text = (
                    f"Temperature: {weather['temp']}°C\n"
                    f"Description: {weather['desc'].capitalize()}\n"
                    f"Humidity: {weather['humidity']}%\n"
                    f"Wind Speed: {weather['wind']} m/s"
                )
                reply_prompt = f"""User asked: "{user_input}"
Weather info: {weather_text}
Reply like a helpful chatbot in one paragraph."""
                bot_reply = model.generate_content(reply_prompt).text.strip()
                # Add weather icon URL for display
                icon_url = f"https://openweathermap.org/img/wn/{weather['icon']}@2x.png"
                st.session_state.messages.append({"role": "bot", "content": bot_reply, "icon_url": icon_url})
            else:
                bot_reply = "Sorry, I couldn't fetch the weather. Please check the city name."
                st.session_state.messages.append({"role": "bot", "content": bot_reply})

    st.experimental_rerun()
