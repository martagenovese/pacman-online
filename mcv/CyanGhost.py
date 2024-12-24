from Ghost import Ghost
import time
from WallTile import WallTile

class CyanGhost(Ghost):
    def __init__(self, characters_position, tiles, pacman, colour):
        super().__init__(characters_position, tiles, pacman, colour)
        self.x = 13
        self.y = 17
        self.status = 1
        self.n_ghost = 2
        self.characters_position.set_x(self.n_ghost, self.x)
        self.characters_position.set_y(self.n_ghost, self.y)

    def chase(self):
        if self.status != 0:
            self.target_reached = True
            self.turn_around()
            self.status = 0

        if self.x == self.x_target and self.y == self.y_target:
            self.target_reached = True

        if self.target_reached:
            self.target_reached = False
            self.x_target = self.characters_position.get_x(0)
            self.y_target = self.characters_position.get_y(0)

            direction = self.pacman.get_direction()
            if direction == 3:
                for i in range(2, -1, -1):
                    if self.y_target - i >= 0:
                        self.y_target -= i
                        break
            elif direction == 1:
                for i in range(2, -1, -1):
                    if self.x_target - i >= 0:
                        self.x_target -= i
                        break
            elif direction == 4:
                for i in range(2, -1, -1):
                    if self.y_target + i <= 35:
                        self.y_target += i
                        break
            elif direction == 0:
                for i in range(2, -1, -1):
                    if self.x_target + i <= 27:
                        self.x_target += i
                        break

            for i in range(self.x_target - self.characters_position.get_x(1), -1, -1):
                if 0 <= self.x_target + (self.x_target - self.characters_position.get_x(1)) <= 27:
                    self.x_target += self.x_target - self.characters_position.get_x(1)
                    break

            for i in range(self.y_target - self.characters_position.get_y(1), -1, -1):
                if 0 <= self.y_target + (self.y_target - self.characters_position.get_y(1)) <= 35:
                    self.y_target += self.y_target - self.characters_position.get_y(1)
                    break

            for i in range(self.y_target - self.characters_position.get_y(0)):
                for j in range(self.x_target - self.characters_position.get_x(0)):
                    if not isinstance(self.tiles[self.y_target - i][self.x_target - j], WallTile):
                        self.x_target -= i
                        self.y_target -= j
                        break

        self.reach_target(self.x_target, self.y_target)

    def scatter(self):
        if self.status != 1:
            self.turn_around()
            self.status = 1
        self.reach_target(0, 35)

    def start_game(self):
        time.sleep(self.waiting_time * 4)
        self.move(2)
        self.move(2)
        self.move(2)
        self.status = 1

    def restore_position(self):
        if self.x != 13 or self.y != 17:
            self.event_manager.clear_ghost_position(self)
        self.x = 13
        self.y = 17
        self.characters_position.set_x(self.n_ghost, self.x)
        self.characters_position.set_y(self.n_ghost, self.y)
        self.event_manager.update_ghost_position(self)