import networkx as nx

# Создание графа Sudoku
def build_sudoku_graph():
    G = nx.Graph()
    for row in range(9):
        for col in range(9):
            cell = (row, col)
            G.add_node(cell)

            # Связи по строке и столбцу
            for i in range(9):
                if i != col:
                    G.add_edge(cell, (row, i))
                if i != row:
                    G.add_edge(cell, (i, col))

            # Связи по квадрату 3x3
            box_row = (row // 3) * 3
            box_col = (col // 3) * 3
            for i in range(box_row, box_row + 3):
                for j in range(box_col, box_col + 3):
                    if (i, j) != cell:
                        G.add_edge(cell, (i, j))
    return G

# Жадная раскраска с учётом начальных значений
def sudoku_coloring(graph, puzzle):
    coloring = {}

    # Сначала раскрасим предзаполненные клетки
    for row in range(9):
        for col in range(9):
            val = puzzle[row][col]
            if val != 0:
                coloring[(row, col)] = val - 1  # 0-based color

    # Теперь раскрашиваем остальные
    for node in graph.nodes():
        if node not in coloring:
            neighbor_colors = {coloring[neighbor] for neighbor in graph.neighbors(node) if neighbor in coloring}
            for color in range(9):
                if color not in neighbor_colors:
                    coloring[node] = color
                    break
    return coloring

# Пример Sudoku (0 — пустая клетка)
puzzle = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

# Создание графа и раскраска
G = build_sudoku_graph()
solution = sudoku_coloring(G, puzzle)

# Печать результата
print("Solved Sudoku:")
for row in range(9):
    print(' '.join(str(solution[(row, col)] + 1) for col in range(9)))
