from flask import Flask, request, jsonify
from flask_cors import CORS
from generatepetname import returnpetname
from predictbreed import predict_breed

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

    breed, breed_ro = predict_breed(image_url, pet_type)

    return jsonify({'breed': breed, 'breedRo': breed_ro})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
