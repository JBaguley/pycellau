import pycellau

class Spreader(pycellau.Cell2D):
    on = "O"
    off = "#"
    def update(self, model):
        counter = 0
        for i in range(3):
            if model.getTape()[(self.l-1+i)%model.l].s == self.on:
                counter += 1
        if self.s == self.off and counter > 0:
            self.s = self.on

seed = "####O##########"

pycellau.run2D(15, Spreader, seed)
