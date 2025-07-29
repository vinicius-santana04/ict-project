import json
from geopy.distance import geodesic
from scipy.spatial import ConvexHull
from scipy.signal import hilbert
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from fields import select_field
import pandas as pd

results_data = []
ict_values = []  # Armazenar ICT por frame

field = {
    "corner1": (20.127965, 40.304853),
    "corner2": (20.128007, 40.303850),
    "corner3": (20.127326, 40.304825),
    "corner4": (20.127381, 40.303826),
}

field["length"] = geodesic(field["corner1"], field["corner2"]).meters
field["width"] = geodesic(field["corner1"], field["corner3"]).meters

latitudes = [field["corner1"][0], field["corner2"][0], field["corner3"][0], field["corner4"][0]]
field["max_lat"] = max(latitudes)
field["min_lat"] = min(latitudes)

longitudes = [field["corner1"][1], field["corner2"][1], field["corner3"][1], field["corner4"][1]]
field["max_lon"] = max(longitudes)  
field["min_lon"] = min(longitudes)

with open('../data/result.json') as f:
    data = json.load(f)

frame_keys = sorted(data.keys())

def convert_to_field_coordinates(lat, lon, field):
    x = (lon - field["min_lon"]) / (field["max_lon"] - field["min_lon"]) * field["width"]
    y = (lat - field["min_lat"]) / (field["max_lat"] - field["min_lat"]) * field["length"]
    return x, y

fig, ax = plt.subplots(figsize=(12, 8))

attackers_centroid_history = []
defenders_centroid_history = []

W_MAX = 30
TAU_MAX = 15

def calculate_cross_correlation(team1_history, team2_history, w_max, tau):
    if tau <= 0:
        w1 = np.array(team1_history[-(w_max + abs(tau)):-abs(tau) if abs(tau) > 0 else len(team1_history)])
        w2 = np.array(team2_history[-w_max:])
    else:
        w1 = np.array(team1_history[-w_max:])
        w2 = np.array(team2_history[-(w_max + tau):-tau])

    min_len = min(len(w1), len(w2))
    w1 = w1[:min_len]
    w2 = w2[:min_len]

    if len(w1) < 2 or len(w2) < 2:
        return 0

    mean1, mean2 = np.mean(w1), np.mean(w2)
    std1, std2 = np.std(w1), np.std(w2)

    if std1 == 0 or std2 == 0:
        return 0

    r = np.sum((w1 - mean1) * (w2 - mean2)) / (min_len * std1 * std2)
    return r

def calculate_instantaneous_ICT(player_phases_frame, current_frame):
    players = list(player_phases_frame.keys())
    if len(players) < 2:
        return None
    total_pairs = 0
    total_in_phase = 0

    for i in range(len(players)):
        for j in range(i + 1, len(players)):
            phi_i = player_phases_frame[players[i]]
            phi_j = player_phases_frame[players[j]]
            if len(phi_i) <= current_frame or len(phi_j) <= current_frame:
                continue
            rel_phase = phi_i[current_frame] - phi_j[current_frame]
            rel_phase = (rel_phase + 180) % 360 - 180
            if abs(rel_phase) < 30:
                total_in_phase += 1
            total_pairs += 1

    if total_pairs == 0:
        return None
    ict = (total_in_phase / total_pairs) * 100
    return ict

def calculate_all_player_phases(data, field):
    player_positions = {}
    for frame_key in sorted(data.keys()):
        objects = data[frame_key]
        for obj in objects:
            player_id = obj.get("player")
            lat, lon = obj.get("lat"), obj.get("lon")
            if player_id and lat and lon:
                x, y = convert_to_field_coordinates(lat, lon, field)
                if player_id not in player_positions:
                    player_positions[player_id] = []
                player_positions[player_id].append((x, y))

    player_phases = {}
    for player, positions in player_positions.items():
        positions = np.array(positions)
        if len(positions) < 2:
            continue
        signal = np.linalg.norm(positions - positions[0], axis=1)
        analytic_signal = hilbert(signal)
        instantaneous_phase = np.angle(analytic_signal, deg=True)
        player_phases[player] = instantaneous_phase
    return player_phases

player_phases_frame = calculate_all_player_phases(data, field)

def init():
    ax.set_xlim(0, field["length"])
    ax.set_ylim(0, field["width"])
    ax.set_xlabel('Posição X (metros)')
    ax.set_ylabel('Posição Y (metros)')
    ax.set_title('Campo de Futebol com Posições Rastreadas e ICT')
    return []

def update(frame_key):
    ax.clear()
    select_field(105, 71, ax)
    init()

    objects = data[frame_key]
    attackers, midfielders, defenders, other_players = [], [], [], []

    for obj in objects:
        x, y = convert_to_field_coordinates(obj.get('lat'), obj.get('lon'), field)
        player_num = obj.get('player')

        if 0 <= x <= field["length"] and 0 <= y <= field["width"]:
            if player_num in ["01", "02", "03"]:
                attackers.append([x, y])
                ax.plot(x, y, 'ro', label="Atacantes" if len(attackers) == 1 else "")
            elif player_num in ["04", "06", "10"]:
                midfielders.append([x, y])
                ax.plot(x, y, 'yo', label="Meio-campistas" if len(midfielders) == 1 else "")
            elif player_num in ["05", "07", "09"]:
                defenders.append([x, y])
                ax.plot(x, y, 'bo', label="Defensores" if len(defenders) == 1 else "")
            else:
                other_players.append([x, y])
                ax.plot(x, y, 'go', label="Outros" if len(other_players) == 1 else "")

    def get_centroid(players, color, label):
        centroid_x, centroid_y = None, None
        if len(players) > 2:
            players_np = np.array(players)
            players_np = np.unique(players_np, axis=0)
            if len(players_np) > 2:
                hull = ConvexHull(players_np)
                hull_points = players_np[hull.vertices]
                centroid_x = np.mean(hull_points[:, 0])
                centroid_y = np.mean(hull_points[:, 1])
                ax.fill(hull_points[:, 0], hull_points[:, 1], color, alpha=0.5, label=label)
                ax.plot(centroid_x, centroid_y, '^', color='black', markersize=8)
        return centroid_x, centroid_y

    attacker_centroid = get_centroid(attackers, 'red', "Área dos Atacantes")
    defender_centroid = get_centroid(defenders, 'blue', "Área dos Defensores")
    get_centroid(midfielders, 'yellow', "Área dos Meio-campistas")

    frame_index = frame_keys.index(frame_key)
    ict_frame = calculate_instantaneous_ICT(player_phases_frame, current_frame=frame_index)

    if ict_frame is not None:
        ict_values.append(ict_frame)
    else:
        ict_values.append(np.nan)

    metrics_text = f"ICT (Coordenação): {ict_frame:.2f}%" if ict_frame is not None else "ICT: N/A"
    ax.text(0.98, 0.98, metrics_text, transform=ax.transAxes, fontsize=12,
            verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    frame_data = {
        'Frame': frame_key,
        'ICT': ict_frame,
        'Attacker_Centroid_X': attacker_centroid[0] if attacker_centroid else None,
        'Attacker_Centroid_Y': attacker_centroid[1] if attacker_centroid else None,
        'Defender_Centroid_X': defender_centroid[0] if defender_centroid else None,
        'Defender_Centroid_Y': defender_centroid[1] if defender_centroid else None,
    }

    results_data.append(frame_data)
    ax.legend(loc='upper left')
    ax.set_title(f"Quadro {frame_key}")
    return []

ani = animation.FuncAnimation(fig, update, frames=frame_keys, init_func=init, blit=False, repeat=False, interval=70)
plt.grid(True)
plt.show()

print("\nAnimação finalizada. Salvando dados para o arquivo Excel...")

if results_data:
    df = pd.DataFrame(results_data)
    output_filename = 'time_delay_analysis_with_ICT.xlsx'
    try:
        df.to_excel(output_filename, index=False, engine='openpyxl')
        print(f"Sucesso! Os dados foram salvos em '{output_filename}'")
    except Exception as e:
        print(f"Ocorreu um erro ao salvar o arquivo: {e}")
else:
    print("Nenhum dado foi coletado para salvar.")

# Gráfico ICT
print("Gerando gráfico da evolução da ICT...")
plt.figure(figsize=(10, 4))
plt.plot(ict_values, label="ICT (%)", color='purple', linewidth=2)
plt.axhline(70, color='orange', linestyle='--', label="Coordenação boa (70%)")
plt.axhline(40, color='red', linestyle='--', label="Coordenação fraca (40%)")
plt.title("Evolução da Intra-team Coordination Tendency (ICT)")
plt.xlabel("Quadro (Frame)")
plt.ylabel("ICT (%)")
plt.ylim(0, 100)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("evolucao_ict.png")
plt.show()

# Nova função: análise de trajetória e melhores momentos
def analisar_trajetoria_e_ict(data, ict_values, player_phases_frame, frame_keys, field, threshold=90):
    print("Analisando trajetórias e momentos de alta coordenação...")

    metade = len(frame_keys) // 2
    tempos = {
        "Primeiro Tempo": frame_keys[:metade],
        "Segundo Tempo": frame_keys[metade:]
    }

    for tempo_nome, tempo_frames in tempos.items():
        melhores_momentos = []
        trajetorias = {}

        for idx, frame_key in enumerate(tempo_frames):
            frame_index = frame_keys.index(frame_key)
            ict = ict_values[frame_index]

            if ict is not None and ict >= threshold:
                melhores_momentos.append((frame_key, ict))

            for obj in data[frame_key]:
                player = obj.get("player")
                if player and obj.get("lat") and obj.get("lon"):
                    x, y = convert_to_field_coordinates(obj['lat'], obj['lon'], field)
                    if player not in trajetorias:
                        trajetorias[player] = []
                    trajetorias[player].append((x, y))

        # Plotagem da trajetória
        fig, ax = plt.subplots(figsize=(12, 7))
        select_field(105, 71, ax)
        ax.set_title(f"Trajetória dos Jogadores – {tempo_nome}")
        ax.set_xlabel("Posição X (m)")
        ax.set_ylabel("Posição Y (m)")

        for player, traj in trajetorias.items():
            if len(traj) > 1:
                traj_np = np.array(traj)
                ax.plot(traj_np[:, 0], traj_np[:, 1], label=f"Jogador {player}")

        if melhores_momentos:
            textos = [f"Frame {f} - ICT: {ict:.1f}%" for f, ict in melhores_momentos]
            print(f"\n{tempo_nome} - Melhores Momentos (ICT >= {threshold}%):")
            for t in textos:
                print("  -", t)

            ax.text(0.5, -0.1, "\n".join(textos[:5]), transform=ax.transAxes, fontsize=10,
                    verticalalignment='top', horizontalalignment='center',
                    bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.6))
        else:
            print(f"\n{tempo_nome}: Nenhum momento com ICT >= {threshold}%.")

        # ax.legend(loc='upper right', fontsize=8)
        # plt.tight_layout()
        # plt.grid(True)
        # plt.savefig(f"trajetoria_{tempo_nome.lower().replace(' ', '_')}.png")
        # plt.show()


        # ax.legend(loc='upper right', fontsize=8)
        # plt.tight_layout()
        # plt.grid(True)
        # plt.savefig(f"trajetoria_{tempo_nome.lower().replace(' ', '_')}.png")
        # plt.show()

ict_values = []
for i in range(len(frame_keys)):
    ict = calculate_instantaneous_ICT(player_phases_frame, i)
    ict_values.append(ict)

analisar_trajetoria_e_ict(data, ict_values, player_phases_frame, frame_keys, field)


# ICT = (num de pares em fase / num total de pares) * 100

# | TIC (%)     | Interpretação                                 |
# | ----------- | --------------------------------------------- |
# | **90–100%** | Excelente cooperação em grupo                 |
# | **70–89%**  | Boa eficiência, mas com espaço para melhorias |
# | **40–69%**  | Coordenação moderada                          |
# | **< 40%**   | Pouca progressiva, movimentos desincronizados |