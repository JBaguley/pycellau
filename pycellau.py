import pycellau2d
import pycellau3d
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

Cell2D = pycellau2d.Cell
Cell3D = pycellau3d.Cell
run2D = pycellau2d.run
run3D = pycellau3d.run

"""
seed = ["-","O","-","O","-","O","-","O","O","O","O","-","-","O","-","O","-","O"]
run2D(len(seed), pycellau2d.TrafficCell, seed)
seed = [
    ["#","#","#","#","#","#","#","#","#","#"],
    ["#","#","#","#","#","#","#","#","#","#"],
    ["#","#","#","#","#","#","#","#","#","#"],
    ["#","#","#","#","O","#","#","#","#","#"],
    ["#","#","#","#","O","#","#","#","#","#"],
    ["#","#","#","#","O","#","#","#","#","#"],
    ["#","#","#","#","#","#","#","#","#","#"],
    ["#","#","#","#","#","#","#","#","#","#"],
    ["#","#","#","#","#","#","#","#","#","#"],
    ["#","#","#","#","#","#","#","#","#","#"],
]
run3D(10,10,pycellau3d.GoLCell,seed,1)
"""
if __name__ == "__main__":
    ins = ["-h","-l","-c","-n","-d"]
    insWord = ["--help", "--length", "--cell", "--num", "--delay"]
    opts = []
    used = []
    try:
        for i in range(0,len(sys.argv[1:]),2):
            if (sys.argv[1+i] in ins or sys.argv[1+i] in insWord) and sys.argv[1+i] not in used:
                opts.append([sys.argv[1+i],sys.argv[2+i]])
                used.append(sys.argv[1+i])
            else:

                ins = ["-h","-x","-y","-c","-n","-d"]
                insWord = ["--help", "--xlength", "--ylength", "--cell", "--num", "--delay"]
                opts = []
                used = []
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
        pycellau2d.main()
    elif is3DA and is3DB:
        pycellau3d.main()
    else:
        usage()
        sys.exit()
