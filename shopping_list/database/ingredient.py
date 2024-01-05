from dataclasses import dataclass

from .item import Item


@dataclass
class Ingredient(Item):
    '''
    A class representing an ingredient to be purchased from the shop.
    '''
    group: str | int = 'none'
