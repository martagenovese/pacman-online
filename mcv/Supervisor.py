import threading
import time

class Supervisor(threading.Thread):
    def __init__(self, characters_position, model):
        super().__init__()
        self.characters_position = characters_position
        self.model = model
        self.ghosts_eaten = 0
        self.event_manager = None

    def set_event_manager(self, event_manager):
        self.event_manager = event_manager

    def n_ghosts_eaten(self):
        g = 1
        n = 0
        for i in range(12, 16):
            if self.characters_position.get_y(g) == 17 and self.characters_position.get_x(g) == i:
                n += 1
            g += 1
        return n

    def run(self):
        n_ghosts_before = self.n_ghosts_eaten()
        while True:
            n = self.model.collision()
            if n >= 0:
                try:
                    is_pacman_alive = self.model.collision_procedure(n)
                    if not is_pacman_alive:
                        self.event_manager.set_start_ghost(2)
                        self.model.lives -= 1
                        if self.model.lives == 2:
                            self.event_manager.get_table().clear_tile(6, 35)
                        elif self.model.lives == 1:
                            self.event_manager.get_table().clear_tile(4, 35)
                        elif self.model.lives == 0:
                            self.event_manager.get_table().clear_tile(2, 35)
                        if self.model.lives < 0:
                            print("Game Over")
                            self.event_manager.stop_game(False)
                        else:
                            self.event_manager.get_table().play_sound("meme/audio/morte.wav")
                    else:
                        self.event_manager.get_table().play_sound("meme/audio/urlo.wav")
                        self.event_manager.get_table().clear_pacman(self.model.get_pacman().get_x(), self.model.get_pacman().get_y())
                        self.event_manager.get_table().update_position()
                        self.ghosts_eaten = self.n_ghosts_eaten()
                        if self.ghosts_eaten != 0 and self.ghosts_eaten != n_ghosts_before:
                            self.model.score += 100 * (2 ** self.ghosts_eaten)
                            n_ghosts_before = self.ghosts_eaten
                except Exception as ex:
                    raise RuntimeError(ex)