import json
from geopy.distance import geodesic
from scipy.spatial import ConvexHull
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from fields import select_field

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

    select_field(105, 71, ax)

    return []


def update(frame_number):
    ax.clear()
    init()

    objects = data[str(frame_number)]

    attackers = []
    midfielders = []
    defenders = []
    other_players = []

    for obj in objects:
        x, y = convert_to_field_coordinates(obj.get('lat'), obj.get('lon'), field)
        player_num = obj.get('player')

        if 0 <= x <= field["length"] and 0 <= y <= field["width"]:
            ax.text(x, y, f"Player-{player_num}", fontsize=10, color='black', ha="left", va="bottom")

            if player_num in ["01", "02", "03"]:
                attackers.append([x, y])
                ax.plot(x, y, 'ro', label="Atacantes" if len(attackers) == 1 else "")  # Vermelho
            elif player_num in ["04", "06", "10"]:
                midfielders.append([x, y])
                ax.plot(x, y, 'yo', label="Meia" if len(midfielders) == 1 else "")  # yellow
            elif player_num in ["05", "07", "09"]:
                defenders.append([x, y])
                ax.plot(x, y, 'bo', label="Defensor" if len(defenders) == 1 else "")  # blue
            else:
                other_players.append([x, y])
                ax.plot(x, y, 'go', label="Outros jogadores" if len(other_players) == 1 else "")  # Verde


    def plot_convex_hull(players, color, label):
        if len(players) > 2:
            players = np.array(players)
            hull = ConvexHull(players)
            hull_points = players[hull.vertices]

            centroid_x = np.mean(hull_points[:, 0])
            centroid_y = np.mean(hull_points[:, 1])

            ax.fill(hull_points[:, 0], hull_points[:, 1], color, alpha=0.5, label=label)
            ax.plot(centroid_x, centroid_y, '^', color='black', markersize=7, label=f'Centroid {label}')
        else: return

    plot_convex_hull(attackers, 'red', "Área dos atacantes")
    plot_convex_hull(midfielders, 'yellow', "Área dos meio-campistas")
    plot_convex_hull(defenders, 'blue', "Área dos defensores")


    ax.legend()
    ax.set_title(f"Football Field with Tracked Object Positions - Frame {frame_number}")
    return []


# Create the animation
ani = animation.FuncAnimation(fig, update, data, init_func=init, blit=True, repeat=False, interval=70)

# Show the animation
plt.grid(True)
plt.show()
