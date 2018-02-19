import random
import time
import getopt
import sys
import os

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = "#"

    def move(self, model):

        return True

    def copy(self):
        return Cell(self.x, self.y)


class LengthError(Exception):
    pass

class Model:
    def __init__(self, xlen, ylen, num_cells, cell_type, seed=None):
        grid = [[None for x in range(xlen)] for y in range(ylen)]
        if num_cells > xlen*ylen:
            raise LengthError("Error: Your number of cells is greater than the area of the grid")
        self.x = xlen
        self.y = ylen
        self.l = xlen*ylen
        self.c = []
        self.t = cell_type
        if seed:
            num = 0
            for i in seed:
                if i == "1": num += 1
            if len(seed) != self.l or num != num_cells:
                raise LengthError("Error: Your seed does not match the details entered")
            else:
                for i in range(self.l):
                    if seed[i] == "1":
                        self.c.append(cell_type(i//xlen, i%xlen))
                return
        for i in range(num_cells):
            cell = None
            while cell == None:
                pos = (random.randint(0,ylen-1),random.randint(0,xlen-1))
                if grid[pos[0]][pos[1]] is None:
                    cell = cell_type(pos[0], pos[1])
                    grid[pos[0]][pos[1]] = cell.copy()
                    self.c.append(cell.copy())

    def show(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        output = [["-" for x in range(self.x)] for y in range(self.y)]
        for i in self.c:
            output[i.y][i.x] = i.state

        s = ""
        for y in range(len(output)-1,-1,-1):
            for x in output[y]:
                s += x
            s += "\n"

        print(s)

    def generate_list(self):
        output = [[None for x in range(self.x)] for y in range(self.y)]
        for i in self.c:
            output[i.y][i.x] = i.copy()

    def update(self):
        dels = []
        self.generate_list()
        for i in self.c:
            if not i.move(self):
                dels.append(i)

        for i in dels:
            self.c.remove(i)

        return self.c

def usage():
    print()
    print("Cellular Automata 3D Usage")
    print("-h --help: Displays this help screen")
    print("------------------------------------")
    print("Essential Parameters")
    print("-x --xlength: The x-length of the grid.")
    print("-y --ylength: The y-length of the grid.")
    print("-n --num: Number of initial cells")
    print("-c --cell: Name of the cell class - must be a subclass of Cell")
    print("Optional Parameters")
    print("-d --delay: Delay between each iteration, for display purposes. Default 0.1s")
    print()

def str_to_class(str):
    return getattr(sys.modules[__name__], str)

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hx:y:n:c:d",
                                   ["help", "xlength", "ylength", "num", "cell", "delay"])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit()
    x, y, num, cell, delay = None, None, None, None, 0.1
    for o, a in opts:
        if o in ("-h","--help"):
            usage()
            sys.exit()
        elif o in ("-x","--xlength"):
            x = int(a)
        elif o in ("-y","--ylength"):
            y = int(a)
        elif o in ("-n","--num"):
            num = int(a)
        elif o in ("-c","--cell"):
            cell = globals()[a]
        elif o in ("-d","--delay"):
            delay = float(a)
        else:
            assert False,"Unhandled Option"

    if not (x and y and num and cell):
        usage()
    else:
        new_model = Model(x, y, num, cell)
        while new_model.update():
            new_model.show()
            time.sleep(delay)

if __name__ == "__main__":
    main()
