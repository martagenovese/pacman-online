from Tile import Tile

class CrossableTile(Tile):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_pacman = False
        self.is_ghost = False
        self.is_dot = False
        self.is_super_food = False
        self.is_intersection = False
        self.is_fruit = False
        self.is_tardis = False

    def set_pacman(self, is_pacman):
        self.is_pacman = is_pacman

    def set_intersection(self, is_intersection):
        self.is_intersection = is_intersection

    def set_ghost(self, is_ghost):
        self.is_ghost = is_ghost

    def set_dot(self, is_dot):
        self.is_dot = is_dot

    def set_super_food(self, is_super_food):
        self.is_super_food = is_super_food

    def set_tardis(self, is_tardis):
        self.is_tardis = is_tardis

    def is_wall(self):
        return False

    def is_pacman(self):
        return self.is_pacman

    def is_ghost(self):
        return self.is_ghost

    def is_dot(self):
        return self.is_dot

    def is_super_food(self):
        return self.is_super_food

    def is_intersection(self):
        return self.is_intersection

    def is_tardis(self):
        return self.is_tardis

    def is_fruit(self):
        return self.is_fruit

    def set_fruit(self, is_fruit):
        self.is_fruit = is_fruit