
from fastapi import FastAPI, Request
import os
import openai
import requests
import json
from weather_agent import fetch_weather
from memory_agent import MemoryAgent
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

session_history = []
memory_agent = MemoryAgent()

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message", "")
    
    session_history.append({"role": "user", "content": user_message})

    system_prompt = {
    "role": "system",
    "content": """
    You are a highly intelligent and friendly travel assistant. Your goal is to help the user create a one-day travel itinerary by gathering only the necessary details step-by-step. Here's how you should handle the interaction:

    1. **Identify Missing Information**: If any required detail is missing, ask for it one at a time. Do not ask for multiple pieces of information in a single response.

    2. **Travel Date Confirmation**: If the user provides a travel date, confirm it by outputting the date in JSON format, like this:  
       {"travel_date": "YYYY-MM-DD"}

       This will trigger a weather forecast retrieval for that date, which you can use to provide weather-based recommendations.

    3. **Gathering Details**: Collect the following details  step-by-step,
       - Start and end times
       - Interests (e.g., history, food)
       - Budget
       - Starting location

    4. **Generate Itinerary**: When all required details are available, create a detailed, weather-informed itinerary that includes:
       - A sequence of stops with timing, travel methods, and estimated costs and short description of place.
       - Recommendations based on the weather forecast (e.g., suggest indoor activities for rain or outdoor for sunny weather).

    5. **Iterative Updates**: If the user provides new or updated details (e.g., a new travel date or budget change), adjust the itinerary accordingly without re-requesting confirmed information.

    Keep responses concise, iterative, and user-friendly, focusing on gathering one piece of missing information at a time.
    """
}

    
    if len(session_history) == 1:
        session_history.insert(0, system_prompt)

    conversation = session_history.copy()
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )

    assistant_reply = response['choices'][0]['message']['content']
    session_history.append({"role": "assistant", "content": assistant_reply})

    try:
        reply_json = json.loads(assistant_reply)
        if "travel_date" in reply_json:
            travel_date = reply_json["travel_date"]
            current_stored_date = memory_agent.get_preference("travel_date")
            
            if travel_date != current_stored_date:
                memory_agent.store_preference("travel_date", travel_date)
            
                weather_data = fetch_weather("Mumbai", travel_date)  
                if weather_data:
                    weather_info = weather_data.get("forecast", "No forecast available")
                    memory_agent.store_preference("weather_info", weather_info)
                    session_history.append({"role": "assistant", "content": f"Weather forecast for {travel_date}: {weather_info}"})
                else:
                    session_history.append({"role": "assistant", "content": "Unable to retrieve the weather forecast. Please try again later."})
    except json.JSONDecodeError:
    
        pass

    travel_date = memory_agent.get_preference("travel_date")
    weather_info = memory_agent.get_preference("weather_info", "not yet available")
    preferences = {
        "start_time": memory_agent.get_preference("start_time"),
        "end_time": memory_agent.get_preference("end_time"),
        "interests": memory_agent.get_preference("interests"),
        "budget": memory_agent.get_preference("budget"),
        "start_location": memory_agent.get_preference("start_location")
    }

    if all(preferences.values()) and travel_date and weather_info:
        itinerary_prompt = f"Generate a full itinerary with weather-based recommendations based on these details: Date: {travel_date}, Weather: {weather_info}, Start: {preferences['start_time']}, End: {preferences['end_time']}, Interests: {preferences['interests']}, Budget: {preferences['budget']}, Start Location: {preferences['start_location']}."
        conversation.append({"role": "assistant", "content": itinerary_prompt})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation
        )

        final_reply = response['choices'][0]['message']['content']
        session_history.append({"role": "assistant", "content": final_reply})
        return {"reply": final_reply}

    return {"reply": assistant_reply}

@app.post("/start_session")
async def start_session():
    """Reset the session history for a new conversation."""
    global session_history
    session_history = []
    memory_agent.clear_memory()
    return {"message": "New session started"}



# 