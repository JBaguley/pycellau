import random
import time
import getopt
import sys

class Cell:
    def __init__(self, location):
        self.l = location
        self.s = "#"

    def move(self, model):
        if self.l == model.l-1:
            self.l += 1
        elif self.l == model.l or model.i[self.l+1] is None:
            self.l += 1
        return self.l<model.l

    def copy(self):
        return Cell(self.l)


class LengthError(Exception):
    pass

class Model:
    def __init__(self, length, num_cells, cell_type, seed=None):
        tape = [None for i in range(length)]
        if num_cells > length:
            raise LengthError("Error: Your number of cells is greater than the length of your tape")
        self.l = length
        self.c = []
        self.t = cell_type
        if seed:
            num = 0
            for i in seed:
                if i == "1": num += 1
            if len(seed) != length or num != num_cells:
                raise LengthError("Error: Your seed does not match the details entered")
            else:
                for i in range(length):
                    if seed[i] == "1":
                        self.c.append(cell_type(i))
                return
        for i in range(num_cells):
            cell = None
            while cell == None:
                pos = random.randint(0,length-1)
                if tape[pos] is None:
                    cell = cell_type(pos)
                    tape[pos] = cell.copy()
                    self.c.append(cell.copy())

    def show(self):
        output = ["-" for i in range(self.l)]
        for i in self.c:
            output[i.l] = i.s

        s = ""
        for i in output:
            s += i

        print(s)

    def generate_list(self):
        self.i = [None for i in range(self.l)]
        for i in self.c:
            self.i[i.l] = i.copy()

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

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hl:n:c:d",
                                   ["help", "length", "num", "cell", "delay"])
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
        new_model = Model(length, num, cell)
        while new_model.update():
            new_model.show()
            time.sleep(delay)

if __name__ == "__main__":
    main()
