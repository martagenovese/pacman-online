import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pygame
from Pacman import Pacman
from Ghost import Ghost

class Table:
    def __init__(self, root):
        self.root = root
        self.root.title("pacman")
        self.tiles = [[tk.Label(self.root, bg="black") for _ in range(28)] for _ in range(36)]
        for i in range(36):
            for j in range(28):
                self.tiles[i][j].grid(row=i, column=j, sticky="nsew", padx=0, pady=0)
        self.root.geometry(f"{224 * 3}x{288 * 3}")
        self.root.resizable(False, False)

        self.event_manager = None
        self.character = None
        self.red_ghost = None
        self.cyan_ghost = None
        self.pink_ghost = None
        self.orange_ghost = None

        self.scaled_image_dot = self.load_image("mcv/images/dot.png", 7, 7)
        self.scaled_image_sfood = self.load_image("mcv/images/dot.png", 18, 18)
        self.scaled_image_tardis = self.load_image("mcv/meme/Tardis.png", 18, 18)
        self.scaled_image_brick = self.load_image("mcv/meme/Brick.png", 18, 18)
        self.scaled_image_fruit = self.load_image("mcv/images/fruit.png", 16, 16)
        self.scaled_image_pacman = self.load_image("mcv/images/pacman/right.png", 17, 17)

        # Keep references to avoid garbage collection
        self.image_refs = {
            "dot": self.scaled_image_dot,
            "sfood": self.scaled_image_sfood,
            "tardis": self.scaled_image_tardis,
            "brick": self.scaled_image_brick,
            "fruit": self.scaled_image_fruit,
            "pacman": self.scaled_image_pacman
        }

        pygame.mixer.init()

    def load_image(self, path, width, height):
        image = Image.open(path)
        image = image.resize((width, height), Image.LANCZOS)
        photo_image = ImageTk.PhotoImage(image, master=self.root)
        return photo_image

    def set_event_manager(self, event_manager):
        self.event_manager = event_manager
        self.root.bind("<KeyPress>", self.event_manager.key_pressed)
        self.root.bind("<KeyRelease>", self.event_manager.key_released)

    def set_dot(self, y, x):
        self.tiles[y][x].config(image=self.image_refs["dot"])

    def set_super_food(self, y, x):
        self.tiles[y][x].config(image=self.image_refs["sfood"])

    def set_tardis(self, x, y):
        self.tiles[y][x].config(image=self.image_refs["tardis"])

    def set_brick(self, x, y):
        self.tiles[y][x].config(image=self.image_refs["brick"])

    def clear_pacman(self, x, y):
        self.tiles[y][x].config(image='')

    def set_character(self, character):
        self.character = character
        self.tiles[26][13].config(image=self.image_refs["pacman"])

    def set_red_ghost(self, red_ghost):
        self.red_ghost = red_ghost
        self.tiles[17][12].config(image=self.red_ghost.image)

    def set_cyan_ghost(self, cyan_ghost):
        self.cyan_ghost = cyan_ghost
        self.tiles[17][13].config(image=self.cyan_ghost.image)

    def set_pink_ghost(self, pink_ghost):
        self.pink_ghost = pink_ghost
        self.tiles[17][14].config(image=self.pink_ghost.image)

    def set_orange_ghost(self, orange_ghost):
        self.orange_ghost = orange_ghost
        self.tiles[17][15].config(image=self.orange_ghost.image)

    def set_score_bar(self):
        score = "SCORE"
        x_tile = 9
        for char in score:
            self.tiles[1][x_tile].config(fg="white", font=("Arial", 25, "bold"), text=char)
            x_tile += 1
        self.tiles[1][18].config(fg="white", font=("Arial", 25, "bold"), text="0")

    def set_lives(self):
        self.tiles[35][2].config(image=self.image_refs["pacman"])
        self.tiles[35][4].config(image=self.image_refs["pacman"])
        self.tiles[35][6].config(image=self.image_refs["pacman"])

    def set_fruit(self):
        self.tiles[35][25].config(image=self.image_refs["fruit"])
        self.tiles[35][23].config(image=self.image_refs["fruit"])

    def set_fruit_in_table(self, x, y):
        if x == 9:
            self.tiles[35][23].config(image='')
        else:
            self.tiles[35][25].config(image='')
        self.tiles[y][x].config(image=self.image_refs["fruit"])

    def play_sound(self, sound_file_name):
        try:
            pygame.mixer.music.load(sound_file_name)
            pygame.mixer.music.play()
        except pygame.error as e:
            print(f"Error playing sound: {e}")

    def end_game(self, message, text, image_path):
        resized_image = self.load_image(image_path, 500, 500)
        label = tk.Label(self.root, text=text, image=resized_image, compound="bottom", font=("Arial", 20, "bold"), fg="black")
        label.image = resized_image  # Keep a reference to avoid garbage collection

        dialog = tk.Toplevel(self.root)
        dialog.title(message)
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.geometry("600x600")
        dialog.resizable(False, False)

        label.pack(expand=True, fill="both")
        self.play_sound(f"meme/audio/{message}.wav")

        self.root.after(3500 if message == "Victory" else 8100, dialog.destroy)
        dialog.wait_window()
        self.root.quit()

    def update_position(self):
        self.tiles[self.character.get_y()][self.character.get_x()].config(image=self.image_refs["pacman"])

    def clear_ghost(self, x, y, is_dot, is_super_food, is_fruit, is_tardis):
        if not is_dot and not is_super_food and not is_fruit and not is_tardis:
            self.tiles[y][x].config(image='')
        elif is_super_food:
            self.set_super_food(y, x)
        elif is_fruit:
            self.set_fruit_in_table(x, y)
        elif is_tardis:
            self.set_tardis(x, y)
        else:
            self.set_dot(y, x)

    def update_ghost(self, ghost):
        self.tiles[ghost.get_y()][ghost.get_x()].config(image=ghost.image)

    def update_score(self, score):
        score_string = str(score)
        x_tile = 18
        for char in reversed(score_string):
            self.tiles[1][x_tile].config(fg="white", font=("Arial", 25, "bold"), text=char)
            x_tile -= 1

    def clear_tile(self, x, y):
        self.tiles[y][x].config(image='')