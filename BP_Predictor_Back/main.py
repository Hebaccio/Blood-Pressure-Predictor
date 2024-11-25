import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from joblib import dump, load
from flask import Flask, request, jsonify
from flask_cors import CORS

# --- Step 1: Load and preprocess data ---
def load_data(file_path="BP_Info2.xlsx"):
    data = pd.read_excel(file_path)
    # Debugging step: print column types
    print("Column types:\n", data.dtypes)
    return data

def preprocess_and_split(data):
    # Define features and targets
    X = data[['Workday', 'Stress_Levels', 'Sleep_Quality', 'Tiredness']]
    y_upper = data['Upper_BP']
    y_lower = data['Lower_BP']

    return train_test_split(X, y_upper, y_lower, test_size=0.2, random_state=42)

# --- Step 2: Train models ---
def train_models(X_train, y_upper_train, y_lower_train):
    upper_model = RandomForestRegressor(n_estimators=100, random_state=42)
    lower_model = RandomForestRegressor(n_estimators=100, random_state=42)
    
    upper_model.fit(X_train, y_upper_train)
    lower_model.fit(X_train, y_lower_train)
    
    dump(upper_model, 'upper_model.joblib')
    dump(lower_model, 'lower_model.joblib')

# --- Step 3: Predict BP ---
def predict_bp(workday, stress_levels, sleep_quality, tiredness):
    # Create input features DataFrame
    input_features = pd.DataFrame([{
        'Workday': workday,
        'Stress_Levels': stress_levels,
        'Sleep_Quality' : sleep_quality,
        'Tiredness' : tiredness
    }])

    # Debugging: Print input features
    print("Input features for prediction:")
    print(input_features)

    # Load trained models and predict
    upper_model = load('upper_model.joblib')
    lower_model = load('lower_model.joblib')
    upper_bp = upper_model.predict(input_features)[0]
    lower_bp = lower_model.predict(input_features)[0]

    return upper_bp, lower_bp

# --- Step 4a: Add data ---
def add_data(new_data, file_path="BP_Info2.xlsx"):
    # Debugging: Print the incoming data
    print("New data received:")
    print(new_data)

    # Check for missing required columns
    required_columns = {'Workday', 'Stress_Levels', 'Sleep_Quality', 'Tiredness', 'Upper_BP', 'Lower_BP'}
    if not required_columns.issubset(new_data.columns):
        raise ValueError(f"New data must contain columns: {required_columns}")

    # Debugging: Print transformed new data
    print("Transformed new data:")
    print(new_data)

    # Load existing data
    print("Loading existing data...")
    data = load_data(file_path)

    # Append new data to existing data
    print("Appending new data to existing data...")
    data = pd.concat([data, new_data], ignore_index=True)

    # Save the updated data
    print("Saving updated data to file...")
    data.to_excel(file_path, index=False)

    print("Data added successfully.")

# --- Step 4b: Retrain model ---
def retrain_model(file_path="BP_Info2.xlsx"):
    print("Loading data for retraining...")
    data = load_data(file_path)

    # Preprocess and split the data
    print("Preprocessing and splitting data...")
    X_train, X_test, y_upper_train, y_upper_test, y_lower_train, y_lower_test = preprocess_and_split(data)

    # Train models
    print("Retraining models...")
    train_models(X_train, y_upper_train, y_lower_train)
    print("Models retrained successfully.")

# --- Step 5: Flask API ---
app = Flask(__name__)
CORS(app)

@app.route('/predict', methods=['POST'])
def predict():
    content = request.json
    workday = content['workday']
    stress_levels = content['stress_levels']
    sleep_quality = content['sleep_quality']
    tiredness = content['tiredness']
    upper_bp, lower_bp = predict_bp(workday, stress_levels, sleep_quality, tiredness)
    return jsonify({'Upper_BP': upper_bp, 'Lower_BP': lower_bp})

@app.route('/add_data', methods=['POST'])
def add_data_endpoint():
    try:
        content = request.json  # Expect a list of dictionaries
        print("Raw JSON received:", content)

        if not isinstance(content, list):
            return jsonify({"error": "Input data must be a list of dictionaries."}), 400

        # Convert JSON to DataFrame
        new_data = pd.DataFrame(content)

        # Call add_data
        add_data(new_data)

        return jsonify({'message': 'Data added successfully.'})

    except ValueError as ve:
        print(f"Validation Error in /add_data: {ve}")
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        print(f"Error in /add_data: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/retrain', methods=['POST'])
def retrain_endpoint():
    try:
        retrain_model()
        return jsonify({'message': 'Model retrained successfully.'})
    except Exception as e:
        print(f"Error in /retrain: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
        app.run(debug=True)