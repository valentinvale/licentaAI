from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
import cv2
import matplotlib.pyplot as plt

def palette(clusters):
    width = 300
    palette = np.zeros((50, width, 3), np.uint8)
    steps = width/clusters.cluster_centers_.shape[0]
    for idx, centers in enumerate(clusters.cluster_centers_): 
        palette[:, int(idx*steps):(int((idx+1)*steps)), :] = centers
    
    # decomentez pentru reglare
    # plt.imshow(palette)
    # plt.show()

    return palette

def getpetmaincolors(petimage, num_clusters=3, ignore_black=True):
    # Check if the image has an alpha channel (transparency)
    if petimage.shape[-1] == 4:
        # If alpha channel is present, remove it
        petimage = petimage[:, :, :3]

    # decomentez pentru reglare
    # plt.imshow(petimage)
    # plt.show()
    # print(petimage.shape)

    # Create a mask to identify non-black pixels
    if ignore_black:
        non_black_mask = np.all(petimage != [0, 0, 0], axis=-1)
        petimage = petimage[non_black_mask]

    # Print the shape after filtering black pixels
    # decomentez pentru reglare
    #print("Filtered image shape:", petimage.shape)

    clt = KMeans(num_clusters)
    clt.fit(petimage.reshape(-1, 3))

    dominant_colors = clt.cluster_centers_.astype(int)
    proportions = [(np.sum(clt.labels_ == i) / clt.labels_.shape[0]) for i in np.unique(clt.labels_)]

    # Sort dominant colors and proportions based on proportions (most dominant first)
    sorting_indices = np.argsort(proportions)[::-1]
    dominant_colors = dominant_colors[sorting_indices]
    proportions = np.array(proportions)[sorting_indices]

    palette_img = palette(clt)

    return dominant_colors, proportions, palette_img
