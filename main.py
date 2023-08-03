import requests
from datetime import datetime
import os

GENDER = "male"
WEIGHT_KG = "80.73944"
HEIGHT_CM = "177.8"
AGE = 46

APP_ID = os.environ["APP_ID"]
API_KEY = os.environ["API_KEY"]
YOUR_TOKEN = os.environ["YOUR_TOKEN"]
bearer_headers = {"Authorization": f"Bearer {YOUR_TOKEN}"}

nutritionix_exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheet_endpoint = os.environ["SHEET_ENDPOINT"]
# sheet_endpoint = "https://api.sheety.co/ad40ae24f3fa5f65a1263aef68f433bb/myWorkouts/workouts"
# this sheet no longer exists as I cancelled my subscriptiond

exercise_text = input("Tell me which exercises you did: ")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

exercise_post_config = {
 "query": exercise_text,
 "gender": GENDER,
 "weight_kg": WEIGHT_KG,
 "height_cm": HEIGHT_CM,
 "age": AGE
}

response = requests.post(url=nutritionix_exercise_endpoint, json=exercise_post_config, headers=headers)
result = response.json()
# print(response.text)
# print(result["exercises"][0]["name"].title())
# print(result["exercises"][0]["duration_min"])
# print(result["exercises"][0]["nf_calories"])




today = datetime.now()
today_date = today.strftime("%d/%m/%Y")
now_time = today.strftime("%X")

for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    sheet_response = requests.post(sheet_endpoint, json=sheet_inputs, headers=bearer_headers)
