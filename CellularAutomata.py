import CellularAutomata2D
import CellularAutomata3D
import getopt
import sys
import os

def usage():
    print()
    print("Cellular Automata Usage")
    print("-h --help: Displays this help screen")
    print("------------------------------------")
    print("2D Essential Parameters")
    print("-l --length: The length of the string.")
    print("-n --num: Number of initial cells")
    print("-c --cell: Name of the cell class - must be a subclass of Cell")
    print("------------------------------------")
    print("3D Essential Parameters")
    print("-x --xlength: The x-length of the grid.")
    print("-y --ylength: The y-length of the grid.")
    print("-n --num: Number of initial cells")
    print("-c --cell: Name of the cell class - must be a subclass of Cell3D")
    print("------------------------------------")
    print("Optional Parameters")
    print("-d --delay: Delay between each iteration, for display purposes. Default 0.1s")
    print()

run3D = CellularAutomata3D.run


if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hl:n:c:d",
                                   ["help", "length", "num", "cell", "delay"])
    except getopt.GetoptError as err2d:
        try:
            opts, args = getopt.getopt(sys.argv[1:],"hx:y:n:c:d",
                                       ["help", "xlength", "ylength", "num", "cell", "delay"])
        except getopt.GetoptError as err3d:
            print(str(err3d))
            usage()
            sys.exit()

    is2D = False
    is3DA = False
    is3DB = False
    for o, a in opts:
        if o in ("-x","--xlength"):
            is3DA = True
        if o in ("-y","--ylength"):
            is3DB = True
        if o in ("-l","--length"):
            is2D = True

    if is2D and (is3DA or is3DB):
        usage()
        sys.exit()
    elif is2D:
        CellularAutomata2D.main()
    elif is3DA and is3DB:
        CellularAutomata3D.main()
    else:
        usage()
        sys.exit()
