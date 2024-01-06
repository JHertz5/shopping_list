from dataclasses import dataclass


@dataclass
class Item:
    '''
    A generic class for a item in a shopping list database.
    '''
    quantity: int = 0

    def incr_quantity(self):
        self.quantity += 1

    def reset_quantity(self):
        self.quantity = 0
