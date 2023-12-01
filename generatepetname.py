import backgroundremoval
import getpetmaincolors
import getclosestcolor
import matplotlib.pyplot as plt
import json
import random

def sort_by_colors(json_object, color1, color2):
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
            

        print("both colors: ", both_colors)
        print("first color: ", first_color)
        print("second color: ", second_color)
        print("rest: ", rest)

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


def generatepetname(petimage):
    color_objects = json.load(open('colorobjects.json'))
    print("color objects: ", color_objects)
    # first_object_color = color_objects["Portocala"]["color1"]
    # print("first object color: ", first_object_color)

    petimage = backgroundremoval.remove_background(petimage)
    dominant_colors, proportions, palette = getpetmaincolors.getpetmaincolors(petimage)
    closest_colors = [getclosestcolor.rgb_to_color_name(rgb) for rgb in dominant_colors]
    sorted_objects, both_colors, first_color, second_color, rest = sort_by_colors(color_objects, closest_colors[0], closest_colors[1])
    petname = pick_random_name(both_colors, first_color, second_color, rest)
    return dominant_colors, proportions, palette, closest_colors, sorted_objects, petname

if __name__ == "__main__":
    petimage = "Resources/tuxedocat.jpg"
    dominant_clors, proportions, palette, closest_colors, sorted_objects, petname =  generatepetname(petimage)
    print(dominant_clors)
    print(proportions)
    print("closest colors: ", closest_colors)
    print("sorted objects: ", sorted_objects)
    print("petname: ", petname)
    plt.imshow(palette)
    plt.show()