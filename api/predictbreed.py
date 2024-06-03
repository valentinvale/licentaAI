import requests
from PIL import Image
from io import BytesIO
import numpy as np
import pandas as pd
from keras.models import load_model
from get_pet_features_from_breed import get_pet_features


def format_breed_name(breed_name):
    return breed_name.replace('_', ' ').title()


def process_image(image_url):
    image_height = 64
    image_width = 64

    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content)).convert('RGB')
    image = image.resize((image_height, image_width))
    image = np.array(image)

    return image


def predict_breed(image_url, pet_type):
    breed_df = pd.read_csv('../breed.csv')
    model = load_model('../best_model_augumented.keras')

    cat_breed_indices = [index for index in range(len(breed_df)) if breed_df['pet_type'][index] == 0]
    dog_breed_indices = [index for index in range(len(breed_df)) if breed_df['pet_type'][index] == 1]

    breed_names = breed_df['breed_name'].values
    breed_names_ro = breed_df['breed_name_ro'].values

    image = process_image(image_url)

    predictions = model.predict(np.expand_dims(image, axis=0))[0]

    if pet_type == 0:
        filtered_predictions = [predictions[i] for i in cat_breed_indices]
        filtered_classes = [breed_names[i] for i in cat_breed_indices]
        filtered_classes_ro = [breed_names_ro[i] for i in cat_breed_indices]
    else:
        filtered_predictions = [predictions[i] for i in dog_breed_indices]
        filtered_classes = [breed_names[i] for i in dog_breed_indices]
        filtered_classes_ro = [breed_names_ro[i] for i in dog_breed_indices]
    
    predicted_index = np.argmax(filtered_predictions)
    
    predicted_class = filtered_classes[predicted_index]
    predicted_class_ro = filtered_classes_ro[predicted_index]

    pet_features = get_pet_features(predicted_class)
    
    return pet_features, format_breed_name(predicted_class), format_breed_name(predicted_class_ro)

    
if __name__ == '__main__':
    image_url = 'https://fureverhomeucv.s3.eu-central-1.amazonaws.com/load4_10c0b9e1-3e3e-4b3a-9475-a9268f645414/f78b3958-d7cd-4423-baa0-0c430d9578a4_cattest2.jpeg'
    pet_type = 0
    features, breed, breed_ro = predict_breed(image_url, pet_type)
    print(features, breed, breed_ro)

    



    