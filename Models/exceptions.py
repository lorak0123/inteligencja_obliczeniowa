from Models.demand import Demand


class NoMoreClientsException(Exception):
    pass


class NotEnoughGoodsException(Exception):
    def __init__(self, missing: Demand):
        self.missing = missing
