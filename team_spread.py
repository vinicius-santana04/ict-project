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
with open('../ict-project/data/result.json') as f:
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

        if 0 <= x <= field["width"] and 0 <= y <= field["length"]:
            points.append([x, y])

    # Calcula o polígono usando o ConvexHull
    if len(points) > 2:
        points = np.array(points)
        num_players = points.shape[0]

        #Matriz de distancias entre jogadores
        dist_matrix = np.zeros((num_players, num_players - 1))
        for w in range(num_players):
            matXYPlay = points[w]
            dres = []
            for z in range(num_players):
                if z != w:
                    matcomp = points[z]
                    dist = np.linalg.norm(matXYPlay - matcomp)
                    dres.append(dist)
            dist_matrix[w] = dres

        spread = np.linalg.norm(dist_matrix, axis = 1)

        spread_mean = np.mean(spread)
        spread_median = np.median(spread)
        std_spread = np.std(spread)

        hull = ConvexHull(points)
        hull_points = points[hull.vertices]

        # Obtém o centróide do polígono
        centroid_x = np.mean(hull_points[:, 0])
        centroid_y = np.mean(hull_points[:, 1])

        # Marca o centróide no gráfico
        ax.plot(centroid_x, centroid_y, '*', color='blue', markersize=10, label='Centroid')

        # Connecting Players
        for i in range(num_players):
            for j in range(i + 1, num_players):  # Apenas uma vez para cada par
                ax.plot([points[i, 0], points[j, 0]], [points[i, 1], points[j, 1]], 'k--', linewidth=1)

        # Exibição das métricas no gráfico
        ax.text(2, field["width"] - 2, f"Spread Médio: {spread_mean:.2f}", fontsize=12, color='black',
                bbox=dict(facecolor='white', alpha=0.7))
        ax.text(2, field["width"] - 5, f"Spread Mediano: {spread_median:.2f}", fontsize=12, color='black',
                bbox=dict(facecolor='white', alpha=0.7))
        ax.text(2, field["width"] - 8, f"Desvio Padrão: {std_spread:.2f}", fontsize=12, color='black',
                bbox=dict(facecolor='white', alpha=0.7))

    ax.set_title(f"Football Field with Tracked Object Positions - Frame {frame_number}")
    return []

# Create the animation
ani = animation.FuncAnimation(fig, update, data, init_func=init, blit=True, repeat=False, interval=100)

# Show the animation
plt.grid(True)
plt.show()