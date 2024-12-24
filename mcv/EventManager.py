import threading
import time
from Ghost import Ghost
from WallTile import WallTile
from CrossableTile import CrossableTile
import random

class EventManager:
    def __init__(self):
        self.is_listener_active = True
        self.start_ghost = 0
        self.characters_position = None
        self.table = None
        self.model = None

    def set_start_ghost(self, n):
        self.start_ghost = n

    def set_model(self, model):
        self.model = model
        model.get_red_ghost().set_event_manager(self)
        model.get_cyan_ghost().set_event_manager(self)
        model.get_pink_ghost().set_event_manager(self)
        model.get_orange_ghost().set_event_manager(self)
        model.pacman.set_event_manager(self)
        self.characters_position = model.characters_position
        model.supervisor.set_event_manager(self)

    def set_table(self, table):
        self.table = table
        for i in range(36):
            for j in range(28):
                if isinstance(self.model.tiles[i][j], WallTile):
                    if i < 3 or (12 < i < 16 or 18 < i < 22) and (j < 5 or j > 22) or i > 33 or (i == 15 and (j == 13 or j == 14)) or (16 <= i <= 18 and 11 <= j <= 16):
                        table.tiles[i][j].config(bg="black")
                    else:
                        table.set_brick(j, i)
                elif isinstance(self.model.tiles[i][j], CrossableTile):
                    tile = self.model.tiles[i][j]
                    if tile.is_dot:
                        table.set_dot(i, j)
                    elif tile.is_super_food:
                        table.set_super_food(i, j)
                    elif tile.is_tardis:
                        table.set_tardis(j, i)
                    table.tiles[i][j].config(bg="black")
        table.set_score_bar()
        table.set_lives()
        table.set_fruit()
        table.set_character(self.model.get_pacman())
        table.set_red_ghost(self.model.get_red_ghost())
        table.set_cyan_ghost(self.model.get_cyan_ghost())
        table.set_pink_ghost(self.model.get_pink_ghost())
        table.set_orange_ghost(self.model.get_orange_ghost())

    def get_table(self):
        return self.table

    def disable_listener_for(self, milliseconds):
        self.is_listener_active = False
        threading.Timer(milliseconds / 1000, self.enable_listener).start()

    def enable_listener(self):
        self.is_listener_active = True

    def clear_ghost_position(self, ghost):
        is_dot = self.model.tiles[ghost.get_y()][ghost.get_x()].is_dot()
        is_super_food = self.model.tiles[ghost.get_y()][ghost.get_x()].is_super_food()
        is_fruit = self.model.tiles[ghost.get_y()][ghost.get_x()].is_fruit()
        is_tardis = self.model.tiles[ghost.get_y()][ghost.get_x()].is_tardis()
        self.table.clear_ghost(ghost.get_x(), ghost.get_y(), is_dot, is_super_food, is_fruit, is_tardis)

    def update_ghost_position(self, ghost):
        self.table.update_ghost(ghost)

    def mucho_macho_pacman(self):
        self.table.update_position()
        self.table.clear_pacman(self.model.get_pacman().get_x(), self.model.get_pacman().get_y())
        self.model.get_red_ghost().set_scared(True)
        self.model.get_cyan_ghost().set_scared(True)
        self.model.get_pink_ghost().set_scared(True)
        self.model.get_orange_ghost().set_scared(True)
        self.model.ghosts_eaten = 0
        threading.Timer(7, self.reset_pacman_and_ghosts).start()

    def reset_pacman_and_ghosts(self):
        self.model.pacman.set_super(False)
        self.model.get_red_ghost().set_scared(False)
        self.model.get_cyan_ghost().set_scared(False)
        self.model.get_pink_ghost().set_scared(False)
        self.model.get_orange_ghost().set_scared(False)

    def stop_game(self, victory):
        self.characters_position.set_x(0, 0)
        self.characters_position.set_y(0, 0)
        if victory:
            self.table.end_game("Victory!", "<html>Hai vinto!<br>Adesso puoi rubare questo gatto</html>", "src/meme/vittoria.jpg")
        else:
            self.table.end_game("Defeat!", "<html>Hai perso.<br>Ora il tipo del quadro di vienna è sotto al tuo letto</html>", "src/meme/sconfitta.jpg")

    def key_typed(self, e):
        pass

    def key_pressed(self, e):
        if self.is_listener_active:
            self.disable_listener_for(150)
            key = e.keycode
            if key == 65:
                d = 1
            elif key == 68:
                d = 0
            elif key == 87:
                d = 2
            elif key == 83:
                d = 3
            else:
                return

            if self.start_ghost == 0:
                self.table.play_sound("mcv/meme/audio/musichetta.wav")
                self.model.start_red_ghost()
                self.model.start_cyan_ghost()
                self.model.start_pink_ghost()
                self.model.start_orange_ghost()
                self.model.start_supervisors()
                self.start_ghost = 1
            elif self.start_ghost == 2:
                self.model.r.set_status(5)
                self.model.c.set_status(5)
                self.model.p.set_status(5)
                self.model.o.set_status(5)
                self.start_ghost = 1

            fruit = self.model.get_fruit()
            pacman_status1 = self.model.get_pacman().is_super
            dot_eaten = self.model.dots_counter
            self.table.clear_pacman(self.model.get_pacman().get_x(), self.model.get_pacman().get_y())
            if self.model.get_pacman().get_x() == 0:
                self.table.play_sound("mcv/meme/audio/Tardis.wav")
                self.model.set_tardis(0, 17)
                self.table.set_tardis(0, 17)
            elif self.model.get_pacman().get_x() == 27:
                self.table.play_sound("mcv/meme/audio/Tardis.wav")
                self.model.set_tardis(27, 17)
                self.table.set_tardis(27, 17)
            try:
                self.model.keep_direction(d)
            except Exception as ex:
                raise RuntimeError(ex)
            pacman_status2 = self.model.get_pacman().is_super
            if not pacman_status1 and pacman_status2:
                self.table.play_sound("mcv/meme/audio/cibo.wav")
            fruit_after = self.model.get_fruit()
            if fruit != fruit_after:
                if fruit_after == 0:
                    self.model.set_fruit(9, 17)
                    self.table.set_fruit_in_table(9, 17)
                else:
                    self.model.set_fruit(18, 17)
                    self.table.set_fruit_in_table(18, 17)
            if self.model.is_fruit_eaten:
                self.table.play_sound("mcv/meme/audio/crocchi.wav")
            if dot_eaten != self.model.dots_counter and random.random() > 0.95:
                self.table.play_sound(f"mcv/meme/audio/bubii/{random.randint(1, 7)}.wav")
            self.table.update_score(self.model.get_score())
            self.model.update_position()
            self.table.update_position()
            if self.model.dots_counter < 0 and self.model.fruit == 0:
                self.stop_game(True)

    def key_released(self, e):
        pass