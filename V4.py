import pygame
from random import randrange
import time
from tkinter import Tk, Button
import json
import os
import tkinter as tk
import tkinter.simpledialog

# Inicializando o tkinter
root = Tk()
root.withdraw()  # Esconde a janela principal do tkinter

# Inicializando o mixer de áudio do pygame
pygame.mixer.init()

# Nome do arquivo para salvar o ranking
RANKING_FILE = "ranking.json"

# Funções de ranking
def carregar_ranking():
    """Carrega o ranking do arquivo JSON. Inicializa se o arquivo estiver vazio ou inválido."""
    if not os.path.exists(RANKING_FILE):
        with open(RANKING_FILE, "w") as file:
            json.dump([], file)  # Inicializa com uma lista vazia
    try:
        with open(RANKING_FILE, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        # Se o JSON estiver inválido, reescreve com uma lista vazia
        with open(RANKING_FILE, "w") as file:
            json.dump([], file)
        return []

def salvar_ranking(nome, pontuacao):
    """Salva a pontuação de um jogador no ranking."""
    ranking = carregar_ranking()
    ranking.append({"nome": nome, "pontuacao": pontuacao})
    ranking.sort(key=lambda x: x["pontuacao"], reverse=True)
    with open(RANKING_FILE, "w") as file:
        json.dump(ranking, file, indent=4)
    

def exibir_ranking():
    """Exibe o ranking em uma nova janela."""
    ranking = carregar_ranking()
    janela_ranking = tk.Toplevel(root)
    janela_ranking.title("Ranking")
    tk.Label(janela_ranking, text="=== RANKING ===", font=("Arial", 16)).pack(pady=10)
    for i, entrada in enumerate(ranking[:10], 1):  # Top 10
        tk.Label(janela_ranking, text=f"{i}. {entrada['nome']} - {entrada['pontuacao']} pontos").pack()
    tk.Button(janela_ranking, text="Fechar", command=janela_ranking.destroy).pack(pady=10)

from tkinter.simpledialog import askstring  # Certifique-se de importar assim

import tkinter as tk
from tkinter.simpledialog import askstring
import json

def finalizar_jogo(score):
    # Janela para registrar o nome do jogador
    janela_game_over = tk.Tk()
    janela_game_over.title("Game Over")
    janela_game_over.geometry("300x200")

    # Exibe a mensagem de fim de jogo
    tk.Label(
        janela_game_over, text=f"Fim de Jogo! Pontuação Final: {score}", font=("Arial", 14)
    ).pack(pady=10)

    # Captura o nome do jogador
    nome = askstring("Registro de Nome", "Digite seu nome:", parent=janela_game_over)

    # Processa o nome e a pontuação, salva no arquivo
    if nome:
        try:
            # Tenta carregar o ranking existente
            with open("ranking.json", "r") as arquivo:
                ranking = json.load(arquivo)
                if not isinstance(ranking, dict):
                    ranking = {}
        except FileNotFoundError:
            ranking = {}

        # Adiciona a pontuação do jogador
        ranking[nome] = score
        with open("ranking.json", "w") as arquivo:
            json.dump(ranking, arquivo, indent=4)

    # Fecha a janela após o nome ser inserido
    janela_game_over.destroy()

    # Exibe uma mensagem para o jogador sobre o fim do jogo e reinício
    tk.messagebox.showinfo("Fim de Jogo", "Clique para reiniciar o jogo!")
    reiniciar_jogo()  # Chame a função que reinicia o jogo, se necessário

# Função para reiniciar o jogo (substitua com a lógica real)
def reiniciar_jogo():
    print("Reiniciando o jogo...")  # Aqui você pode colocar o código para reiniciar o jogo

# Carregando o som
game_start = pygame.mixer.Sound('./sound/game_start.wav')
game_over = pygame.mixer.Sound('./sound/game_over.wav')
blue_sound = pygame.mixer.Sound('./sound/blue_sound.mp3')
red_sound = pygame.mixer.Sound('./sound/red_sound.wav')
green_sound = pygame.mixer.Sound('./sound/green_sound.wav')
yellow_sound = pygame.mixer.Sound('./sound/yellow_sound.wav')

# Cores do Jogo
preto = (0, 0, 0)
cinza = (100, 100, 100)
branco = (255, 255, 255)
vermelho = (255, 100, 100)
vermelho_escuro = (200, 0, 0)
amarelo = (255, 255, 150)
amarelo_escuro = (255, 255, 0)
verde = (100, 255, 100)
verde_escuro = (0, 200, 0)
azul = (150, 150, 255)
azul_escuro = (0, 0, 255)

# Setup da tela do Jogo
window = pygame.display.set_mode((600, 600))
window.fill(branco)
pygame.display.set_caption("Brilliant Disse!")

# Inicializando fonte
pygame.font.init()
# Escolhendo uma fonte e tamanho
fonte = pygame.font.SysFont("Comic Sans MS", 30)

# Variáveis do Jogo
click_on_off = 0
sequencia_do_jogo = []
repeticao_das_cores = 0
resposta = []

def inicio(window):
    pygame.draw.rect(window, verde_escuro, (100, 100, 200, 200))
    pygame.draw.rect(window, vermelho_escuro, (300, 100, 200, 200))
    pygame.draw.rect(window, amarelo_escuro, (100, 300, 200, 200))
    pygame.draw.rect(window, azul_escuro, (300, 300, 200, 200))
    pygame.draw.rect(window, preto, (100, 300, 400, 10))
    pygame.draw.rect(window, preto, (300, 100, 10, 400))
    pygame.draw.circle(window, branco, (300, 300), 300, 100)
    pygame.draw.circle(window, preto, (300, 300), 90)
    pygame.draw.circle(window, preto, (300, 300), 210, 10)
    texto = fonte.render("Brilliant", 1, branco)
    window.blit(texto, (260, 275))
    pygame.display.update()

def b_verde(window):
    pygame.draw.rect(window, verde, (100, 100, 200, 200))
    pygame.draw.rect(window, vermelho_escuro, (300, 100, 200, 200))
    pygame.draw.rect(window, amarelo_escuro, (100, 300, 200, 200))
    pygame.draw.rect(window, azul_escuro, (300, 300, 200, 200))
    pygame.draw.rect(window, preto, (100, 300, 400, 10))
    pygame.draw.rect(window, preto, (300, 100, 10, 400))
    pygame.draw.circle(window, branco, (300, 300), 300, 100)
    pygame.draw.circle(window, preto, (300, 300), 90)
    pygame.draw.circle(window, preto, (300, 300), 210, 10)
    texto = fonte.render("Melody", 1, branco)
    window.blit(texto, (260, 275))
    pygame.display.update()

def b_vermelho(window):
    pygame.draw.rect(window, verde_escuro, (100, 100, 200, 200))
    pygame.draw.rect(window, vermelho, (300, 100, 200, 200))
    pygame.draw.rect(window, amarelo_escuro, (100, 300, 200, 200))
    pygame.draw.rect(window, azul_escuro, (300, 300, 200, 200))
    pygame.draw.rect(window, preto, (100, 300, 400, 10))
    pygame.draw.rect(window, preto, (300, 100, 10, 400))
    pygame.draw.circle(window, branco, (300, 300), 300, 100)
    pygame.draw.circle(window, preto, (300, 300), 90)
    pygame.draw.circle(window, preto, (300, 300), 210, 10)
    texto = fonte.render("Melody", 1, branco)
    window.blit(texto, (260, 275))
    pygame.display.update()

def b_amarelo(window):
    pygame.draw.rect(window, verde_escuro, (100, 100, 200, 200))
    pygame.draw.rect(window, vermelho_escuro, (300, 100, 200, 200))
    pygame.draw.rect(window, amarelo, (100, 300, 200, 200))
    pygame.draw.rect(window, azul_escuro, (300, 300, 200, 200))
    pygame.draw.rect(window, preto, (100, 300, 400, 10))
    pygame.draw.rect(window, preto, (300, 100, 10, 400))
    pygame.draw.circle(window, branco, (300, 300), 300, 100)
    pygame.draw.circle(window, preto, (300, 300), 90)
    pygame.draw.circle(window, preto, (300, 300), 210, 10)
    texto = fonte.render("Melody", 1, branco)
    window.blit(texto, (260, 275))
    pygame.display.update()

def b_azul(window):
    pygame.draw.rect(window, verde_escuro, (100, 100, 200, 200))
    pygame.draw.rect(window, vermelho_escuro, (300, 100, 200, 200))
    pygame.draw.rect(window, amarelo_escuro, (100, 300, 200, 200))
    pygame.draw.rect(window, azul, (300, 300, 200, 200))
    pygame.draw.rect(window, preto, (100, 300, 400, 10))
    pygame.draw.rect(window, preto, (300, 100, 10, 400))
    pygame.draw.circle(window, branco, (300, 300), 300, 100)
    pygame.draw.circle(window, preto, (300, 300), 90)
    pygame.draw.circle(window, preto, (300, 300), 210, 10)
    texto = fonte.render("Melody", 1, branco)
    window.blit(texto, (260, 275))
    pygame.display.update()

def b_centro(window):
    pygame.draw.rect(window, verde_escuro, (100, 100, 200, 200))
    pygame.draw.rect(window, vermelho_escuro, (300, 100, 200, 200))
    pygame.draw.rect(window, amarelo_escuro, (100, 300, 200, 200))
    pygame.draw.rect(window, azul_escuro, (300, 300, 200, 200))
    pygame.draw.rect(window, preto, (100, 300, 400, 10))
    pygame.draw.rect(window, preto, (300, 100, 10, 400))
    pygame.draw.circle(window, branco, (300, 300), 300, 100)
    pygame.draw.circle(window, preto, (300, 300), 90)
    pygame.draw.circle(window, preto, (300, 300), 210, 10)
    pygame.draw.circle(window, cinza, (300, 300), 80)
    texto = fonte.render("Melody", 1, branco)
    window.blit(texto, (260, 275))
    pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Declarando mouse:
    mouse = pygame.mouse.get_pos()

    # Declarando click do mouse
    click = pygame.mouse.get_pressed()

    # Lógica de repetição das cores
    if repeticao_das_cores == 1:
        inicio(window)
        time.sleep(0.5)
        for i in range(len(sequencia_do_jogo)):
            pygame.draw.rect(window, branco, (0, 0, 500, 50))
            texto = fonte.render(str(i + 1) + ' / ' + str(len(sequencia_do_jogo)), 1, preto)
            window.blit(texto, (10, 10))
            pygame.display.update()
            if sequencia_do_jogo[i] == 0:
                green_sound.play()
                b_verde(window)
            if sequencia_do_jogo[i] == 1:
                red_sound.play()
                b_vermelho(window)
            if sequencia_do_jogo[i] == 2:
                yellow_sound.play()
                b_amarelo(window)
            if sequencia_do_jogo[i] == 3:
                blue_sound.play()
                b_azul(window)
            time.sleep(0.5)
            inicio(window)
            time.sleep(0.5)
        repeticao_das_cores = 0

    # Lógica de Certo e Errado
    if resposta == sequencia_do_jogo and sequencia_do_jogo != []:
        repeticao_das_cores = 1
        sequencia_do_jogo.append(randrange(4))
        resposta = []
    if len(resposta) > 0 and \
      len(sequencia_do_jogo) > 0 and \
     resposta[len(resposta) - 1] != sequencia_do_jogo[len(resposta) - 1] and \
     sequencia_do_jogo != []:
     game_over.play()
     score = len(sequencia_do_jogo) - 1
     pygame.display.update()
     finalizar_jogo(score)  # Chama a função finalizar_jogo
     sequencia_do_jogo = []
     resposta = []
 

    # Verde
    if (mouse[0] - 300) ** 2 + (mouse[1] - 300) ** 2 <= 40000 and \
        (mouse[0] - 300) ** 2 + (mouse[1] - 300) ** 2 >= 8100 and \
        100 <= mouse[0] <= 300 and \
        100 <= mouse[1] <= 300:
        b_verde(window)
        if click[0] == 0 and click_on_off == 1:
            green_sound.play()
            resposta.append(0)
    # Vermelho
    elif (mouse[0] - 300) ** 2 + (mouse[1] - 300) ** 2 <= 40000 and \
        (mouse[0] - 300) ** 2 + (mouse[1] - 300) ** 2 >= 8100 and \
        300 <= mouse[0] <= 500 and \
        100 <= mouse[1] <= 300:
        b_vermelho(window)
        if click[0] == 0 and click_on_off == 1:
            red_sound.play()
            resposta.append(1)
    # Amarelo
    elif (mouse[0] - 300) ** 2 + (mouse[1] - 300) ** 2 <= 40000 and \
        (mouse[0] - 300) ** 2 + (mouse[1] - 300) ** 2 >= 8100 and \
        100 <= mouse[0] <= 300 and \
        300 <= mouse[1] <= 500:
        b_amarelo(window)
        if click[0] == 0 and click_on_off == 1:
            yellow_sound.play()
            resposta.append(2)
    # Azul
    elif (mouse[0] - 300) ** 2 + (mouse[1] - 300) ** 2 <= 40000 and \
        (mouse[0] - 300) ** 2 + (mouse[1] - 300) ** 2 >= 8100 and \
        300 <= mouse[0] <= 500 and \
        300 <= mouse[1] <= 500:
        b_azul(window)
        if click[0] == 0 and click_on_off == 1:
            blue_sound.play()
            resposta.append(3)
    # Centro - Restart
    elif (mouse[0] - 300) ** 2 + (mouse[1] - 300) ** 2 <= 6400:
        b_centro(window)
        if click[0] == 0 and click_on_off == 1:
            game_start.play()
            repeticao_das_cores = 1
            sequencia_do_jogo.append(randrange(4))
            resposta = []
    else:
        inicio(window)

    pygame.draw.rect(window, branco, (0, 0, 500, 50))
    texto = fonte.render(str(len(sequencia_do_jogo)), 1, preto)
    window.blit(texto, (10, 10))

    click_on_off = click[0]

    pygame.display.update()


