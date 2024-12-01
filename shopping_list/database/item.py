from dataclasses import dataclass


@dataclass
class Item:
    '''
    A class for an item in a shopping list.
    '''
    quantity: int = 0
    group: str | int = 'none'

    def incr_quantity(self, incr_num=1):
        self.quantity += incr_num

    def reset_quantity(self):
        self.quantity = 0
