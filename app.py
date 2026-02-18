import os
import requests
from google import genai
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)


def get_weather_data(location):
    """Fetch 5-day weather forecast"""
    url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": f"{location},IN",
        "appid": WEATHER_API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        summary = []
        for item in data['list'][::8]:  # one reading per day
            date = item['dt_txt'].split(" ")[0]
            temp = item['main']['temp']
            desc = item['weather'][0]['description']
            summary.append(f"{date}: {temp}°C, {desc}")

        return "\n".join(summary)

    except Exception as e:
        return f"Weather data unavailable: {e}"


def generate_agri_report(crop, location):
    weather_summary = get_weather_data(location)

    prompt = f"""
    Role: Senior Agricultural Consultant

    Crop: {crop}
    Location: {location}, India

    5-Day Weather Forecast:
    {weather_summary}

    Provide output strictly in valid JSON format:

    {{
        "current_market_price": "",
        "harvest_advice": "",
        "risk_level": "Low/Medium/High",
        "7_day_price_trend": "",
        "confidence_score": "0-100%"
    }}
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-latest",
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"AI Error: {e}"


if __name__ == "__main__":
    print("\n🌾 AgriVerse AI – Weather & Market Intelligence\n")

    crop = input("Enter Crop: ")
    location = input("Enter City: ")

    print("\nAnalyzing...\n")

    result = generate_agri_report(crop, location)

    print("=" * 50)
    print(result)
    print("=" * 50)