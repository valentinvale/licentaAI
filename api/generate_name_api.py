from flask import Flask, request, jsonify
from flask_cors import CORS
from generatepetname import returnpetname
from predictbreed import predict_breed
import pandas as pd
import joblib
import pickle
from get_pet_features_from_breed import get_unformated_breed_name

app = Flask(__name__)

CORS(app)

@app.route('/generate-pet-name', methods=['POST'])
def generate_pet_name():
    data = request.get_json()
    image_url = data['imageUrl']
    pet_type = data.get('petType', 'pet')
    if not image_url:
        return jsonify({'error': 'Image URL is required'}), 400
    
    if pet_type not in ['pet', 'cat', 'dog']:
        return jsonify({'error': 'Invalid pet type'}), 400

    pet_name = returnpetname(image_url, pet_type)
    return jsonify({'petName': pet_name})

@app.route('/predict-pet-breed', methods=['POST'])
def predict_pet_breed():
    data = request.get_json()
    image_url = data['imageUrl']
    pet_type = data.get('petType', 'pet')
    if not image_url:
        return jsonify({'error': 'Image URL is required'}), 400

    if pet_type not in ['cat', 'dog']:
        return jsonify({'error': 'Invalid pet type'}), 400
    
    if pet_type == 'cat':
        pet_type = 0
    else:
        pet_type = 1

    features, breed, breed_ro = predict_breed(image_url, pet_type)

    return jsonify({'breed': breed, 'breedRo': breed_ro, 'temperament': features['pet_temperament'], 'activityLevel': features['pet_activity_level'], 'careNeeds': features['pet_care_needs'], 'noiseLevel': features['pet_noise_level'], 'goodWithKids': features['pet_good_with_kids'], 'goodWithPets': features['pet_good_with_pets']})


model = joblib.load('../logistic_regression_model.pkl')

def preprocess_input(data, expected_columns):
    # Convert JSON to DataFrame
    df = pd.DataFrame([data])

    # Handle categorical variables using one-hot encoding
    df = pd.get_dummies(df)

    # Add missing columns from training data and set them to 0
    missing_cols = set(expected_columns) - set(df.columns)
    for col in missing_cols:
        df[col] = 0

    # Ensure the DataFrame has the columns in the same order as the training data
    df = df[expected_columns]

    return df


@app.route('/predict-compatibility', methods=['POST'])
def predict_compatibility():
    try:
        data = request.get_json(force=True)

        print(data)
        
        existing_breed = data['pet_breed']

        if get_unformated_breed_name(existing_breed) != None:
            existing_breed = get_unformated_breed_name(data['pet_breed']) 

        user_data = {
            'personality': data['personality'],
            'activity_level': data['activity_level'],
            'work_schedule': data['work_schedule'],
            'living_environment': data['living_environment'],
            'has_children': data['has_children'],
            'has_other_pets': data['has_other_pets'],
            'hypoallergenic': data['hypoallergenic'],
            'low_maintenance': data['low_maintenance']
        }

        pet_data = {
            'pet_species': data['pet_species'],
            'pet_breed': existing_breed,
            'pet_temperament': data['pet_temperament'],
            'pet_activity_level': data['pet_activity_level'],
            'pet_care_needs': data['pet_care_needs'],
            'pet_noise_level': data['pet_noise_level'],
            'pet_good_with_kids': data['pet_good_with_kids'],
            'pet_good_with_pets': data['pet_good_with_pets']
        }

        combined_data = {**user_data, **pet_data}

        # Load the expected columns used during training
        with open('../model_features.pkl', 'rb') as file:
            expected_columns = pickle.load(file)

        # Preprocess the input data to match the training data format
        user_df = preprocess_input(combined_data, expected_columns)

        # Make prediction
        prediction = model.predict(user_df)
        prediction_prob = model.predict_proba(user_df)[:, 1]

        print(prediction, prediction_prob)

        return jsonify({
            'prediction': int(prediction[0]),
            'compatibility_percentage': float(prediction_prob[0] * 100)
        })
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
