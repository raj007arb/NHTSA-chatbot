import io
from flask import Flask, render_template, request, send_file, jsonify
from flask_cors import CORS
from visualiztion import *
from fetch import fetch_recall_data
from query_brain import query_brain
import json
import threading
import os
import pandas as pd

app = Flask(__name__)
CORS(app)

DATA_FILE = r"vehicle_data.json"
file_lock = threading.Lock()

chart_functions = {
    "component": generate_component_chart,
    "manufacturer": generate_manufacturer_chart,
    "severity": generate_severity_chart,
    "recall_trend": generate_recall_trend_chart,
    "recall_forecast": generate_recall_forecast_chart,
    "impact_score": generate_impact_score_chart,
    "remedy_score": generate_remedy_score_chart,
    "recall_forecast_lr": generate_recall_forecast_lr
}
def get_dataframe():
    data = fetch_recall_data()
    df = pd.DataFrame(data["results"])
    return df

def save_data(data):
    """Save the received vehicle data into a JSON file safely."""
    try:
        DATA_FILE = os.path.join(os.path.dirname(__file__), "vehicle_data.json")  # Ensure directory exists

        with file_lock:  # Prevent multiple threads from writing at the same time
            with open(DATA_FILE, "w") as file:
                json.dump(data, file, indent=4)

        # Verify that data was actually written
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as file:
                saved_data = json.load(file)
                print("✅ Data saved successfully! Contents:", saved_data)  # Debugging output
        else:
            print("❌ File was NOT created!")

    except Exception as e:
        print(f"❌ Error saving data: {e}")

        
@app.route('/get_vehicle_data', methods=['POST'])
def get_vehicle_data():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON format"}), 400
        
        if not isinstance(data, dict):
            return jsonify({"error": "Expected a JSON object"}), 400

        print("📥 Received Data:", data)  # Debugging output

        # Save data safely
        save_data(data)

        # Check if data was actually written
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as file:
                saved_data = json.load(file)
                print("📁 Saved Data in File:", saved_data)  # Debugging output
        else:
            print("❌ File was NOT created!")

        return jsonify({"message": "Data saved successfully"}), 200

    except Exception as e:
        print(f"❌ Error in get_vehicle_data: {e}")  # Debugging output
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_chart', methods=['POST'])
def get_chart():
    data = request.json
    chart_type = data.get("chart_type")

    if chart_type in chart_functions:
        img_bytes = chart_functions[chart_type]()  # Generate the chart
        return send_file(img_bytes, mimetype='image/png')  # Send image response

    return {"error": "Invalid chart type"}, 400

@app.route('/chatbot', methods=['POST'])
def chatbot():
    try:
        print("🔹 Received a request at /chatbot")  # Log request arrival

        data = request.get_json()
        print("📥 Received JSON data:", data)  # Debugging log

        if not data or "message" not in data:
            print("❌ Error: Missing 'message' in request")  # Log error
            return jsonify({"error": "Missing 'message' in request"}), 400

        user_message = data["message"]
        print("💬 User Message:", user_message)  # Log user input

        response = query_brain(user_message)
        print("🤖 Chatbot Response:", response)  # Log AI response

        return jsonify({"response": response})
    except Exception as e:
        print("❌ Exception in /chatbot:", str(e))  # Log any unexpected error
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
