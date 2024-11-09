# Travel Itinerary Assistant

This project is a conversational travel itinerary assistant powered by OpenAI, FastAPI, and Streamlit. It helps users plan a one-day itinerary by gathering information iteratively, providing weather-informed recommendations, and dynamically adjusting based on user inputs.

## Features

- **Iterative Interaction**: Gathers necessary details one at a time (e.g., travel date, start time, interests).
- **Weather-Based Suggestions**: Fetches weather data based on the travel date to provide personalized activity recommendations.
- **Dynamic Updates**: Updates the itinerary when the user changes preferences, such as travel date or budget.
- **Secure API Key Management**: Uses a `.env` file for securely storing API keys.

## Tech Stack

- **FastAPI** - For the backend API
- **OpenAI API** - For generating conversational responses and itinerary planning
- **Streamlit** - For a user-friendly front-end interface
- **Python-dotenv** - For environment variable management
- **OpenWeather API** - For weather forecasts based on travel date

## Prerequisites

- Python 3.7 or higher
- OpenAI API Key
- OpenWeather API Key

## Installation and Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-username/travel-itinerary-assistant.git
   cd travel-itinerary-assistant
