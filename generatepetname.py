import backgroundremoval
import getpetmaincolors
import getclosestcolor
import matplotlib.pyplot as plt

def generatepetname(petimage):
    petimage = backgroundremoval.remove_background(petimage)
    dominant_colors, proportions, palette = getpetmaincolors.getpetmaincolors(petimage)
    closest_colors = [getclosestcolor.rgb_to_color_name(rgb) for rgb in dominant_colors]
    return dominant_colors, proportions, palette, closest_colors

if __name__ == "__main__":
    petimage = "Resources/tuxedocat.jpg"
    dominant_clors, proportions, palette, closest_colors =  generatepetname(petimage)
    print(dominant_clors)
    print(proportions)
    print("closest colors: ", closest_colors)
    plt.imshow(palette)
    plt.show()