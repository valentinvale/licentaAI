import pandas as pd
from translate import Translator

translator = Translator(to_lang="ro")

breed_images_df = pd.read_csv('breed_images.csv')
breed_names = breed_images_df['breed_name'].unique()
bred_names = [breed_name.replace(' ', '_').title() for breed_name in breed_names]
print(breed_names)
breed_names_romanian = [translator.translate(breed_name.replace('_', ' ')).title() for breed_name in breed_names]

breed_ids = range(len(breed_names))

breed_df = pd.DataFrame({
    'breed_id': breed_ids,
    'breed_name': breed_names,
    'breed_name_ro': breed_names_romanian
})

breed_df.to_csv('breed.csv', index=False)
