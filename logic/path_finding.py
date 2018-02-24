import copy
from queue import PriorityQueue

from engine.logger import Logger, logged


def dist(point1, point2):
    y1, x1 = point1
    y2, x2 = point2
    return max(abs(y2-y1), abs(x2-x1))


def get_direction_towards_target(cells, start, finish):
    p = get_path_towards_target(cells, start, finish)
    if p is not None:
        return cells[p[1][0]][p[1][1]]
    return None


def neigh4(point, cells, ignore=None):
    y, x = point
    h = len(cells)
    w = len(cells[0])
    neighs = []
    #                (y - 1, x)
    # (y, x - 1)                     (y, x + 1)
    #                (y + 1, x)
    if y-1>=0 and cells[y-1][x].walkable(True) and ignore != (y - 1, x):
        neighs.append((y - 1, x))
    if x-1>=0 and cells[y][x-1].walkable(True) and ignore != (y, x - 1):
        neighs.append((y, x - 1))
    if x+1<w and cells[y][x+1].walkable(True) and ignore != (y, x + 1):
        neighs.append((y, x + 1))
    if y+1<h and cells[y+1][x].walkable(True) and ignore != (y + 1, x):
        neighs.append((y + 1, x))
    return neighs


def neigh4plain(point, _, ignore=None):
    y, x = point
    neighs = [x for x in [(y - 1, x), (y, x - 1), (y, x + 1), (y + 1, x)] if x != ignore]
    return neighs



def get_path_towards_target(cells, start, finish, successors=neigh4):
    if start == finish:
        return None
    closed = set()
    open = PriorityQueue()
    open.put((1+dist(start, finish), [start]))
    traversed = set()

    Logger.debug("Searching path from {} to {}".format(start, finish))

    i = 0
    while not open.empty():
        Logger.debug(" > Iteration #{}".format(i))
        Logger.debug(" > Queue contents: {}".format(open))
        Logger.debug(" > Closed set: {}".format(closed))
        Logger.debug(" > Traversed set: {}".format(traversed))
        i += 1

        p = open.get()[1]
        x = p[-1]
        Logger.debug("    x pt := {}".format(x))
        Logger.debug("    path := {}".format(p))

        if tuple(x) in closed:
            Logger.debug("    x is in the closed set, continuing...")
            continue
        if x == finish:
            Logger.debug("Finishing point reached")
            return p
        closed.add(tuple(x))
        Logger.debug("    x is in the closed set now")
        for y in successors(x, cells, p[-2] if len(p) > 1 else None):
            Logger.debug("    y pt := {}".format(y))
            newpath = copy.deepcopy(p)
            newpath.append(y)
            #if tuple(newpath) not in traversed:
            Logger.debug("        path + y is not in traversed")
            priority = dist(y, finish) + len(p) + 1
            open.put((priority, newpath))
            Logger.debug("        path + y added to open with {} priority".format(priority))
            #traversed.add(tuple(newpath))
            #else:
                #Logger.debug("        path + y is already traversed")
    return None


def validate_visual_range(cells, start, finish, range):
    if dist(start, finish) > range:
        return False
    path = get_path_towards_target(cells, start, finish, neigh4plain)
    for point in path[1:-1]:
        cell = cells[point[0]][point[1]]
        if not cell.walkable(True):
            return False
    return True
