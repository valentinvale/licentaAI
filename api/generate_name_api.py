from flask import Flask, request, jsonify
from flask_cors import CORS
from generatepetname import returnpetname

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

if __name__ == '__main__':
    app.run(debug=True, port=5000)
