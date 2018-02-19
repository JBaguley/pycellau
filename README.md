# pycellau
A python cellular automata simulator with console output

## Using as a module
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
CellularAutomata3D.run(10,10,CellularAutomata3D.GoLCell,seed,1)
