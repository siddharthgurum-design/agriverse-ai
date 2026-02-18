from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI()

# Enable CORS (VERY IMPORTANT for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gemini Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Request model
class CropRequest(BaseModel):
    crop: str
    location: str

# API Endpoint
@app.post("/get-price")
def get_price(data: CropRequest):

    prompt = f"""
    You are an agricultural market expert.

    Crop: {data.crop}
    Location: {data.location}, India

    Respond strictly in JSON format:

    {{
        "crop": "{data.crop}",
        "location": "{data.location}",
        "estimated_price": "",
        "trend": "Increasing/Decreasing/Stable",
        "advice": ""
    }}
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    try:
        return json.loads(response.text)
    except:
        return {"raw_response": response.text}