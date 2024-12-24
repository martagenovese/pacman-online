from Ghost import Ghost

class RedGhost(Ghost):
    def __init__(self, characters_position, tiles, pacman, colour):
        super().__init__(characters_position, tiles, pacman, colour)
        self.x = 12
        self.y = 17
        self.status = 1
        self.n_ghost = 1
        self.characters_position.set_x(self.n_ghost, self.x)
        self.characters_position.set_y(self.n_ghost, self.y)

    def start_game(self):
        self.move(2)
        self.move(0)
        self.move(2)
        self.move(2)
        self.status = 1

    def scatter(self):
        if self.status != 1:
            self.turn_around()
            self.status = 1
        self.reach_target(25, 0)

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

        self.reach_target(self.x_target, self.y_target)

    def restore_position(self):
        if self.x != 12 or self.y != 17:
            self.event_manager.clear_ghost_position(self)
        self.x = 12
        self.y = 17
        self.characters_position.set_x(self.n_ghost, self.x)
        self.characters_position.set_y(self.n_ghost, self.y)
        self.event_manager.update_ghost_position(self)