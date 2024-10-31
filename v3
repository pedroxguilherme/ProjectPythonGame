import tkinter as tk
import random
from tkinter import messagebox
import pygame
import numpy as np

pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

def generate_tone(frequency, duration=0.5, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = 32767 * np.sin(2 * np.pi * frequency * t)
    wave = wave.astype(np.int16)
    stereo_wave = np.zeros((wave.size, 2), dtype=np.int16)
    stereo_wave[:, 0] = wave
    stereo_wave[:, 1] = wave
    sound = pygame.sndarray.make_sound(stereo_wave)
    return sound

SOUNDS = {
    'red': generate_tone(440),
    'green': generate_tone(550),
    'blue': generate_tone(660),
    'yellow': generate_tone(770)
}

COLORS = ['red', 'green', 'blue', 'yellow']
GAME_SPEED = 1000
LEVEL_INCREMENT = 100
MAX_SPEED = 300
current_sequence = []
user_sequence = []
scores = {1: 0, 2: 0}
lives = {1: 3, 2: 3}

class BrilliantMelody:
    def __init__(self, root):
        self.root = root
        self.root.title("Brilliant Melody")
        self.root.geometry("800x600")
        self.root.configure(bg="#2e2e2e")

        self.is_player_turn = False
        self.level = 1
        self.game_speed = GAME_SPEED
        self.single_player = True
        self.player_turn = 1
        self.buttons = {}
        self.create_menu_screen()
        
    def create_menu_screen(self):
        self.menu_frame = tk.Frame(self.root, bg="#2e2e2e")
        self.menu_frame.place(relwidth=1, relheight=1)

        tk.Label(self.menu_frame, text="Brilliant Melody", font=('Helvetica', 36), bg="#2e2e2e", fg="white").pack(pady=80)
        
        single_btn = tk.Button(self.menu_frame, text="Single Player", command=lambda: self.start_game(True), font=('Helvetica', 16), width=15, bg="#1f6f8b", fg="white")
        single_btn.pack(pady=10)

        multi_btn = tk.Button(self.menu_frame, text="Multiplayer", command=lambda: self.start_game(False), font=('Helvetica', 16), width=15, bg="#1f6f8b", fg="white")
        multi_btn.pack(pady=10)

        exit_btn = tk.Button(self.menu_frame, text="Sair", command=self.root.quit, font=('Helvetica', 16), width=15, bg="#1f6f8b", fg="white")
        exit_btn.pack(pady=10)

    def start_game(self, single_player):
        self.single_player = single_player
        self.menu_frame.destroy()
        self.setup_game_screen()

    def setup_game_screen(self):
        self.create_scoreboard()
        self.create_buttons()
        self.reset_game()
        self.next_round()

    def create_buttons(self):
        button_frame = tk.Frame(self.root, bg="#2e2e2e")
        button_frame.pack(pady=20)

        button_width = 15
        button_height = 8
        for i, color in enumerate(COLORS):
            button = tk.Button(button_frame, bg=color, width=button_width, height=button_height,
                               command=lambda c=color: self.handle_click(c), activebackground=color, relief="flat")
            button.grid(row=0 if i < 2 else 1, column=i % 2, padx=10, pady=10, ipadx=10, ipady=10)
            self.buttons[color] = button

    def create_scoreboard(self):
        score_frame = tk.Frame(self.root, bg="#2e2e2e")
        score_frame.pack(side=tk.TOP, fill=tk.X, pady=10)

        # Placar para Single Player
        if self.single_player:
            self.score_label1 = tk.Label(score_frame, text="Pontos: 0", font=('Helvetica', 14), bg="#2e2e2e", fg="white")
            self.score_label1.pack(side=tk.LEFT, padx=20)

            self.status_label = tk.Label(self.root, text="Vidas: 3", font=('Helvetica', 12), bg="#2e2e2e", fg="white")
            self.status_label.pack(pady=5)

        # Placar para Multiplayer com destaque no jogador ativo
        else:
            self.score_label1 = tk.Label(score_frame, text="Jogador 1: 0", font=('Helvetica', 14), bg="#2e2e2e", fg="white")
            self.score_label1.pack(side=tk.LEFT, padx=20)

            self.score_label2 = tk.Label(score_frame, text="Jogador 2: 0", font=('Helvetica', 14), bg="#2e2e2e", fg="white")
            self.score_label2.pack(side=tk.RIGHT, padx=20)

            self.status_label = tk.Label(self.root, text="Vidas - Jogador 1: 3 | Jogador 2: 3", font=('Helvetica', 12), bg="#2e2e2e", fg="white")
            self.status_label.pack(pady=5)

    def next_round(self):
        self.is_player_turn = False
        user_sequence.clear()
        self.add_to_sequence()
        self.show_sequence(0)

    def reset_game(self):
        global current_sequence, scores, lives
        current_sequence = []
        scores = {1: 0, 2: 0}
        lives = {1: 3, 2: 3}
        self.update_score_labels()
        self.level = 1
        self.game_speed = GAME_SPEED
        self.player_turn = 1

    def add_to_sequence(self):
        current_sequence.append(random.choice(COLORS))
        
    def show_sequence(self, index):
        if index < len(current_sequence):
            color = current_sequence[index]
            self.buttons[color].config(bg="white")
            self.play_sound(color)
            self.root.after(500, lambda: self.hide_button(color, index))
        else:
            self.is_player_turn = True
            self.status_label.config(text="Sua vez!" if self.single_player else f"Turno do Jogador {self.player_turn}")

    def hide_button(self, color, index):
        self.buttons[color].config(bg=color)
        self.root.after(500, lambda: self.show_sequence(index + 1))

    def handle_click(self, color):
        if not self.is_player_turn:
            return
        user_sequence.append(color)
        
        if user_sequence[-1] != current_sequence[len(user_sequence) - 1]:
            self.player_failed()
        elif len(user_sequence) == len(current_sequence):
            self.round_complete()
        
        self.animate_button(color)
        self.play_sound(color)

    def animate_button(self, color):
        self.buttons[color].config(bg="white")
        self.root.after(100, lambda: self.buttons[color].config(bg=color))

    def round_complete(self):
        if self.single_player:
            scores[1] += 1
            self.update_score_labels()
            self.level += 1
            self.game_speed = max(1000 - (self.level - 1) * LEVEL_INCREMENT, MAX_SPEED)
            user_sequence.clear()
            self.root.after(1000, self.next_round)
        else:
            self.multiplayer_round_complete()

    def multiplayer_round_complete(self):
        scores[self.player_turn] += 1
        self.update_score_labels()
        self.player_turn = 2 if self.player_turn == 1 else 1
        self.status_label.config(text=f"Turno do Jogador {self.player_turn}")
        user_sequence.clear()
        self.root.after(1000, self.next_round)

    def player_failed(self):
        lives[self.player_turn] -= 1
        if lives[self.player_turn] == 0:
            winner = "Jogador 2" if self.player_turn == 1 else "Jogador 1"
            messagebox.showinfo("Fim de Jogo", f"{winner} venceu!")
            self.reset_game()
            self.create_menu_screen()
        else:
            messagebox.showinfo("Erro", f"Você errou! Vidas restantes: {lives[self.player_turn]}")
            self.player_turn = 2 if self.player_turn == 1 else 1
            user_sequence.clear()
            self.next_round()

    def update_score_labels(self):
        if self.single_player:
            self.score_label1.config(text=f"Pontos: {scores[1]}")
            self.status_label.config(text=f"Vidas: {lives[1]}")
        else:
            self.score_label1.config(text=f"Jogador 1: {scores[1]}")
            self.score_label2.config(text=f"Jogador 2: {scores[2]}")
            self.status_label.config(text=f"Vidas - Jogador 1: {lives[1]} | Jogador 2: {lives[2]}")

    def play_sound(self, color):
        sound = SOUNDS.get(color)
        if sound:
            sound.play()

root = tk.Tk()
game = BrilliantMelody(root)
root.mainloop()
