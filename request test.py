import requests

url = "http://localhost:5000/recommend/plan/1/cairo"
params = {
    "startTime": "8AM",
    "endTime": "8PM",
    "longitude": 31.2357,
    "latitude": 30.0444,
    "noOfDays": 2,
}

response = requests.get(url, params=params)

print(response.json())  # Print the JSON response