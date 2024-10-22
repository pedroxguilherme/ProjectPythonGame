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
    wave = wave.astype(np.int16)

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
scores = {1: 0, 2: 0}  # Pontuação para jogadores
lives = {1: 3, 2: 3}  # Vidas para multiplayer

class BrilliantMelody:
    def __init__(self, root):
        self.root = root
        self.root.title("Brilliant Melody")
        self.root.geometry("400x500")  # Definir um tamanho fixo
        self.root.configure(bg="#2e2e2e")  # Fundo mais escuro para contraste
        
        self.is_player_turn = False
        self.level = 1
        self.game_speed = GAME_SPEED
        self.single_player = True  # Por padrão, iniciar no modo single player
        self.buttons = {}
        self.create_buttons()
        self.reset_game()

    def create_buttons(self):
        button_frame = tk.Frame(self.root, bg="#2e2e2e")
        button_frame.pack(pady=20)

        for i, color in enumerate(COLORS):
            button = tk.Button(button_frame, bg=color, width=8, height=4, 
                               command=lambda c=color: self.handle_click(c),
                               activebackground=color, relief="flat")
            button.grid(row=0 if i < 2 else 1, column=i % 2, padx=10, pady=10)
            self.buttons[color] = button

        self.status_label = tk.Label(self.root, text="Escolha um modo para começar!", 
                                     font=('Helvetica', 14), bg="#2e2e2e", fg="white")
        self.status_label.pack(pady=10)

        self.score_label = tk.Label(self.root, text="Jogador 1: 0 | Jogador 2: 0", 
                                    font=('Helvetica', 12), bg="#2e2e2e", fg="white")
        self.score_label.pack(pady=5)

        control_frame = tk.Frame(self.root, bg="#2e2e2e")
        control_frame.pack(pady=10)

        self.start_button = tk.Button(control_frame, text="Novo Jogo", command=self.select_mode,
                                      font=('Helvetica', 12), width=15, bg="#1f6f8b", fg="white",
                                      activebackground="#145e77", relief="flat")
        self.start_button.pack(pady=10)

    def select_mode(self):
        """Exibe um menu para selecionar o modo de jogo (Single ou Multiplayer)."""
        mode = messagebox.askquestion("Modo de Jogo", "Deseja jogar no modo Single Player? (Clique em 'Não' para Multiplayer)")
        self.single_player = (mode == 'yes')
        self.start_game()

    def start_game(self):
        self.reset_game()
        self.root.after(self.game_speed, self.next_round)

    def next_round(self):
        global player_turn

        if not self.single_player:
            if player_turn == 1:
                self.status_label.config(text="Turno: Jogador 1")
            else:
                self.status_label.config(text="Turno: Jogador 2")
        else:
            self.status_label.config(text="Turno: Jogador 1 (Single Player)")

        self.is_player_turn = False
        user_sequence.clear()
        self.add_to_sequence()
        self.show_sequence(0)

    def reset_game(self):
        global current_sequence, player_turn, scores, lives
        current_sequence = []
        player_turn = 1
        scores = {1: 0, 2: 0}
        lives = {1: 3, 2: 3}  # Resetar vidas no multiplayer
        self.update_score_label()
        self.level = 1
        self.game_speed = GAME_SPEED

    def add_to_sequence(self):
        current_sequence.append(random.choice(COLORS))

    def show_sequence(self, index):
        if index < len(current_sequence):
            color = current_sequence[index]
            self.buttons[color].config(bg="white")  # Alterar para branco para piscar
            self.play_sound(color)

            # Esperar 500ms e restaurar a cor original
            self.root.after(500, lambda: self.hide_button(color, index))
        else:
            self.is_player_turn = True
            self.status_label.config(text="Sua vez!")

    def hide_button(self, color, index):
        # Restaurar a cor original e seguir para o próximo botão na sequência
        self.buttons[color].config(bg=color)
        self.root.after(500, lambda: self.show_sequence(index + 1))

    def handle_click(self, color):
        if not self.is_player_turn:
            return

        user_sequence.append(color)
        self.play_sound(color)

        if user_sequence[-1] != current_sequence[len(user_sequence) - 1]:
            self.player_failed()
        elif len(user_sequence) == len(current_sequence):
            self.round_complete()

    def round_complete(self):
        global player_turn

        # Atualiza o placar
        scores[player_turn] += 1
        self.update_score_label()

        if self.single_player:
            # Aumenta a dificuldade reduzindo o tempo de espera
            if self.game_speed > MAX_SPEED:
                self.game_speed -= LEVEL_INCREMENT
                self.level += 1
            self.root.after(1000, self.next_round)
        else:
            # Alterna o turno entre os jogadores
            if player_turn == 1:
                player_turn = 2
            else:
                player_turn = 1
            self.root.after(1000, self.next_round)

    def player_failed(self):
        global player_turn

        if self.single_player:
            messagebox.showinfo("Fim de Jogo", "Você perdeu! Tente novamente.")
            self.reset_game()
        else:
            lives[player_turn] -= 1
            if lives[player_turn] == 0:
                messagebox.showinfo("Fim de Jogo", f"Jogador {3 - player_turn} venceu!")
                self.reset_game()
            else:
                messagebox.showinfo("Erro", f"Jogador {player_turn} perdeu uma vida. Restam {lives[player_turn]} vidas.")
                self.update_score_label()
                self.next_round()

    def update_score_label(self):
        self.score_label.config(text=f"Jogador 1: {scores[1]} | Jogador 2: {scores[2]} | Vidas: Jogador 1: {lives[1]} | Jogador 2: {lives[2]}")

    def play_sound(self, color):
        sound = SOUNDS.get(color)
        if sound:
            sound.play()

# Iniciar aplicação
root = tk.Tk()
app = BrilliantMelody(root)
root.mainloop()
