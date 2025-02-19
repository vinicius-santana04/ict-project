import json

import numpy as np
import matplotlib.pyplot as plt
from geopy.distance import geodesic
from scipy.stats import gaussian_kde
from fields import select_field
from datetime import datetime

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

def convert_to_field_coordinates(lats, lons, field):
    #print(lat, lon, field)
    xis, yos = [],[]
    for lat in lats:
        yos.append((lat - field["min_lat"]) / (field["max_lat"] - field["min_lat"]) * field["length"])
    for lon in lons:
        xis.append((lon - field["min_lon"]) / (field["max_lon"] - field["min_lon"]) * field["width"])
    return xis, yos

def heatmap(dados):
    """
    Calcula e exibe o heatmap a partir dos dados x e y do jogador.

    Parâmetros:
    - dados: array 2D contendo as coordenadas x e y.

    Retorna:
    - dens2: array 2D representando o heatmap.
    """
    # Criar uma grid de valores
    gridx1 = np.arange(0, 106)  # de 0 a 105
    gridx2 = np.arange(0, 69)   # de 0 a 68
    x1, x2 = np.meshgrid(gridx1, gridx2)

    # Achatar os arrays
    x1 = x1.ravel()
    x2 = x2.ravel()

    # Criar um conjunto de dados 2D
    xi = np.vstack([x1, x2]).T

    # Estimação da densidade do kernel gaussiano
    kde = gaussian_kde(dados.T)
    dens = kde(xi.T)

    # Remodelar para ter o mesmo formato da grid
    dens2 = dens.reshape(gridx2.size, gridx1.size)

    # Plotting
    fig, ax = plt.subplots()
    ax.pcolormesh(gridx1, gridx2, dens2, shading='auto', cmap='viridis')
    ax.grid(False)  # Desligar a grade
    ax.set_aspect('equal', 'box')  # Manter o aspecto do plot
    ax.set_xlim(0, 105)
    ax.set_ylim(0, 68)

    # Adicionando título
    ax.set_title("heatmap")

    # Sobrepondo o campo ao heatmap
    select_field(105, 71, ax)

    plt.show()

    return dens2

def getDados(number):
    with open('../data/result.json') as f:
        data = json.load(f)

    hora_limite = datetime.strptime("20:00:00", "%H:%M:%S")

    latitudes = [
        jogador["lat"]
        for frame, jogadores in data.items()
        if datetime.strptime(frame, "%H:%M:%S") < hora_limite
        for jogador in jogadores
        if jogador["player"] == number
    ]
    longitudes = [
        jogador["lon"]
        for frame, jogadores in data.items()
        if datetime.strptime(frame, "%H:%M:%S") < hora_limite
        for jogador in jogadores
        if jogador["player"] == number
    ]

    xis, yos = convert_to_field_coordinates(latitudes, longitudes, field)

    dados = np.column_stack((np.array(xis), np.array(yos)))

    return dados

dados_teste = getDados("08")
print(dados_teste)
result = heatmap(dados_teste)