from abc import ABC, abstractmethod

class Tile(ABC):
    @abstractmethod
    def is_wall(self):
        pass

    @abstractmethod
    def is_pacman(self):
        pass

    @abstractmethod
    def is_ghost(self):
        pass

    @abstractmethod
    def is_dot(self):
        pass

    @abstractmethod
    def is_super_food(self):
        pass

    @abstractmethod
    def is_tardis(self):
        pass

    def set_pacman(self, b):
        pass

    def set_intersection(self, b):
        pass

    def set_tardis(self, b):
        pass

    @abstractmethod
    def is_intersection(self):
        pass

    def set_fruit(self, b):
        pass

    def is_fruit(self):
        return False