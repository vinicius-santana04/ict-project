import matplotlib.pyplot as plt
import numpy as np

def select_field(length, width):
    if length < 70:
        pass
        # small_field(length, width)
    else:
        big_field(length, width)

# def small_field(length, width):
#     print("Executando small field")
#
#     # Cores e configurações do campo
#     c = [0, 0.7, 0]  # Cor do campo (verde)
#     comp, larg = length, width  # Dimensões do campo (comprimento x largura)
#
#     # Configuração do gráfico
#     fig, ax = plt.subplots()
#     ax.set_facecolor(c)  # Define a cor de fundo do campo
#     ax.set_xlim([-2, comp + 2])  # Limites do eixo X
#     ax.set_ylim([-2, larg + 2])  # Limites do eixo Y
#     ax.set_aspect('equal')  # Mantém a proporção 1:1
#
#     # Linha central
#     ax.plot([comp / 2, comp / 2], [0, larg], 'w-', linewidth=2.5)
#
#     # Linhas de fundo
#     ax.plot([0, 0], [0, larg], 'w-', linewidth=2.5)
#     ax.plot([comp, comp], [0, larg], 'w-', linewidth=2.5)
#
#     # Linhas laterais
#     ax.plot([0, comp], [0, 0], 'w-', linewidth=2.5)
#     ax.plot([0, comp], [larg, larg], 'w-', linewidth=2.5)
#
#     # Círculo central
#     ang1 = np.linspace(-np.pi, np.pi, 100)
#     x1 = (3 * np.cos(ang1)) + comp / 2
#     y1 = (3 * np.sin(ang1)) + larg / 2
#     ax.plot(x1, y1, 'w-', linewidth=2.5)
#
#     # Área esquerda (Grande)
#     ax.plot([comp * 0.16, comp * 0.16], [(larg / 2) - comp * 0.16, (larg / 2) + comp * 0.16], 'w-', linewidth=2.5)
#     ax.plot([0, comp * 0.16], [(larg / 2) - comp * 0.16, (larg / 2) - comp * 0.16], 'w-', linewidth=2.5)
#     ax.plot([0, comp * 0.16], [(larg / 2) + comp * 0.16, (larg / 2) + comp * 0.16], 'w-', linewidth=2.5)
#
#     # Área esquerda (Pequena)
#     ax.plot([comp * 0.07, comp * 0.07], [(larg / 2) - comp * 0.07, (larg / 2) + comp * 0.07], 'w-', linewidth=2.5)
#     ax.plot([0, comp * 0.07], [(larg / 2) - comp * 0.07, (larg / 2) - comp * 0.07], 'w-', linewidth=2.5)
#     ax.plot([0, comp * 0.07], [(larg / 2) + comp * 0.07, (larg / 2) + comp * 0.07], 'w-', linewidth=2.5)
#
#     # Área direita (Grande)
#     ax.plot([comp * 0.84, comp * 0.84], [(larg / 2) - comp * 0.16, (larg / 2) + comp * 0.16], 'w-', linewidth=2.5)
#     ax.plot([comp - comp * 0.16, comp], [(larg / 2) - comp * 0.16, (larg / 2) - comp * 0.16], 'w-', linewidth=2.5)
#     ax.plot([comp - comp * 0.16, comp], [(larg / 2) + comp * 0.16, (larg / 2) + comp * 0.16], 'w-', linewidth=2.5)
#
#     # Área direita (Pequena)
#     ax.plot([comp * 0.93, comp * 0.93], [(larg / 2) - comp * 0.07, (larg / 2) + comp * 0.07], 'w-', linewidth=2.5)
#     ax.plot([comp - comp * 0.07, comp], [(larg / 2) - comp * 0.07, (larg / 2) - comp * 0.07], 'w-', linewidth=2.5)
#     ax.plot([comp - comp * 0.07, comp], [(larg / 2) + comp * 0.07, (larg / 2) + comp * 0.07], 'w-', linewidth=2.5)
#
#     # Pontos de penalidade
#     ax.plot(comp * 0.1, larg / 2, 'w.', markersize=15)
#     ax.plot(comp - comp * 0.1, larg / 2, 'w.', markersize=15)
#     ax.plot(comp / 2, larg / 2, 'w.', markersize=15)
#
#     # Remover eixos
#     ax.set_xticks([])
#     ax.set_yticks([])
#     ax.set_xticklabels([])
#     ax.set_yticklabels([])
#     ax.spines['top'].set_visible(False)
#     ax.spines['right'].set_visible(False)
#     ax.spines['bottom'].set_visible(False)
#     ax.spines['left'].set_visible(False)
#
#     plt.show()

def big_field(length, width):

    print("Executando big field")

    # Cores e configurações do campo
    c = [0, 0.7, 0]  # Cor do campo (verde)
    comp, larg = length, width  # Dimensões do campo (comprimento x largura)

    # Configuração do gráfico
    fig, ax = plt.subplots()
    ax.set_facecolor(c)  # Define a cor de fundo do campo
    ax.set_xlim([-5, comp + 5])  # Limites do eixo X
    ax.set_ylim([-5, larg + 5])  # Limites do eixo Y
    ax.set_aspect('equal')  # Mantém a proporção 1:1

    # Linha central
    ax.plot([comp / 2, comp / 2], [0, larg], 'w-', linewidth=2.5)

    # Linhas de fundo
    ax.plot([0, 0], [0, larg], 'w-', linewidth=2.5)
    ax.plot([comp, comp], [0, larg], 'w-', linewidth=2.5)

    # Linhas laterais
    ax.plot([0, comp], [0, 0], 'w-', linewidth=2.5)
    ax.plot([0, comp], [larg, larg], 'w-', linewidth=2.5)

    # Grandes áreas
    ax.plot([0, 16.5], [(larg / 2) - 20.16, (larg / 2) - 20.16], 'w-', linewidth=2.5)
    ax.plot([0, 16.5], [(larg / 2) + 20.16, (larg / 2) + 20.16], 'w-', linewidth=2.5)
    ax.plot([16.5, 16.5], [(larg / 2) - 20.16, (larg / 2) + 20.16], 'w-', linewidth=2.5)
    ax.plot([0, 5.5], [(larg / 2) - 9.16, (larg / 2) - 9.16], 'w-', linewidth=2.5)
    ax.plot([5.5, 5.5], [(larg / 2) - 9.16, (larg / 2) + 9.16], 'w-', linewidth=2.5)
    ax.plot([comp - 16.5, comp], [(larg / 2) - 20.16, (larg / 2) - 20.16], 'w-', linewidth=2.5)
    ax.plot([comp - 16.5, comp], [(larg / 2) + 20.16, (larg / 2) + 20.16], 'w-', linewidth=2.5)
    ax.plot([comp - 16.5, comp - 16.5], [(larg / 2) - 20.16, (larg / 2) + 20.16], 'w-', linewidth=2.5)

    # Pequenas áreas
    # ax.plot([0, 5.5], [(larg / 2) - 9.16, (larg / 2) - 9.16], 'w-', linewidth=2.5)
    ax.plot([5.5, 5.5], [(larg / 2) - 9.16, (larg / 2) + 9.16], 'w-', linewidth=2.5)
    ax.plot([0, 5.5], [(larg / 2) + 9.16, (larg / 2) + 9.16], 'w-', linewidth=2.5)
    ax.plot([comp - 5.5, comp], [(larg / 2) - 9.16, (larg / 2) - 9.16], 'w-', linewidth=2.5)
    ax.plot([comp - 5.5, comp], [(larg / 2) + 9.16, (larg / 2) + 9.16], 'w-', linewidth=2.5)
    ax.plot([comp - 5.5, comp - 5.5], [(larg / 2) - 9.16, (larg / 2) + 9.16], 'w-', linewidth=2.5)

    # Círculos
    # centro = ax.plot(comp / 2, larg / 2, 'w.', markersize=20)
    # penalti1 = ax.plot(11, larg / 2, 'w.', markersize=20)
    # penalti2 = ax.plot(comp - 11, larg / 2, 'w.', markersize=20)

    # Círculo central
    ang1 = np.linspace(-np.pi, np.pi, 100)
    x1 = (9.15 * np.cos(ang1)) + comp / 2
    y1 = (9.15 * np.sin(ang1)) + larg / 2
    ax.plot(x1, y1, 'w-', linewidth=2.5)

    # Arcos das áreas
    ang2 = np.linspace(-np.pi / 3.5, np.pi / 3.5, 100)
    x2 = (9.15 * np.cos(ang2)) + 11
    y2 = (9.15 * np.sin(ang2)) + larg / 2
    ax.plot(x2, y2, 'w-', linewidth=2.5)

    ang3 = np.linspace((-np.pi / 3.5) + np.pi, (np.pi / 3.5) + np.pi, 100)
    x3 = (9.15 * np.cos(ang3)) + comp - 11
    y3 = (9.15 * np.sin(ang3)) + larg / 2
    ax.plot(x3, y3, 'w-', linewidth=2.5)

    # Remover eixos
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    plt.show()

if __name__ == "__main__":
    select_field(104, 70)