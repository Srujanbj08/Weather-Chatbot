# 🌤 Interactive Weather Chatbot

A friendly AI-powered weather chatbot built with Streamlit that provides real-time weather information for any city worldwide. The chatbot uses Google's Gemini AI to understand natural language queries and OpenWeatherMap API to fetch accurate weather data.

## ✨ Features

- 🌍 **Global Weather Data**: Get weather information for any city worldwide
- 🤖 **AI-Powered**: Uses Google Gemini AI to understand natural language queries
- 🎨 **Interactive UI**: Clean and user-friendly Streamlit interface
- 🌡️ **Comprehensive Info**: Temperature, description, humidity, wind speed, and weather icons
- 💬 **Conversational**: Friendly chatbot responses powered by Gemini AI

## 🚀 Demo

Simply ask questions like:
- "What's the weather in Paris?"
- "How's it looking in Tokyo today?"
- "Tell me about the weather in New York"
- "Is it raining in London?"

## 📋 Prerequisites

- Python 3.7 or higher
- Google Gemini API key
- OpenWeatherMap API key

## 🛠 Installation

1. **Clone or download** the project files

2. **Install required packages**:
   ```bash
   pip install streamlit requests google-generativeai
   ```

3. **Get API Keys**:
   
   **Google Gemini API Key:**
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Copy the API key
   
   **OpenWeatherMap API Key:**
   - Sign up at [OpenWeatherMap](https://openweathermap.org/api)
   - Go to API keys section
   - Copy your API key

4. **Update API Keys** in the code:
   ```python
   GENAI_API_KEY = "your_gemini_api_key_here"
   WEATHER_API_KEY = "your_openweathermap_api_key_here"
   ```

## 🎯 Usage

1. **Run the application**:
   ```bash
   streamlit run app.py
   ```

2. **Open your browser** and navigate to the provided URL (usually `http://localhost:8501`)

3. **Ask about weather** in any city using natural language

## 📁 Project Structure

```
weather-chatbot/
│
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
└── README.md          # Project documentation
```

## 📦 Dependencies

```txt
streamlit
requests
google-generativeai
```

## 🔧 Configuration

### API Keys Setup
Make sure to replace the placeholder API keys in the code:

```python
# Your API keys
GENAI_API_KEY = "your_actual_gemini_api_key"
WEATHER_API_KEY = "your_actual_openweathermap_api_key"
```

### Environment Variables (Optional)
For better security, you can use environment variables:

```python
import os
GENAI_API_KEY = os.getenv("GEMINI_API_KEY")
WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
```

## 🌟 How It Works

1. **User Input**: User types a weather query in natural language
2. **City Extraction**: Gemini AI extracts the city name from the user's query
3. **Weather Fetch**: App calls OpenWeatherMap API to get current weather data
4. **Display**: Weather information is displayed with icons and details
5. **AI Response**: Gemini generates a friendly, conversational response

## 🎨 Features Breakdown

- **Smart City Detection**: AI automatically identifies city names from natural language
- **Real-time Data**: Current weather conditions from OpenWeatherMap
- **Visual Elements**: Weather icons and clean layout
- **Error Handling**: Graceful handling of invalid cities or API errors
- **Responsive Design**: Works on desktop and mobile devices

## 🔒 Security Notes

- **API Key Security**: Never commit API keys to version control
- **Rate Limits**: Be aware of API rate limits for both services
- **Error Handling**: The app handles API failures gracefully

## 🚨 Troubleshooting

**Common Issues:**

1. **"Please specify a city"**: Make sure your query mentions a city name
2. **"Couldn't fetch weather"**: Check if the city name is spelled correctly
3. **API Errors**: Verify your API keys are valid and have sufficient quota

**API Rate Limits:**
- OpenWeatherMap: 1000 calls/day (free tier)
- Google Gemini: Check your quota in Google AI Studio

## 🛡️ Privacy & Security

- API keys should be kept secure and not shared publicly
- Consider using environment variables for production deployment
- No user data is stored by this application

## 📈 Future Enhancements

- 📅 5-day weather forecast
- 📊 Weather charts and graphs
- 🔔 Weather alerts and notifications
- 🗺️ Interactive weather maps
- 💾 Favorite cities feature
- 🌐 Multi-language support

## 🤝 Contributing

Feel free to fork this project and submit pull requests for any improvements!

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- [Google Gemini AI](https://ai.google.dev/) for natural language processing
- [OpenWeatherMap](https://openweathermap.org/) for weather data
- [Streamlit](https://streamlit.io/) for the web framework

---

**Made with ❤️ using Python, Streamlit, and AI**
