class Demand:
    def __init__(self, uranium: int, tuna: int, orange: int):
        self.uranium = uranium
        self.tuna = tuna
        self.orange = orange

    def __str__(self):
        return "{},{},{}".format(self.uranium,self.tuna,self.orange)