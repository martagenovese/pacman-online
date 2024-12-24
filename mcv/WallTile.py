from Tile import Tile

class WallTile(Tile):
    def __init__(self):
        pass

    def is_wall(self):
        return True

    def is_pacman(self):
        return False

    def is_ghost(self):
        return False

    def is_dot(self):
        return False

    def is_super_food(self):
        return False

    def is_intersection(self):
        return False

    def is_tardis(self):
        return False