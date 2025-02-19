from fields import select_field
import json
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.ndimage import gaussian_filter
from scipy.spatial import ConvexHull
import numpy as np
from matplotlib.colors import LogNorm

## This code will be reused for all the metrics
## Move it to a different place later
# Define your four corner points as (latitude, longitude)
field = {
    #"corner1": (-20.127965, -40.304853),
    #"corner2": (-20.128007, -40.303850),
    #"corner3": (-20.127326, -40.304825),
    #"corner4": (-20.127381, -40.303826),
    "corner1": (20.127965, 40.304853),
    "corner2": (20.128007, 40.303850),
    "corner3": (20.127326, 40.304825),
    "corner4": (20.127381, 40.303826),
}

# Calculate length and width using geodesic distances
field["length"] = geodesic(field["corner1"], field["corner2"]).meters
field["width"] = geodesic(field["corner1"], field["corner3"]).meters

latitudes = [field["corner1"][0], field["corner2"][0], field["corner3"][0], field["corner4"][0]]
field["max_lat"] = max(latitudes)
field["min_lat"] = min(latitudes)

longitudes = [field["corner1"][1], field["corner2"][1], field["corner3"][1], field["corner4"][1]]
field["max_lon"] = max(longitudes)
field["min_lon"] = min(longitudes)

# Load your JSON data
with open('../data/result.json') as f:
    data = json.load(f)

def convert_to_field_coordinates(lat, lon, field):
    print(lat, lon, field)
    x = (lon - field["min_lon"]) / (field["max_lon"] - field["min_lon"]) * field["width"]
    y = (lat - field["min_lat"]) / (field["max_lat"] - field["min_lat"]) * field["length"]
    return x, y

# Create a figure and axis
fig, ax = plt.subplots(figsize=(10, 7))

# Function to initialize the plot
def init():
    ax.set_xlim(0, field["length"])
    ax.set_ylim(0, field["width"])
    ax.set_xlabel('X Position (meters)')
    ax.set_ylabel('Y Position (meters)')
    ax.set_title('Football Field with Tracked Object Positions')

    return []

x_array = []
y_array = []

def getBiggestFrequency(xis, yos):
    npx = np.array(xis)
    npy = np.array(yos)
    npx_round = np.round(npx, 2)
    npy_round = np.round(npy, 2)

    valuesx, counts = np.unique(npx_round, return_counts=True)
    most_frequent_valuex = valuesx[np.argmax(counts)]
    valuesy, counts = np.unique(npy_round, return_counts=True)
    most_frequent_valuey = valuesy[np.argmax(counts)]

    return most_frequent_valuex, most_frequent_valuey

player_obj = "01"
escalação_barcelona = {
    '01': 'Koundé',
    '02': 'Araujo',
    '03': 'Iñigo',
    '04': 'Balde',
    '05': 'De Jong',
    '06': 'Gavi',
    '07': 'Yamal',
    '08': 'Pedri',
    '09': 'Lewandowski',
    '10': 'Raphinha'
}


# Function to update the plot for each frame
def update(frame_number):

    if frame_number == "18:00:00":
        heatmap, xedges, yedges = np.histogram2d(x_array, y_array, bins=[50, 50], range=[[0, 105], [0, 68]])
        heatmap = gaussian_filter(heatmap, sigma=0.8)  # Aplicar filtro gaussiano

        # Plotar o campo e o heatmap
        fig1, ax1 = plt.subplots(figsize=(10, 7))
        select_field(105, 71, ax1)

        extent = [0, 105, 0, 71]
        heatmap_img = ax1.imshow(heatmap.T, extent=extent, origin='lower', cmap='coolwarm',
                            norm=LogNorm(vmin=0.01, vmax=np.max(heatmap)), alpha=0.8)

        #get the biggest frequency value on heatmap
        x_max, y_max = getBiggestFrequency(x_array, y_array)
        ax1.text(2, field["width"] - 2, f'ponto mais frequente: {x_max}, {y_max}', fontsize=12, color='black',
                bbox=dict(facecolor='white', alpha=0.7))
        # save the image
        #plt.savefig("heatmap.png", dpi=300, bbox_inches='tight', facecolor='white')
        # Show the animation
        ax1.set_title(f"Mapa de calor do Player {escalação_barcelona.get(player_obj)}")
        plt.grid(True)
        plt.show()

        return [heatmap_img]

    ax.clear()
    select_field(105, 71, ax)
    init()

    objects = data[str(frame_number)]

    points = []

    for obj in objects:
        x, y = convert_to_field_coordinates(obj.get('lat'), obj.get('lon'), field)
        number_player = obj.get('player')
        if number_player == player_obj:
            x_array.append(x)
            y_array.append(y)

        ax.plot(x, y, 'o', color='red')
        ax.text(x, y, escalação_barcelona.get(number_player), fontsize=10, color='black', ha="left", va="bottom")

        if 0 <= x <= field["length"] and 0 <= y <= field["width"]:
            points.append([x, y])

    # Draw the polygon by connecting the dots inside the field using the Convex Hull
    if len(points) > 2:
        points = np.array(points)
        hull = ConvexHull(points)
        hull_points = points[hull.vertices]



    ax.set_title(f"Football Field with Tracked Object Positions - Frame {frame_number}")

    return []

# Create the animation
#ani = animation.FuncAnimation(fig, update, frames=len(data), init_func=init, blit=True, repeat=False, interval=1)
ani = animation.FuncAnimation(fig, update, data, init_func=init, blit=True, repeat=False, interval=100)

# Show the animation
plt.grid(True)
plt.show()
