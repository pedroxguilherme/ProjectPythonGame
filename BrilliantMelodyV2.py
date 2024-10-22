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
    'yellow': generate_tone(770) # G#
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
        self.root.geometry("800x600")  # Tamanho fixo maior
        self.root.configure(bg="#2e2e2e")  # Fundo mais escuro para contraste

        self.is_player_turn = False
        self.level = 1
        self.game_speed = GAME_SPEED
        self.single_player = True  # Iniciar no modo single player
        self.buttons = {}
        self.score_label = None  # Inicializar score_label como None
        self.create_menu()
        self.create_loading_screen()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        game_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Game", menu=game_menu)
        game_menu.add_command(label="Novo Jogo", command=self.select_mode)
        game_menu.add_command(label="Sair", command=self.root.quit)

    def create_loading_screen(self):
        self.loading_frame = tk.Frame(self.root, bg="#2e2e2e")
        self.loading_frame.place(relwidth=1, relheight=1)

        loading_label = tk.Label(self.loading_frame, text="Brilliant Melody", 
                                  font=('Helvetica', 36), bg="#2e2e2e", fg="white")
        loading_label.pack(pady=200)

        self.root.after(2000, self.setup_game)  # Espera 2 segundos antes de iniciar o jogo

    def setup_game(self):
        self.loading_frame.destroy()
        self.create_buttons()
        self.create_scoreboard()  # Cria a tabela de pontuação
        self.reset_game()
        self.start_game()

    def create_buttons(self):
        button_frame = tk.Frame(self.root, bg="#2e2e2e")
        button_frame.pack(pady=20)

        button_width = 15
        button_height = 8
        for i, color in enumerate(COLORS):
            button = tk.Button(button_frame, bg=color, width=button_width, height=button_height,
                               command=lambda c=color: self.handle_click(c),
                               activebackground=color, relief="flat")
            button.grid(row=0 if i < 2 else 1, column=i % 2, padx=10, pady=10, ipadx=10, ipady=10)
            self.buttons[color] = button

    def create_scoreboard(self):
        score_frame = tk.Frame(self.root, bg="#2e2e2e")
        score_frame.pack(pady=10)

        self.status_label = tk.Label(score_frame, text="Escolha um modo para começar!",
                                     font=('Helvetica', 14), bg="#2e2e2e", fg="white")
        self.status_label.pack(side=tk.LEFT, padx=10)

        self.score_label = tk.Label(score_frame, text="Jogador 1: 0 | Jogador 2: 0",
                                     font=('Helvetica', 12), bg="#2e2e2e", fg="white")
        self.score_label.pack(side=tk.RIGHT, padx=10)

        self.player1_character = tk.Label(self.root, text="🤖", font=('Helvetica', 24), bg="#2e2e2e")
        self.player1_character.place(relx=0.25, rely=0.1)

        self.player2_character = tk.Label(self.root, text="👾", font=('Helvetica', 24), bg="#2e2e2e")
        self.player2_character.place(relx=0.75, rely=0.1)

        control_frame = tk.Frame(self.root, bg="#2e2e2e")
        control_frame.pack(pady=10)
        self.start_button = tk.Button(control_frame, text="Novo Jogo", command=self.select_mode,
                                      font=('Helvetica', 12), width=15, bg="#1f6f8b", fg="white",
                                      activebackground="#145e77", relief="flat")
        self.start_button.pack(pady=10)

    def select_mode(self):
        mode = messagebox.askquestion("Modo de Jogo", "Deseja jogar no modo Single Player? (Clique em 'Não' para Multiplayer)")
        self.single_player = (mode == 'yes')

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
        self.update_score_label()  # Atualizar a tabela de pontuação
        self.level = 1
        self.game_speed = GAME_SPEED

    def add_to_sequence(self):
        current_sequence.append(random.choice(COLORS))
        print(f"Sequência atual: {current_sequence}")  # Depuração

    def show_sequence(self, index):
        if index < len(current_sequence):
            color = current_sequence[index]
            self.buttons[color].config(bg="white")  # Alterar para branco para piscar
            self.play_sound(color)
            self.root.after(500, lambda: self.hide_button(color, index))
        else:
            self.is_player_turn = True
            self.status_label.config(text="Sua vez!")

    def hide_button(self, color, index):
        self.buttons[color].config(bg=color)
        self.root.after(500, lambda: self.show_sequence(index + 1))

    def handle_click(self, color):
        if not self.is_player_turn:
            return
        
        user_sequence.append(color)
        print(f"Sequência do usuário: {user_sequence}")  # Depuração

        # Verificar se user_sequence não está vazia e se estamos acessando um índice válido
        if len(user_sequence) > 0 and len(user_sequence) <= len(current_sequence):
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
        global player_turn
        if self.single_player:
            self.level += 1
            scores[1] += 1
            self.update_score_label()
            self.game_speed = max(1000 - (self.level - 1) * LEVEL_INCREMENT, MAX_SPEED)
            user_sequence.clear()
            self.root.after(1000, self.next_round)
        else:
            scores[player_turn] += 1  # Incrementa a pontuação do jogador atual
            self.update_score_label()
            self.level += 1
            self.game_speed = max(1000 - (self.level - 1) * LEVEL_INCREMENT, MAX_SPEED)
            user_sequence.clear()
            player_turn = 2 if player_turn == 1 else 1  # Troca de jogador
            self.root.after(1000, self.next_round)

    def player_failed(self):
        global player_turn
        if self.single_player:
            messagebox.showinfo("Fim de Jogo", "Você perdeu! Tente novamente!")
            self.reset_game()
        else:
            lives[player_turn] -= 1
            if lives[player_turn] == 0:
                messagebox.showinfo("Fim de Jogo", f"Jogador {player_turn} perdeu! Jogador {2 if player_turn == 1 else 1} vence!")
                self.reset_game()
            else:
                messagebox.showinfo("Erro", f"Jogador {player_turn}, você errou! Vidas restantes: {lives[player_turn]}")
                player_turn = 2 if player_turn == 1 else 1
                self.root.after(1000, self.next_round)

    def play_sound(self, color):
        SOUNDS[color].play()

    def update_score_label(self):
        self.score_label.config(text=f"Jogador 1: {scores[1]} | Jogador 2: {scores[2]}")

if __name__ == "__main__":
    root = tk.Tk()
    game = BrilliantMelody(root)
    root.mainloop()
