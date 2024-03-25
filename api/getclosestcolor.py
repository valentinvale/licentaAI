from scipy.spatial import distance

def rgb_to_color_name(rgb):
    color_names = {
        'Red': (255, 0, 0),
        'Green': (0, 255, 0),
        'Blue': (0, 0, 255),
        'Orange': (255, 165, 0),
        'Purple': (128, 0, 128),
        'Yellow': (255, 255, 0),
        'Brown': (165, 42, 42),
        'Pink': (255, 192, 203),
        'Gray': (128, 128, 128),
        'Black': (0, 0, 0),
        'White': (255, 255, 255),
        # Add more color names and RGB values as needed
    }

    min_distance = float('inf')
    closest_color = 'Unknown'

    # calculam distanta euclidiana dintre rgb si fiecare culoare din color_names si returnam cea mai mica distanta

    for color, ref_rgb in color_names.items():
        d = distance.euclidean(rgb, ref_rgb)
        if d < min_distance:
            min_distance = d
            closest_color = color

    return closest_color

# rgb_value = (228, 231, 228)
# color_name = rgb_to_color_name(rgb_value)
# print(f"The closest color name is: {color_name}")
