import requests
from datetime import datetime
import os

# Nutritionix API Credentials
API_ID = os.environ.get("API_ID")
API_KEY = os.environ.get("API_KEY")

# Sheety API
SHEETY_ENDPOINT = os.environ.get("SHEETY_ENDPOINT")
BEARER_TOKEN = os.environ.get("BEARER_TOKEN")

# User Data
GENDER = "male"
WEIGHT_KG = 60
HEIGHT_CM = 160
AGE = 17

# Get Exercise Input
QUERY = input("Tell me which exercises you did: ")

# Nutritionix API Headers
nutritionix_headers = {
    "x-app-id": API_ID,
    "x-app-key": API_KEY,
    "Content-Type": "application/json",
}

# Nutritionix API Payload
nutritionix_payload = {
    "query": QUERY,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE,
}

# Call Nutritionix API
response = requests.post(
    url="https://trackapi.nutritionix.com/v2/natural/exercise",
    headers=nutritionix_headers,
    json=nutritionix_payload)
if response.status_code != 200:
  print(
      f"Error fetching data from Nutritionix API: {response.status_code}, {response.text}"
  )
  exit()

data = response.json()

# Extract Data
if "exercises" in data and data["exercises"]:
  exercise = data["exercises"][0]["user_input"]
  duration = data["exercises"][0]["duration_min"]
  calories = data["exercises"][0]["nf_calories"]
else:
  print("No exercise data found.")
  exit()

# Current Date and Time
date = datetime.now()
current_date = date.strftime("%d/%m/%Y")
current_time = date.strftime("%H:%M:%S")

# Sheety API Payload
sheety_payload = {
    "sheet1": {
        "date": current_date,
        "time": current_time,
        "exercise": exercise.title(),
        "duration": duration,
        "calories": calories,
    }
}

# Sheety API Headers
sheety_headers = {
    "Authorization": BEARER_TOKEN,
}

# Call Sheety API
response2 = requests.post(url=SHEETY_ENDPOINT,
                          json=sheety_payload,
                          headers=sheety_headers)
if response2.status_code == 200:
  print("Data successfully added to Google Sheet!")
else:
  print(
      f"Error posting data to Sheety API: {response2.status_code}, {response2.text}"
  )

