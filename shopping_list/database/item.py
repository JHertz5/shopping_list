from dataclasses import dataclass


@dataclass
class Item:
    '''
    A class for an item in a shopping list.
    '''
    quantity: int = 0
    group: str | int = 'none'

    def incr_quantity(self):
        self.quantity += 1

    def reset_quantity(self):
        self.quantity = 0
