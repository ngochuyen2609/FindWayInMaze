from queue import PriorityQueue
import math

def h1(cell1, cell2):
    x1, y1 = cell1
    x2, y2 = cell2
    return abs(x1 - x2) + abs(y1 - y2)

def h2(cell1, cell2):
    x1, y1 = cell1
    x2, y2 = cell2
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def aStar(maze_map, width, height, source, destination, typ):
    g_score = {cell: float('inf') for x in range(width) for y in range(height) for cell in [(x, y)]}
    f_score = {cell: float('inf') for x in range(width) for y in range(height) for cell in [(x, y)]}
    g_score[source] = 0
    f_score[source] = h1(source, destination) if typ == 1 else h2(source, destination)

    open = PriorityQueue()
    open.put((f_score[source], source))
    searchPath = []
    aPath = {}
    closed_set = set()

    while not open.empty():
        currCell = open.get()[1]
        if currCell in closed_set:
            continue

        closed_set.add(currCell)
        searchPath.append(currCell)

        if currCell == destination:
            break

        directions = {
            'T': (0, -1),
            'R': (1, 0),
            'B': (0, 1),
            'L': (-1, 0)
        }

        for direction, (dx, dy) in directions.items():
            if maze_map[currCell][direction] == 1:
                childCell = (currCell[0] + dx, currCell[1] + dy)
                temp_g_score = g_score[currCell] + 1
                temp_f_score = temp_g_score + (h1(childCell, destination) if typ == 1 else h2(childCell, destination))

                if temp_f_score < f_score[childCell]:
                    aPath[childCell] = currCell
                    g_score[childCell] = temp_g_score
                    f_score[childCell] = temp_f_score
                    open.put((temp_f_score, childCell))

    if destination not in aPath:
        return searchPath, []  # No path found

    fwdPath = []
    cell = destination
    while cell != source:
        fwdPath.append(cell)
        cell = aPath[cell]
    fwdPath.append(source)
    fwdPath.reverse()
    return searchPath, fwdPath

def greedyBFS(maze_map, width, height, source, destination, typ):
    f_score = {cell: float('inf') for x in range(width) for y in range(height) for cell in [(x, y)]}
    f_score[source] = h1(source, destination) if typ == 1 else h2(source, destination)

    open = PriorityQueue()
    open.put((f_score[source], source))
    searchPath = []
    aPath = {}
    closed_set = set()

    while not open.empty():
        currCell = open.get()[1]
        if currCell in closed_set:
            continue

        closed_set.add(currCell)
        searchPath.append(currCell)

        if currCell == destination:
            break

        directions = {
            'T': (0, -1),
            'R': (1, 0),
            'B': (0, 1),
            'L': (-1, 0)
        }

        for direction, (dx, dy) in directions.items():
            if maze_map[currCell][direction] == 1:
                childCell = (currCell[0] + dx, currCell[1] + dy)
                temp_f_score = h1(childCell, destination) if typ == 1 else h2(childCell, destination)

                if temp_f_score < f_score[childCell]:
                    aPath[childCell] = currCell
                    f_score[childCell] = temp_f_score
                    open.put((temp_f_score, childCell))

    if destination not in aPath:
        return searchPath, []  # No path found

    fwdPath = []
    cell = destination
    while cell != source:
        fwdPath.append(cell)
        cell = aPath[cell]
    fwdPath.append(source)
    fwdPath.reverse()
    return searchPath, fwdPath
