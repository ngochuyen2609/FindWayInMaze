from queue import PriorityQueue

def h1(cell1,cell2):
    x1,y1 = cell1
    x2,y2 = cell2
    return abs(x1-x2) + abs(y1-y2)

def h2(cell1,cell2):
    x1,y1 = cell1
    x2,y2 = cell2
    return (x1-x2)*(x1-x2) + (y1-y2)*(y1-y2)

def aStar(maze_map, width, height, source, destination, typ):
    g_score = {}
    f_score = {}
    for x in range (width):
        for y in range (height):
            g_score[(x,y)] = 1e9
            f_score[(x,y)] = 1e9
    g_score[source] = 0
    if(typ == 1):
        f_score[source] = h1(source, destination)
    if (typ == 2):
        f_score[source] = h2(source, destination)

    open = PriorityQueue()
    open.put((f_score[source],source))
    searchPath = []
    aPath={}
    while not open.empty():
        currCell = open.get()[1]
        searchPath.append(currCell)

        if currCell == destination:
            break
        childCells = []

        if maze_map[currCell]['T'] == 1:
            childCells.append( (currCell[0],currCell[1]-1) )
        if maze_map[currCell]['R'] == 1:
            childCells.append( (currCell[0]+1,currCell[1]) )
        if maze_map[currCell]['B'] == 1:
            childCells.append( (currCell[0],currCell[1]+1) )
        if maze_map[currCell]['L'] == 1:
            childCells.append( (currCell[0]-1,currCell[1]) )
        for childCell in childCells:
            temp_g_score = g_score[currCell]+1
            if(typ == 1):
                temp_f_score = temp_g_score + h1(source, destination)
            if (typ == 2):
                temp_f_score = temp_g_score + h2(source, destination)

            if temp_f_score < f_score[childCell]:
                aPath[childCell] = currCell
                g_score[childCell] = temp_g_score
                f_score[childCell] = temp_f_score
                open.put((temp_f_score,childCell))
    fwdPath = []
    cell = destination
    while cell != source:
        fwdPath.append(cell)
        cell = aPath[cell]
    fwdPath.append(source)
    return searchPath, fwdPath

def greedyBFS(maze_map, width, height, source, destination, typ):
    f_score = {}
    for x in range (width):
        for y in range (height):
            f_score[(x,y)] = 1e9

    if(typ == 1):
        f_score[source] = h1(source, destination)
    if (typ == 2):
        f_score[source] = h2(source, destination)

    open = PriorityQueue()
    open.put((f_score[source],source))
    searchPath = []
    aPath={}
    while not open.empty():
        currCell = open.get()[1]
        searchPath.append(currCell)

        if currCell == destination:
            break
        childCells = []

        if maze_map[currCell]['T'] == 1:
            childCells.append( (currCell[0],currCell[1]-1) )
        if maze_map[currCell]['R'] == 1:
            childCells.append( (currCell[0]+1,currCell[1]) )
        if maze_map[currCell]['B'] == 1:
            childCells.append( (currCell[0],currCell[1]+1) )
        if maze_map[currCell]['L'] == 1:
            childCells.append( (currCell[0]-1,currCell[1]) )
        for childCell in childCells:
            if(typ == 1):
                temp_f_score = h1(source, destination)
            if (typ == 2):
                temp_f_score =  h2(source, destination)

            if temp_f_score < f_score[childCell]:
                aPath[childCell] = currCell
                f_score[childCell] = temp_f_score
                open.put((temp_f_score,childCell))
    fwdPath = []
    cell = destination
    while cell != source:
        fwdPath.append(cell)
        cell = aPath[cell]
    fwdPath.append(source)
    return searchPath, fwdPath