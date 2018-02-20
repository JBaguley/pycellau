import random
import time
import getopt
import sys
import os

class Cell:
    def __init__(self, x, y, state="#"):
        self.x = x
        self.y = y
        self.state = state

    def move(self, model):
        return True

    def copy(self):
        return Cell(self.x, self.y, self.state)

    def __str__(self):
        return self.state

    def __repr__(self):
        return str(self)


class GoLCell(Cell):
    def move(self, model):
        counter = 0
        for i in range(9):
            if model.getGrid()[(self.y+i%3-1)%model.y][(self.x+i//3-1)%model.x].state == "O":
                counter += 1
        if self.state == "O":
            counter -= 1
            if counter < 2 or counter >= 4:
                self.state = "#"
                return True
        else:
            if counter == 3:
                self.state = "O"
                return True


class LengthError(Exception):
    pass


class Model:
    def __init__(self, xlen, ylen, cell_type, num_cells=0, seed=None):
        self.cg = [[None for x in range(xlen)] for y in range(ylen)]
        self.g = [[None for x in range(xlen)] for y in range(ylen)]
        if num_cells > xlen*ylen:
            raise LengthError("Error: Your number of cells is greater than the area of the grid")
        self.x = xlen
        self.y = ylen
        self.l = xlen*ylen
        self.t = cell_type
        if seed:
            for i in range(self.l):
                self.g[i//ylen][i%xlen] = cell_type(i//ylen, i%xlen)
                self.g[i//ylen][i%xlen].state = seed[i//self.y][i%self.x]
        else:
            for i in range(num_cells):
                cell = None
                while cell == None:
                    pos = (random.randint(0,ylen-1),random.randint(0,xlen-1))
                    if self.g[pos[0]][pos[1]] is None:
                        cell = cell_type(pos[0], pos[1])
                        self.g[pos[0]][pos[1]] = cell.copy()

        self.generate_cg()

    def getGrid(self):
        return self.cg

    def show(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        output = [[self.g[y][x].state for x in range(self.x)] for y in range(self.y)]
        s = ""
        for y in range(self.y-1,-1,-1):
            for x in output[y]:
                s += x
            s += "\n"

        print(s)

    def generate_cg(self):
        self.cg = [[None for x in range(self.x)] for y in range(self.y)]
        for y in self.g:
            for x in y:
                self.cg[x.y][x.x] = x.copy()

    def update(self):
        for y in self.g:
            for x in y:
                x.move(self)
        self.generate_cg()
        return True


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

def run_model(model, delay):
    model.show()
    while model.update():
        model.show()
        time.sleep(delay)

def run(xlength, ylength, cell, seed, delay=0.1):
    new_model = Model(xlength, ylength, cell, seed=seed)
    run_model(new_model, delay)


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hx:y:c:n:d",
                                   ["help", "xlength", "ylength", "cell", "num", "delay"])
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
        new_model = Model(x, y, cell, num_cells=num)
        run_model(new_model, delay)

if __name__ == "__main__":
    main()
