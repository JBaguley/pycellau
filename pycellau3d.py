import random
import time
import getopt
import sys
import os

class Cell:
    off = "#"
    on = "O"

    def __init__(self, x, y, state=off):
        self.x = x
        self.y = y
        self.s = state

    def update(self, model):
        return True

    def copy(self):
        return type(self)(self.x, self.y, self.s)

    def __str__(self):
        return self.s

    def __repr__(self):
        return str(self)


class GoLCell(Cell):
    off = "#"
    on = "O"

    def update(self, model):
        counter = 0
        for i in range(9):
            if model.getGrid()[(self.y+i%3-1)%model.y][(self.x+i//3-1)%model.x].s == self.on:
                counter += 1
        if self.s == self.on:
            counter -= 1
            if counter < 2 or counter >= 4:
                self.s = self.off
        else:
            if counter == 3:
                self.s = self.on
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
            for y in range(self.y):
                for x in range(self.x):
                    self.g[y][x] = cell_type(x, y, seed[y][x])
        else:
            for i in range(self.l):
                cell = cell_type(i%xlen,i//ylen,cell_type.off)
                self.g[i//ylen][i%xlen] = cell.copy()

            for i in range(num_cells):
                cell = self.g[random.randint(0,ylen-1)][random.randint(0,xlen-1)]
                while cell.s != cell_type.off:
                    cell = self.g[random.randint(0,ylen-1)][random.randint(0,xlen-1)]
                cell.s = cell_type.on


        self.generate_cg()

    def getGrid(self):
        return self.cg

    def show(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        output = [[self.g[y][x].s for x in range(self.x)] for y in range(self.y)]
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
                x.update(self)
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
    ins = ["-h","-x","-y","-c","-n","-d"]
    insWord = ["--help", "--xlength", "--ylength", "--cell", "--num", "--delay"]
    opts = []
    used = []
    try:
        for i in range(0,len(sys.argv[1:]),2):
            if (sys.argv[1+i] in ins or sys.argv[1+i] in insWord) and sys.argv[1+i] not in used:
                opts.append([sys.argv[1+i],sys.argv[2+i]])
                used.append(sys.argv[1+i])
            else:
                raise ValueError("Parameter error, either parameter does not exist or has been repeated: "+str(sys.argv[1+i]))

    except ValueError as err:
        print(err)
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
