import random
import time
import getopt
import sys

class Cell:
    off = "#"
    on = "O"
    def __init__(self, location, state=off):
        self.l = location
        self.s = state

    def move(self, model):
        return True

    def copy(self):
        return type(self)(self.l, self.s)

    def __str__(self):
        return self.s

    def __repr__(self):
        return str(self)

class TrafficCell(Cell):
    off = "-"
    on = "O"

    def move(self, model):
        if self.s == self.on and self.l == model.l-1:
            self.s = self.off
        elif self.s == self.off and model.getTape()[self.l-1].s == self.on and self.l != 0:
            self.s = self.on
        elif self.s == self.on and model.getTape()[self.l+1].s == self.off:
            self.s = self.off
        return True


class LengthError(Exception):
    pass

class Model:
    def __init__(self, length, cell_type, num_cells=0, seed=None):
        if num_cells > length:
            raise LengthError("Error: Your number of cells is greater than the length of your tape")
        self.l = length
        self.c = []
        self.t = cell_type
        if seed:
            if len(seed) != length :
                raise LengthError("Error: Your seed does not match the details entered")
            else:
                for i in range(length):
                    self.c.append(cell_type(i, seed[i]))
        else:
            for i in range(length):
                cell = cell_type(i,cell_type.off)
                self.c.append(cell.copy())

            for i in range(num_cells):
                cell = self.c[random.randint(0,length-1)]
                while cell.s != cell_type.off:
                    cell = self.c[random.randint(0,length-1)]
                cell.s = cell_type.on

        self.i = [None for i in range(self.l)]
        for i in self.c:
            self.i[i.l] = i.copy()

        self.generate_list()

    def show(self):
        output = ["-" for i in range(self.l)]
        for i in self.c:
            output[i.l] = i.s

        s = ""
        for i in output:
            s += i

        print(s)

    def getTape(self):
        return self.i

    def generate_list(self):
        self.p = []
        for i in self.i:
            self.p.append(i.copy())
        self.i = [None for i in range(self.l)]
        for i in self.c:
            self.i[i.l] = i.copy()

    def update(self):
        s = ""
        for i in self.c:
            i.move(self)
            s+= str(i)
        print(s)
        self.generate_list()
        for i in range(len(self.c)):
            if str(self.p[i]) != str(self.c[i]):
                return True

        return False

def usage():
    print()
    print("Cellular Automata 2D Usage")
    print("-h --help: Displays this help screen")
    print("------------------------------------")
    print("Essential Parameters")
    print("-l --length: The length of the string.")
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

def run(length, cell, seed, delay=0.1):
    new_model = Model(length, cell, seed=seed)
    run_model(new_model, delay)

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hl:c:n:d",
                                   ["help", "length", "cell", "num", "delay"])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit()
    length, num, cell, delay = None, None, None, 0.1
    for o, a in opts:
        if o in ("-h","--help"):
            usage()
            sys.exit()
        elif o in ("-l","--length"):
            length = int(a)
        elif o in ("-n","--num"):
            num = int(a)
        elif o in ("-c","--cell"):
            cell = globals()[a]
        elif o in ("-d","--delay"):
            delay = float(a)
        else:
            assert False,"Unhandled Option"

    if not (length and num and cell):
        usage()
    else:
        new_model = Model(length, cell, num)
        run_model(new_model, delay)

if __name__ == "__main__":
    main()
