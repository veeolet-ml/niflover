import random

from snake_grid import GridEntity, SnakeGrid, CellType


def _count_food(grid: SnakeGrid) -> int:
    count = 0
    for row in range(grid.blocks_per_height):
        for col in range(grid.blocks_per_width):
            if grid.grid[row][col] == CellType.FOOD:
                count += 1
    return count


def _add_food(to_add: int, grid: SnakeGrid) -> int:
    coord_list = []
    for row in range(grid.blocks_per_height):
        for col in range(grid.blocks_per_width):
            if grid.grid[row][col] == CellType.NOTHING:
                coord_list.append((row, col))
    random.shuffle(coord_list)
    size = min(to_add, len(coord_list))
    for i in range(size):
        grid.set_food_cell(coord_list[i])
    return size


class FoodManager(GridEntity):

    def __init__(self, max_food_items: int):
        self.original_food_items = max_food_items
        self.max_food_items = max_food_items

    def update(self, grid: SnakeGrid) -> bool:
        food = _count_food(grid)
        if food < self.max_food_items:
            to_add = self.max_food_items - food
            added = _add_food(to_add, grid)

            # if grid is full lower max amount of food that can be placed
            # sanity check if
            if added < to_add:
                self.max_food_items = food + added
        return False