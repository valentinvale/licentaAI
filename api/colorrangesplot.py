import matplotlib.pyplot as plt
import numpy as np

def plot_color_ranges(color_ranges):
    # Convert color_ranges values to a NumPy array
    colors_array = np.array(list(color_ranges.values()), dtype=np.uint8)

    plt.figure(figsize=(10, 1))
    ax = plt.gca()
    
    # Iterate over each color range and create a colored bar
    for i, (lower, upper) in enumerate(colors_array):
        ax.fill_betweenx(y=[0, 1], x1=i, x2=i+1, color=[lower / 255.0], edgecolor='black')

    ax.set_yticks([])
    ax.set_xticks(np.arange(0.5, len(color_ranges) + 0.5, 1))
    ax.set_xticklabels(list(color_ranges.keys()), rotation=45, ha='right')

    plt.show()

# Define approximate RGB ranges for common color names
color_ranges = {
    'Red': ((200, 0, 0), (255, 50, 50)),
    'Green': ((0, 150, 0), (50, 255, 50)),
    'Blue': ((0, 0, 150), (50, 50, 255)),
    'Orange': ((255, 100, 0), (255, 200, 50)),
    'Purple': ((100, 0, 100), (200, 50, 200)),
    'Yellow': ((255, 255, 0), (255, 255, 50)),
    'Brown': ((139, 69, 19), (165, 42, 42)),
    'Pink': ((255, 182, 193), (255, 192, 203)),
    'Gray': ((128, 128, 128), (192, 192, 192)),
    'Black': ((0, 0, 0), (20, 20, 20)),
    'White': ((255, 255, 255), (255, 255, 255)),
}

# Plot the color ranges
plot_color_ranges(color_ranges)
