class Entity:
    def __init__(self):
        pass


class Node:
    def __init__(self, x, y):
        self.position = (x, y)
        self.items = []

    def add_item(self, item):
        self.items.append(item)


class Item:
    def __init__(self, profit, weight):
        self.profit = profit
        self.weight = weight
