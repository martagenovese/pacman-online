from Ghost import Ghost
import time
from WallTile import WallTile

class PinkGhost(Ghost):
    def __init__(self, characters_position, tiles, pacman, colour):
        super().__init__(characters_position, tiles, pacman, colour)
        self.x = 14
        self.y = 17
        self.status = 1
        self.n_ghost = 3
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
            if direction == 2:
                for i in range(4, -1, -1):
                    if self.y_target - i >= 0 and not isinstance(self.tiles[self.y_target - i][self.x_target], WallTile):
                        self.y_target -= i
                        break
            elif direction == 1:
                for i in range(4, -1, -1):
                    if self.x_target - i >= 0 and not isinstance(self.tiles[self.y_target][self.x_target - i], WallTile):
                        self.x_target -= i
                        break
            elif direction == 3:
                for i in range(4, -1, -1):
                    if self.y_target + i <= 35 and not isinstance(self.tiles[self.y_target + i][self.x_target], WallTile):
                        self.y_target += i
                        break
            elif direction == 0:
                for i in range(4, -1, -1):
                    if self.x_target + i <= 27 and not isinstance(self.tiles[self.y_target][self.x_target + i], WallTile):
                        self.x_target += i
                        break

        self.reach_target(self.x_target, self.y_target)

    def scatter(self):
        if self.status != 1:
            self.turn_around()
            self.status = 1
        self.reach_target(1, 0)

    def start_game(self):
        time.sleep(self.waiting_time * 7)
        self.move(2)
        self.move(2)
        self.move(2)
        self.status = 1

    def restore_position(self):
        if self.x != 14 or self.y != 17:
            self.event_manager.clear_ghost_position(self)
        self.x = 14
        self.y = 17
        self.characters_position.set_x(self.n_ghost, self.x)
        self.characters_position.set_y(self.n_ghost, self.y)
        self.event_manager.update_ghost_position(self)