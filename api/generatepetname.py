import backgroundremoval
import getpetmaincolors
import getclosestcolor
import generatepetnamereddit
import matplotlib.pyplot as plt
import json
import random

def sort_by_colors(json_object, color1, color2):
        print(color1, color2)
        both_colors = []
        first_color = []
        second_color = []
        rest = []

        for object in json_object:
            colors = [object["color1"], object["color2"]]
            if color1 in colors and color2 in colors:
                both_colors.append(object["name"])
            elif color1 in colors:
                first_color.append(object["name"])
            elif color2 in colors:
                second_color.append(object["name"])
            else:
                rest.append(object["name"])
            

        # decomentez pentru reglare
        # print("both colors: ", both_colors)
        # print("first color: ", first_color)
        # print("second color: ", second_color)
        # print("rest: ", rest)

        sorted_objects = both_colors + first_color + second_color + rest

        return sorted_objects, both_colors, first_color, second_color, rest


def pick_random_name(both_colors, first_color, second_color, rest):
    if len(both_colors) > 0:
        return random.choice(both_colors)
    elif len(first_color) > 0:
        return random.choice(first_color)
    elif len(second_color) > 0:
        return random.choice(second_color)
    else:
        return random.choice(rest)

def create_random_name_pool(both_colors, first_color, second_color, rest):
    name_pool = []
    if len(both_colors) > 0:
        name_pool += both_colors
    if len(first_color) > 0:
        name_pool += first_color
    if len(second_color) > 0:
        name_pool += second_color
    if len(rest) > 0:
        name_pool += rest
    return name_pool

def generatepetname(petimage, pet_type="pet"):
    color_objects = json.load(open('colorobjects.json'))
    # decomentez pentru reglare
    # print("color objects: ", color_objects)
    # first_object_color = color_objects["Portocala"]["color1"]
    # print("first object color: ", first_object_color)

    petimage = backgroundremoval.remove_background(petimage)
    dominant_colors, proportions, palette = getpetmaincolors.getpetmaincolors(petimage, num_clusters=2)
    closest_colors = [getclosestcolor.rgb_to_color_name(rgb) for rgb in dominant_colors]
    sorted_objects, both_colors, first_color, second_color, rest = sort_by_colors(color_objects, closest_colors[0], closest_colors[1])
    # petname = pick_random_name(both_colors, first_color, second_color, rest)
    pregenerated_name_pool = create_random_name_pool(both_colors, first_color, second_color, rest)
    use_both_colors = False
    if dominant_colors[len(dominant_colors)-1][1] > 0.20:
        use_both_colors = True
    reddit_names = generatepetnamereddit.get_pet_names(closest_colors[0], closest_colors[1], pet_type=pet_type, two_colors=use_both_colors, limit=500, pos=False)
    if reddit_names == []:
        full_name_pool = pregenerated_name_pool
    else:
        full_name_pool = reddit_names
    petname = random.choice(full_name_pool)
    return dominant_colors, proportions, palette, closest_colors, sorted_objects, petname

def returnpetname(petimage, pet_type="pet"):
    dominant_colors, proportions, palette, closest_colors, sorted_objects, petname =  generatepetname(petimage, pet_type=pet_type)
    return petname

if __name__ == "__main__":
    petimage = "simba2.jpg"
    dominant_colors, proportions, palette, closest_colors, sorted_objects, petname =  generatepetname(petimage)
    # print(dominant_colors)
    # print(proportions)
    # print("closest colors: ", closest_colors)
    # print("sorted objects: ", sorted_objects)
    # print("petname: ", petname)
    # plt.imshow(palette)
    # plt.show()