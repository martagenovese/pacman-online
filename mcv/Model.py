import threading
import random
from Pacman import Pacman
from RedGhost import RedGhost
from PinkGhost import PinkGhost
from CyanGhost import CyanGhost
from OrangeGhost import OrangeGhost
from My2DSyncArray import My2DSyncArray
from CrossableTile import CrossableTile
from WallTile import WallTile
from Supervisor import Supervisor
from GhostSupervisor import GhostSupervisor

class Model:
    def __init__(self):
        self.characters_position = My2DSyncArray(5)
        self.pacman = Pacman(self.characters_position)
        self.tiles = [[CrossableTile(i, j) for j in range(28)] for i in range(36)]
        self.supervisor = Supervisor(self.characters_position, self)
        self.s_thread = threading.Thread(target=self.supervisor.run)
        self.ghosts_eaten = 0

        self.arrange_walls()
        self.arrange_intersections()
        self.arrange_dots()
        self.tiles[26][13].set_pacman(True)
        self.set_tardis(0, 17)
        self.set_tardis(27, 17)

        self.score = 0
        self.lives = 3
        self.dots_counter = 0
        self.fruit = 2
        self.r = RedGhost(self.characters_position, self.tiles, self.pacman, 1)
        self.c = CyanGhost(self.characters_position, self.tiles, self.pacman, 2)
        self.p = PinkGhost(self.characters_position, self.tiles, self.pacman, 3)
        self.o = OrangeGhost(self.characters_position, self.tiles, self.pacman, 4)

        self.r_thread = threading.Thread(target=self.r.run)
        self.p_thread = threading.Thread(target=self.p.run)
        self.c_thread = threading.Thread(target=self.c.run)
        self.o_thread = threading.Thread(target=self.o.run)

        self.ghost_supervisor = GhostSupervisor(self.r, self.c, self.p, self.o)
        self.g_thread = threading.Thread(target=self.ghost_supervisor.run)

        self.is_fruit_eaten = False
        self.last_direction = 0

    def arrange_walls(self):
        try:
            with open("mcv\construction\walls.csv", "r") as f:
                for line in f:
                    i, j = map(int, line.strip().split(";"))
                    self.tiles[i][j] = WallTile()
        except FileNotFoundError as e:
            raise RuntimeError(e)

        for i in range(36):
            for j in range(28):
                if i == 3:
                    i = 13
                elif ((12 < i < 16) or (18 < i < 22)) and j == 5:
                    j = 23
                elif i == 22:
                    i = 34
                if i < 3 or ((12 < i < 16) or (18 < i < 22)) and (j < 5 or j > 22) or i > 33 or (16 <= i <= 18 and 11 <= j <= 16):
                    self.tiles[i][j] = WallTile()
        self.tiles[15][13] = WallTile()
        self.tiles[15][14] = WallTile()

    def arrange_intersections(self):
        try:
            with open("mcv/construction/intersections.csv", "r") as f:
                for line in f:
                    i, j = map(int, line.strip().split(";"))
                    self.tiles[i][j].set_intersection(True)
        except FileNotFoundError as e:
            raise RuntimeError(e)

    def arrange_dots(self):
        try:
            with open("mcv/construction/dots.csv", "r") as f:
                for line in f:
                    i, j = map(int, line.strip().split(";"))
                    if (i == 6 and j == 1) or (i == 6 and j == 26) or (i == 26 and j == 1) or (i == 26 and j == 26):
                        self.tiles[i][j] = CrossableTile(i, j)
                        self.tiles[i][j].set_super_food(True)
                    else:
                        self.tiles[i][j].set_dot(True)
        except FileNotFoundError as e:
            raise RuntimeError(e)

    def set_fruit(self, x, y):
        self.tiles[y][x].set_fruit(True)

    def set_tardis(self, x, y):
        self.tiles[y][x].set_tardis(True)

    def get_pacman(self):
        return self.pacman

    def get_left_tile(self):
        try:
            self.left_tile = self.tiles[self.pacman.get_y()][self.pacman.get_x() - 1]
        except IndexError:
            self.left_tile = self.tiles[self.pacman.get_y()][27]
        return self.left_tile

    def get_right_tile(self):
        try:
            self.right_tile = self.tiles[self.pacman.get_y()][self.pacman.get_x() + 1]
        except IndexError:
            self.right_tile = self.tiles[self.pacman.get_y()][0]
        return self.right_tile

    def get_up_tile(self):
        self.up_tile = self.tiles[self.pacman.get_y() - 1][self.pacman.get_x()]
        return self.up_tile

    def get_down_tile(self):
        self.down_tile = self.tiles[self.pacman.get_y() + 1][self.pacman.get_x()]
        return self.down_tile

    def get_my_tile(self):
        self.my_tile = self.tiles[self.pacman.get_y()][self.pacman.get_x()]
        return self.my_tile

    def get_red_ghost(self):
        return self.r

    def get_pink_ghost(self):
        return self.p

    def get_cyan_ghost(self):
        return self.c

    def get_orange_ghost(self):
        return self.o

    def get_score(self):
        return self.score

    def get_fruit(self):
        return self.fruit

    def update_position(self):
        self.characters_position.set_x(0, self.pacman.get_x())
        self.characters_position.set_y(0, self.pacman.get_y())

    def move_pacman(self, direction, tile, my_tile):
        self.is_fruit_eaten = False
        if tile is None:
            return
        if not isinstance(tile, WallTile):
            if self.dots_counter in [70, 240] and self.fruit > 0:
                self.fruit -= 1
            if tile.is_super_food:
                tile.set_super_food(False)
                self.pacman.set_super(True)
                self.score += 50
            elif tile.is_dot:
                tile.set_dot(False)
                self.score += 10
                self.dots_counter += 1
            elif tile.is_fruit:
                tile.set_fruit(False)
                self.is_fruit_eaten = True
                self.score += 100
            if self.fruit == 0 and self.dots_counter == 240:
                self.dots_counter = -1
            my_tile.set_pacman(False)
            self.pacman.move(direction)
            tile.set_pacman(True)

    def pacman_has_been_eaten(self):
        self.pacman.eaten()
        self.r.pacman_eaten()
        self.c.pacman_eaten()
        self.p.pacman_eaten()
        self.o.pacman_eaten()

    def collision(self):
        for i in range(1, 5):
            if self.characters_position.get_x(i) == self.characters_position.get_x(0) and self.characters_position.get_y(i) == self.characters_position.get_y(0):
                return i
        return -1

    def collision_procedure(self, n):
        if self.pacman.is_super():
            if n == 1:
                self.r.set_status(3)
            elif n == 2:
                self.c.set_status(3)
            elif n == 3:
                self.p.set_status(3)
            elif n == 4:
                self.o.set_status(3)
            return True
        else:
            self.tiles[23][14].set_pacman(True)
            self.pacman_has_been_eaten()
            return False

    def is_next_tile_wall(self, direction):
        if direction == 1:
            return isinstance(self.get_left_tile(), WallTile)
        elif direction == 0:
            return isinstance(self.get_right_tile(), WallTile)
        elif direction == 2:
            return isinstance(self.get_up_tile(), WallTile)
        elif direction == 3:
            return isinstance(self.get_down_tile(), WallTile)
        return False

    def keep_direction(self, direction):
        if self.is_next_tile_wall(direction):
            direction = self.last_direction
        if direction == 1:
            self.last_direction = 1
            self.move_pacman(1, self.get_left_tile(), self.get_my_tile())
        elif direction == 0:
            self.last_direction = 0
            self.move_pacman(0, self.get_right_tile(), self.get_my_tile())
        elif direction == 2:
            self.last_direction = 2
            self.move_pacman(2, self.get_up_tile(), self.get_my_tile())
        elif direction == 3:
            self.last_direction = 3
            self.move_pacman(3, self.get_down_tile(), self.get_my_tile())

    def start_red_ghost(self):
        self.r_thread.start()

    def start_cyan_ghost(self):
        self.c_thread.start()

    def start_pink_ghost(self):
        self.p_thread.start()

    def start_orange_ghost(self):
        self.o_thread.start()

    def start_supervisors(self):
        self.g_thread.start()
        self.s_thread.start()