from dataclasses import dataclass, field
from typing import List


from .item import Item


@dataclass
class Recipe(Item):
    '''
    A class representing a recipe.
    '''
    ingredient_list: List[str] = field(default_factory=list)

    def ingredient_is_in_recipe(self, ingredient):
        return ingredient in self.ingredient_list
