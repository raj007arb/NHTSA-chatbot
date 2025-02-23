import requests
import json
import os

def fetch_recall_data():
    file_path = r"vehicle_data.json"
    with open(file_path, 'r') as file:
        data = json.load(file) 

    make = data['make']
    model = data['model']
    model_year = data['model_year']

    # Construct the API URL with URL-encoded parameters
    url = f"https://api.nhtsa.gov/recalls/recallsByVehicle?make={requests.utils.quote(make)}&model={requests.utils.quote(model)}&modelYear={requests.utils.quote(model_year)}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

if __name__ == "__main__":
    data = fetch_recall_data()
    # print(type(data))
    print(data["results"])
    