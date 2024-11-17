import pygame
import sys
import random
from pygame.locals import QUIT
import itertools
import subprocess  # Para rodar o jogo como um subprocesso

# Inicialização do Pygame
pygame.init()

# Definir cores
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GRAY = (169, 169, 169)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Tamanho da tela
WIDTH, HEIGHT = 600, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brilliant Melody")

# Tamanho dos botões
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50

# Fonte
font = pygame.font.SysFont("Arial", 30)
large_font = pygame.font.SysFont("Arial", 50)

# Variável de controle do som
sound_muted = False

# Variável para cor do fundo e velocidade de mudança de cor
background_color = [0, 0, 0]  # Inicialmente preto
color_change_speed = 0.2  # Velocidade de transição lenta
color_stages = [(0, 0, 0)]  # Azul, vermelho, preto
current_stage = 0  # Índice da cor inicial

# Função para desenhar o fundo animado com degradê entre azul, vermelho e preto
def draw_animated_background():
    global current_stage, background_color

    # Obter a próxima cor-alvo no ciclo
    target_color = color_stages[(current_stage + 1) % len(color_stages)]

    # Transição gradual da cor atual para a cor-alvo
    for i in range(3):  # RGB
        if background_color[i] < target_color[i]:
            background_color[i] = min(background_color[i] + color_change_speed, target_color[i])
        elif background_color[i] > target_color[i]:
            background_color[i] = max(background_color[i] - color_change_speed, target_color[i])

    # Verificar se a transição para a cor atual está completa
    if all(abs(background_color[i] - target_color[i]) < color_change_speed for i in range(3)):
        current_stage = (current_stage + 1) % len(color_stages)  # Passa para a próxima cor no ciclo

    # Atualiza a tela com a nova cor de fundo
    window.fill(tuple(int(c) for c in background_color))

# Função para desenhar o título com animação
def draw_title():
    title_text = "Brilliant Melody"
    colors = [GREEN, BLUE, YELLOW, RED]
    shadow_color = BLACK
    x = (WIDTH - sum(large_font.size(letter)[0] for letter in title_text)) // 2  # Centralizar o título

    for i, letter in enumerate(title_text):
        # Seleciona a cor, alternando entre as cores
        color = colors[(i + pygame.time.get_ticks() // 500) % len(colors)]  # Alterna a cor a cada 500 ms
        
        # Renderiza a sombra
        shadow_surface = large_font.render(letter, True, shadow_color)
        for dx, dy in itertools.product([-1, 1], repeat=2):
            window.blit(shadow_surface, (x + dx, 50 + dy))  # Desenha a sombra ao redor

        # Renderiza a letra principal com uma borda mais espessa
        letter_surface = large_font.render(letter, True, color)
        for dx, dy in itertools.product([-1, 0, 1], repeat=2):
            if dx != 0 or dy != 0:  # Evitar o centro para não sobrescrever
                window.blit(letter_surface, (x + dx, 50 + dy))

        # Renderiza a letra no centro para a camada principal
        window.blit(letter_surface, (x, 50))

        # Atualiza a posição x para a próxima letra
        x += letter_surface.get_width()  

# Função para desenhar o botão com animação similar ao título
def draw_button(text, x, y, width, height, color, text_color):
    shadow_color = BLACK
    colors = [GREEN, BLUE, YELLOW, RED]
    
    # Desenho da caixa do botão
    pygame.draw.rect(window, color, (x, y, width, height))

    # Animação das letras do botão
    x_pos = x + (width - font.size(text)[0]) // 2  # Centraliza o texto
    y_pos = y + (height - font.size(text)[1]) // 2  # Centraliza o texto

    for i, letter in enumerate(text):
        # Alterna a cor da letra
        color = colors[(i + pygame.time.get_ticks() // 500) % len(colors)]  # Alterna a cor a cada 500 ms

        # Renderiza a sombra
        shadow_surface = font.render(letter, True, shadow_color)
        for dx, dy in itertools.product([-1, 1], repeat=2):
            window.blit(shadow_surface, (x_pos + dx, y_pos + dy))  # Desenha a sombra ao redor

        # Renderiza a letra principal com uma borda mais espessa
        letter_surface = font.render(letter, True, color)
        for dx, dy in itertools.product([-1, 0, 1], repeat=2):
            if dx != 0 or dy != 0:  # Evitar o centro para não sobrescrever
                window.blit(letter_surface, (x_pos + dx, y_pos + dy))

        # Renderiza a letra no centro para a camada principal
        window.blit(letter_surface, (x_pos, y_pos))

        # Atualiza a posição para a próxima letra
        x_pos += letter_surface.get_width()

# Função para exibir opções
def options():
    global sound_muted
    window.fill(GRAY)

    if sound_muted:
        sound_text = "Som: Mudo"
    else:
        sound_text = "Som: Ativado"
        
    sound_surface = font.render(sound_text, True, WHITE)
    window.blit(sound_surface, (WIDTH//2 - sound_surface.get_width()//2, HEIGHT//2 - 50))

    # Botão de Mudo/Ativado
    draw_button("Alternar Som", WIDTH//2 - BUTTON_WIDTH//2, HEIGHT//2 + 50, BUTTON_WIDTH, BUTTON_HEIGHT, BLUE, WHITE)

    back_button = font.render("Voltar", True, WHITE)
    window.blit(back_button, (WIDTH//2 - back_button.get_width()//2, HEIGHT - 100))

    pygame.display.update()

    # Esperar por evento
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Voltar ao menu
                if WIDTH//2 - back_button.get_width()//2 <= mouse_x <= WIDTH//2 + back_button.get_width()//2 and HEIGHT - 100 <= mouse_y <= HEIGHT - 50:
                    waiting = False
                # Alternar som
                if WIDTH//2 - BUTTON_WIDTH//2 <= mouse_x <= WIDTH//2 + BUTTON_WIDTH//2 and HEIGHT//2 + 50 <= mouse_y <= HEIGHT//2 + 50 + BUTTON_HEIGHT:
                    sound_muted = not sound_muted  # Alterna o estado do som
                    pygame.mixer.music.set_volume(0 if sound_muted else 1)  # Atualiza volume

# Função para iniciar o jogo
def start_game(multiplayer=False):
    # Aqui, chame o seu arquivo V4.py com um argumento de multiplayer
    # Substitua 'V4.py' pelo caminho correto do seu arquivo
    subprocess.run(['python', 'V4.py', 'multiplayer' if multiplayer else 'singleplayer'])  # Ajuste o nome do arquivo

# Função para o menu
def menu():
    running = True
    while running:
        draw_animated_background()  # Desenha fundo animado
        draw_title()  # Desenhar o título centralizado

        # Desenhar os botões com animação
        draw_button("Iniciar Solo", 200, 200, BUTTON_WIDTH, BUTTON_HEIGHT, BLACK, WHITE)
        draw_button("Iniciar Multiplayer", 200, 270, BUTTON_WIDTH, BUTTON_HEIGHT, BLACK, WHITE)
        draw_button("Opções", 200, 340, BUTTON_WIDTH, BUTTON_HEIGHT, BLACK, WHITE)
        draw_button("Sair", 200, 410, BUTTON_WIDTH, BUTTON_HEIGHT, BLACK, WHITE)

        # Verificar eventos
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                # Verificar se o botão "Iniciar Solo" foi clicado
                if 200 <= mouse_x <= 400 and 200 <= mouse_y <= 250:
                    running = False  # Fecha o menu e inicia o jogo
                    start_game(multiplayer=False)  # Inicia o modo Singleplayer

                # Verificar se o botão "Iniciar Multiplayer" foi clicado
                elif 200 <= mouse_x <= 400 and 270 <= mouse_y <= 320:
                    running = False
                    start_game(multiplayer=True)  # Inicia o modo Multiplayer

                # Verificar se o botão "Opções" foi clicado
                elif 200 <= mouse_x <= 400 and 340 <= mouse_y <= 390:
                    options()  # Exibe opções

                # Verificar se o botão "Sair" foi clicado
                elif 200 <= mouse_x <= 400 and 410 <= mouse_y <= 460:
                    running = False  # Sai do jogo

        pygame.display.update()

# Chama o menu para começar
menu()
