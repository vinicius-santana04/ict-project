import json
from geopy.distance import geodesic
from scipy.spatial import ConvexHull
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

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


def update(frame_number):
    ax.clear()
    init()

    objects = data[str(frame_number)]

    points = []

    for obj in objects:
        x, y = convert_to_field_coordinates(obj.get('lat'), obj.get('lon'), field)

        ax.plot(x, y, 'o', color='red')

        if 0 <= x <= field["length"] and 0 <= y <= field["width"]:
            points.append([x, y])

    # Calcula o polígono usando o ConvexHull
    if len(points) > 2:
        points = np.array(points)
        hull = ConvexHull(points)
        hull_points = points[hull.vertices]

        # Área do polígono com ConvexHull
        polygon_area = hull.volume

        # Obtém o centróide do polígono
        centroid_x = np.mean(hull_points[:, 0])
        centroid_y = np.mean(hull_points[:, 1])

        # Preenche o polígono com uma cor transparente
        ax.fill(hull_points[:, 0], hull_points[:, 1], 'orange', alpha=0.2)

        # Marca o centróide no gráfico
        ax.plot(centroid_x, centroid_y, '*', color='blue', markersize=10, label='Centroid')

        # Adiciona as métricas ao gráfico
        ax.text(2, field["length"] - 2, f'Surface Area: {polygon_area:.2f} m²', fontsize=12, color='black',
                bbox=dict(facecolor='white', alpha=0.7))
        ax.text(2, field["length"] - 5, f'Centroid: ({centroid_x:.2f}, {centroid_y:.2f})', fontsize=12, color='black',
                bbox=dict(facecolor='white', alpha=0.7))

    ax.set_title(f"Football Field with Tracked Object Positions - Frame {frame_number}")
    return []

# Create the animation
#ani = animation.FuncAnimation(fig, update, frames=len(data), init_func=init, blit=True, repeat=False, interval=1)
ani = animation.FuncAnimation(fig, update, data, init_func=init, blit=True, repeat=False, interval=100)
# = animation.FuncAnimation(fig, update, frames=len(data), init_func=init, blit=True, repeat=False, interval=100)
# Show the animation
plt.grid(True)
plt.show()
