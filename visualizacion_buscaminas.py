#-*-coding: utf-8-*-
# Visualización de tableros de Buscaminas 5x5 a partir de una interpretación.
# Basado en visualizacion.py (Edgar Andrade, 2018), adaptado al proyecto
# Buscaminas — Lógica para Ciencias de la Computación 2026-II.
# Autores: Juan Camilo Lozano González y Fabiana Vargas Velasco.
#
# Representación: un solo descriptor
#     Casilla = Descriptor([5, 5, 10])
#     N_{x,y,k} = Casilla.ravel([x, y, k])  ≡ "la casilla (x,y) tiene el valor k"
#     k ∈ {0,...,8}: número de minas vecinas;  k = 9: la casilla tiene una mina.
#     x = fila (0 arriba), y = columna (0 a la izquierda).
#
# Entrada: I, diccionario {letra: True/False} (lo que devuelve un SAT-solver).
#          Las letras que no aparecen en I se toman como False (DPLL puede
#          devolver interpretaciones parciales). Las letras fuera del rango del
#          descriptor (p. ej. átomos de Tseitin) se ignoran.
# Salida:  figura en pantalla, o archivo tablero_<n>.png si se da n.

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from Logica import Descriptor

FILAS, COLUMNAS, VALORES = 5, 5, 10
MINA = 9

Casilla = Descriptor([FILAS, COLUMNAS, VALORES])

# Colores clásicos del Buscaminas para los números
COLOR_NUMERO = {1: '#1f4fd1', 2: '#2e7d32', 3: '#c62828', 4: '#1a237e',
                5: '#8d2a00', 6: '#00838f', 7: 'black', 8: 'dimgrey'}


def leer_tablero(I, D=Casilla):
    '''
    Traduce la interpretación I a una matriz de valores.
    Input:  I, diccionario {letra: True/False}
    Output: tablero, lista FILAS x COLUMNAS; cada entrada es la lista de
            valores k tales que N_{x,y,k} es verdadera en I.
            Una casilla bien formada tiene exactamente un valor.
    '''
    tablero = [[[] for _ in range(COLUMNAS)] for _ in range(FILAS)]
    for letra in I:
        if len(letra) != 1 or not I[letra]:
            continue
        if not (D.rango[0] <= ord(letra) < D.rango[1]):   # '<': rango[1] es exclusivo
            continue
        x, y, k = D.unravel(letra)
        tablero[x][y].append(k)
    return tablero


def dibujar_mina(axes, cx, cy, r=0.24):
    '''Dibuja una mina centrada en (cx, cy) solo con patches: cuerpo, 8 púas y brillo.'''
    for i in range(4):  # 4 líneas = 8 púas
        if i == 0:   dx, dy = r * 1.45, 0
        elif i == 1: dx, dy = 0, r * 1.45
        elif i == 2: dx, dy = r * 1.03, r * 1.03
        else:        dx, dy = r * 1.03, -r * 1.03
        axes.add_patch(patches.Polygon([(cx - dx, cy - dy), (cx + dx, cy + dy)],
                                       closed=False, edgecolor='black', linewidth=3))
    axes.add_patch(patches.Circle((cx, cy), r, facecolor='black'))
    axes.add_patch(patches.Circle((cx - r * 0.35, cy - r * 0.35), r * 0.22, facecolor='white'))


def dibujar_tablero(I, n=None, titulo=None, D=Casilla):
    '''
    Visualiza un tablero de Buscaminas dada una interpretación I.
    Input:
      - I, diccionario {letra: True/False}
      - n, número de identificación; si se da, guarda tablero_n.png en vez de mostrar
      - titulo, texto opcional sobre el tablero
    Output:
      - lista de problemas encontrados (casillas sin valor o con más de uno).
        Si la lista está vacía, toda casilla tiene exactamente un valor.

    Convenciones de dibujo:
      - mina (k = 9): fondo rojo claro y mina dibujada
      - número 0: casilla vacía (fondo más claro, como en el juego)
      - número k > 0: el número con su color clásico
      - casilla sin ningún valor verdadero: '?' sobre gris  (viola R1)
      - casilla con más de un valor verdadero: '!' con borde rojo (viola la unicidad)
    '''
    tablero = leer_tablero(I, D)
    problemas = []

    fig, axes = plt.subplots(figsize=(COLUMNAS, FILAS))
    axes.set_xlim(0, COLUMNAS)
    axes.set_ylim(FILAS, 0)          # fila 0 arriba
    axes.set_aspect('equal')
    axes.axis('off')

    for x in range(FILAS):
        for y in range(COLUMNAS):
            valores = tablero[x][y]
            # Esquina superior izquierda de la casilla (x,y): columna y, fila x
            esq = (y, x)
            cx, cy = y + 0.5, x + 0.5

            if len(valores) == 0:
                axes.add_patch(patches.Rectangle(esq, 1, 1, facecolor='lightgrey',
                                                 edgecolor='dimgrey', linewidth=2))
                axes.text(cx, cy, '?', ha='center', va='center', size=30, c='dimgrey')
                problemas.append(f'Casilla ({x},{y}): ningún valor')
            elif len(valores) > 1:
                axes.add_patch(patches.Rectangle(esq, 1, 1, facecolor='mistyrose',
                                                 edgecolor='red', linewidth=4))
                axes.text(cx, cy - 0.12, '!', ha='center', va='center', size=26, c='red')
                axes.text(cx, cy + 0.28, ','.join(str(v) for v in sorted(valores)),
                          ha='center', va='center', size=11, c='red')
                problemas.append(f'Casilla ({x},{y}): varios valores {sorted(valores)}')
            else:
                k = valores[0]
                if k == MINA:
                    axes.add_patch(patches.Rectangle(esq, 1, 1, facecolor='#f4c7c3',
                                                     edgecolor='dimgrey', linewidth=2))
                    dibujar_mina(axes, cx, cy)
                elif k == 0:
                    axes.add_patch(patches.Rectangle(esq, 1, 1, facecolor='#f7f5ef',
                                                     edgecolor='dimgrey', linewidth=2))
                else:
                    axes.add_patch(patches.Rectangle(esq, 1, 1, facecolor='cornsilk',
                                                     edgecolor='dimgrey', linewidth=2))
                    axes.text(cx, cy, str(k), ha='center', va='center', size=30,
                              c=COLOR_NUMERO[k], fontweight='bold')

    # Marco exterior
    axes.add_patch(patches.Rectangle((0, 0), COLUMNAS, FILAS, fill=False,
                                     edgecolor='black', linewidth=4))
    if titulo is not None:
        axes.set_title(titulo, size=14)

    if n is not None:
        fig.savefig('tablero_' + str(n) + '.png', bbox_inches='tight')
        plt.close(fig)
    else:
        plt.show()
    return problemas


def interpretacion_desde_minas(minas, D=Casilla):
    '''
    Construye una interpretación COMPLETA a partir de una lista de minas,
    calculando los números por conteo de vecinos. Sirve para probar el
    visualizador (y más adelante las reglas) sin necesidad de un SAT-solver.
    Input:  minas, lista de casillas (x,y)
    Output: I, diccionario {letra: True/False} con todas las letras del descriptor
    '''
    I = {}
    for x in range(FILAS):
        for y in range(COLUMNAS):
            if (x, y) in minas:
                valor = MINA
            else:
                valor = sum(1 for i in (-1, 0, 1) for j in (-1, 0, 1)
                            if (i, j) != (0, 0) and (x + i, y + j) in minas)
            for k in range(VALORES):
                I[D.ravel([x, y, k])] = (k == valor)
    return I


if __name__ == '__main__':
    # Tablero de ejemplo del paper (Tabla II)
    minas = [(0, 2), (1, 0), (1, 3), (2, 1), (3, 4), (4, 2)]
    I = interpretacion_desde_minas(minas)
    print(dibujar_tablero(I, n=1, titulo='Tabla II'))
