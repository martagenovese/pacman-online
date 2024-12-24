from PIL import Image, ImageTk
import threading

class Pacman:
    def __init__(self, characters_position):
        self.pacman_images = [
            self.create_image("right.png"),
            self.create_image("left.png"),
            self.create_image("up.png"),
            self.create_image("down.png")
        ]
        self.super_pacman_images = [
            self.create_image("super/right.png"),
            self.create_image("super/left.png"),
            self.create_image("super/up.png"),
            self.create_image("super/down.png")
        ]
        self.image = None
        self.image_ref = None
        self.direction = 0
        self.characters_position = characters_position
        self.x = 13
        self.y = 26
        self.is_super = False
        self.event_manager = None
        self.lock = threading.Lock()

    def create_image(self, image_path):
        original_image = Image.open(f"mcv/images/pacman/{image_path}")
        scaled_image = original_image.resize((25, 23), Image.LANCZOS)
        self.image = ImageTk.PhotoImage(scaled_image)
        self.image_ref = scaled_image
        return ImageTk.PhotoImage(scaled_image)

    def set_event_manager(self, event_manager):
        self.event_manager = event_manager

    def set_direction(self, direction):
        with self.lock:
            if self.is_super:
                self.image = self.super_pacman_images[direction]
            else:
                self.image = self.pacman_images[direction]
            self.direction = direction

    def set_super(self, is_super):
        with self.lock:
            self.is_super = is_super
            if is_super:
                self.event_manager.mucho_macho_pacman()
                self.image = self.super_pacman_images[self.direction]

    def is_super(self):
        with self.lock:
            return self.is_super

    def get_direction(self):
        with self.lock:
            return self.direction

    def get_x(self):
        with self.lock:
            return self.x

    def get_y(self):
        with self.lock:
            return self.y

    def move(self, direction):
        self.set_direction(direction)
        with self.lock:
            if direction == 1:
                self.x = 27 if self.x == 0 else self.x - 1
            elif direction == 0:
                self.x = 0 if self.x == 27 else self.x + 1
            elif direction == 2:
                self.y -= 1
            elif direction == 3:
                self.y += 1
            self.characters_position.set_x(0, self.x)
            self.characters_position.set_y(0, self.y)

    def eaten(self):
        with self.lock:
            self.event_manager.get_table().clear_pacman(self.x, self.y)
            self.x = 13
            self.y = 26
            self.characters_position.set_x(0, self.x)
            self.characters_position.set_y(0, self.y)
            self.set_direction(0)
            self.event_manager.get_table().update_position()