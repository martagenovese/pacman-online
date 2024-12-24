from PIL import Image, ImageTk
import threading
import time
import random
from WallTile import WallTile

class Ghost(threading.Thread):
    def __init__(self, characters_position, tiles, pacman, colour):
        super().__init__()
        self.characters_position = characters_position
        self.tiles = tiles
        self.pacman = pacman
        self.colour = colour
        self.normal = self.create_image(f"mcv/images/ghosts/{self.switch_color()}.png")
        self.image = self.normal
        self.scared = self.create_image("mcv/images/ghosts/scared.png")
        self.target_reached = True
        self.x_target = 0
        self.y_target = 0
        self.waiting_time = 0.4
        self.x = 0
        self.y = 0
        self.direction = ""
        self.direction_int = 0
        self.status = 0
        self.n_ghost = 0
        self.event_manager = None
        self.lock = threading.Lock()

    def create_image(self, image_path):
        original_image = Image.open(image_path)
        scaled_image = original_image.resize((18, 16), Image.LANCZOS)
        return ImageTk.PhotoImage(scaled_image)

    def switch_color(self):
        return {1: "red", 2: "cyan", 3: "pink", 4: "orange"}.get(self.colour, "scared")

    def set_event_manager(self, event_manager):
        self.event_manager = event_manager

    def set_scared(self, is_scared):
        with self.lock:
            if is_scared:
                self.image = self.scared
                self.status = 2
            else:
                self.image = self.normal
                self.status = 0

    def set_status(self, n):
        with self.lock:
            self.status = n

    def get_status(self):
        with self.lock:
            return self.status

    def get_x(self):
        with self.lock:
            return self.x

    def get_y(self):
        with self.lock:
            return self.y

    def move(self, dir):
        with self.lock:
            self.event_manager.clear_ghost_position(self)
            self.direction_int = dir
            if dir == 1:
                self.x = 27 if self.x == 0 else self.x - 1
            elif dir == 0:
                self.x = 0 if self.x == 27 else self.x + 1
            elif dir == 2:
                self.y -= 1
            elif dir == 3:
                self.y += 1
            self.characters_position.set_x(self.n_ghost, self.x)
            self.characters_position.set_y(self.n_ghost, self.y)
            self.event_manager.update_ghost_position(self)
            time.sleep(self.waiting_time)

    def reach_target(self, x_target, y_target):
        directions = [[self.y - 1, self.x], [self.y, self.x - 1], [self.y + 1, self.x], [self.y, self.x + 1]]
        if directions[1][1] == -1:
            directions[1][1] = 27
        if directions[3][1] == 28:
            directions[3][1] = 0
        distance_min = float('inf')
        chosen_direction = self.direction_int
        back = (self.direction_int + 2) % 4

        if self.tiles[self.y][self.x].is_intersection() or isinstance(self.tiles[directions[chosen_direction][0]][directions[chosen_direction][1]], WallTile):
            for i, (dy, dx) in enumerate(directions):
                if not isinstance(self.tiles[dy][dx], WallTile) and i != back:
                    distance = ((y_target - dy) ** 2 + (x_target - dx) ** 2) ** 0.5
                    if distance < distance_min:
                        distance_min = distance
                        chosen_direction = i

        self.move(chosen_direction)

    def frightened(self):
        with self.lock:
            if self.status != 2:
                self.target_reached = True
                self.turn_around()
                self.status = 2

            if self.x == self.x_target and self.y == self.y_target:
                self.target_reached = True

            if self.target_reached:
                while True:
                    self.x_target = random.randint(1, 26)
                    self.y_target = random.randint(4, 29)
                    if not isinstance(self.tiles[self.y_target][self.x_target], WallTile):
                        break

            self.reach_target(self.x_target, self.y_target)

    def eaten(self):
        with self.lock:
            self.restore_position()
            if not self.pacman.is_super():
                self.start_game()

    def turn_around(self):
        with self.lock:
            if self.direction_int == 2 and not isinstance(self.tiles[self.y - 1][self.x], WallTile):
                self.move(3)
            elif self.direction_int == 1 and not isinstance(self.tiles[self.y][self.x - 1], WallTile):
                self.move(0)
            elif self.direction_int == 3 and not isinstance(self.tiles[self.y + 1][self.x], WallTile):
                self.move(2)
            elif self.direction_int == 0 and not isinstance(self.tiles[self.y][self.x + 1], WallTile):
                self.move(1)

    def pacman_eaten(self):
        with self.lock:
            self.restore_position()
            self.status = 4
            self.event_manager.update_ghost_position(self)
            self.event_manager.clear_ghost_position(self)

    def run(self):
        self.start_game()
        while True:
            with self.lock:
                if self.status == 0:
                    self.chase()
                elif self.status == 1:
                    self.scatter()
                elif self.status == 2:
                    self.frightened()
                elif self.status == 3:
                    self.eaten()
                elif self.status == 4:
                    self.restore_position()
                elif self.status == 5:
                    self.start_game()

    def start_game(self):
        raise NotImplementedError

    def chase(self):
        raise NotImplementedError

    def scatter(self):
        raise NotImplementedError

    def restore_position(self):
        raise NotImplementedError