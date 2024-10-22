import tkinter as tk
import random
from tkinter import messagebox
import pygame
import numpy as np

# Inicializar pygame para tocar sons
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

def generate_tone(frequency, duration=0.5, sample_rate=44100):
    """Gera um som de frequência e duração específicas em estéreo."""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = 32767 * np.sin(2 * np.pi * frequency * t)
    wave = wave.astype(np.int16)  # Converte para 16-bit

    # Cria um array 2D para o áudio estéreo
    stereo_wave = np.zeros((wave.size, 2), dtype=np.int16)
    stereo_wave[:, 0] = wave  # Canal esquerdo
    stereo_wave[:, 1] = wave  # Canal direito

    sound = pygame.sndarray.make_sound(stereo_wave)
    return sound

# Sons personalizados para cada cor
SOUNDS = {
    'red': generate_tone(440),   # A
    'green': generate_tone(550), # C#
    'blue': generate_tone(660),  # E
    'yellow': generate_tone(770)  # G#
}

# Configurações do jogo
COLORS = ['red', 'green', 'blue', 'yellow']
GAME_SPEED = 1000  # Velocidade inicial
LEVEL_INCREMENT = 100  # Aumento de velocidade por nível
MAX_SPEED = 300  # Limite máximo de velocidade
current_sequence = []
user_sequence = []
player_turn = 1
scores = {1: 0, 2: 0}  # Pontuação para jogador 1 e 2

class SimonSays:
    def __init__(self, root):
        self.root = root
        self.root.title("Brilliant Melody")
        self.is_player_turn = False
        self.level = 1
        self.game_speed = GAME_SPEED
        self.buttons = {}
        self.create_buttons()
        self.reset_game()

    def create_buttons(self):
        for i, color in enumerate(COLORS):
            button = tk.Button(self.root, bg=color, width=10, height=5, command=lambda c=color: self.handle_click(c))
            button.grid(row=1, column=i)
            self.buttons[color] = button

        self.status_label = tk.Label(self.root, text="Aperte Start para começar!", font=('Helvetica', 14))
        self.status_label.grid(row=0, column=0, columnspan=4)

        self.score_label = tk.Label(self.root, text="Jogador 1: 0 | Jogador 2: 0", font=('Helvetica', 14))
        self.score_label.grid(row=3, column=0, columnspan=4)

        self.start_button = tk.Button(self.root, text="Start", command=self.start_game)
        self.start_button.grid(row=2, column=0, columnspan=4)

    def start_game(self):
        self.reset_game()
        self.root.after(self.game_speed, self.next_round)

    def next_round(self):
        global player_turn

        if player_turn == 1:
            self.status_label.config(text="Turno: Jogador 1")
        else:
            self.status_label.config(text="Turno: Jogador 2")

        self.is_player_turn = False
        user_sequence.clear()
        self.add_to_sequence()
        self.show_sequence(0)

    def reset_game(self):
        global current_sequence, player_turn, scores
        current_sequence = []
        player_turn = 1
        scores = {1: 0, 2: 0}
        self.update_score_label()
        self.level = 1
        self.game_speed = GAME_SPEED

    def add_to_sequence(self):
        current_sequence.append(random.choice(COLORS))

    def show_sequence(self, index):
        if index < len(current_sequence):
            color = current_sequence[index]
            self.play_sound(color)
            self.buttons[color].config(state=tk.ACTIVE)
            self.root.after(500, lambda: self.hide_button(color, index))
        else:
            self.is_player_turn = True
            self.status_label.config(text="Sua vez!")

    def hide_button(self, color, index):
        self.buttons[color].config(state=tk.NORMAL)
        self.root.after(500, lambda: self.show_sequence(index + 1))

    def handle_click(self, color):
        if not self.is_player_turn:
            return

        user_sequence.append(color)
        self.play_sound(color)

        if user_sequence[-1] != current_sequence[len(user_sequence) - 1]:
            self.game_over()
        elif len(user_sequence) == len(current_sequence):
            global player_turn

            # Atualiza o placar
            scores[player_turn] += 1
            self.update_score_label()

            # Alterna o turno entre os jogadores
            if player_turn == 1:
                player_turn = 2
            else:
                player_turn = 1

            # Aumenta a dificuldade reduzindo o tempo de espera
            if self.game_speed > MAX_SPEED:
                self.game_speed -= LEVEL_INCREMENT
                self.level += 1

            self.root.after(1000, self.next_round)

    def game_over(self):
        global player_turn
        if player_turn == 1:
            messagebox.showinfo("Fim de Jogo", "Jogador 2 Ganhou!")
        else:
            messagebox.showinfo("Fim de Jogo", "Jogador 1 Ganhou!")
        self.reset_game()

    def update_score_label(self):
        self.score_label.config(text=f"Jogador 1: {scores[1]} | Jogador 2: {scores[2]}")

    def play_sound(self, color):
        sound = SOUNDS.get(color)
        if sound:
            sound.play()

# Iniciar aplicação
root = tk.Tk()
app = SimonSays(root)
root.mainloop()
