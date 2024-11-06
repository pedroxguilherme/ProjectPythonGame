import pygame
import sys
from pygame.locals import QUIT
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

# Função para desenhar o botão
def draw_button(text, x, y, width, height, color, text_color):
    pygame.draw.rect(window, color, (x, y, width, height))
    text_surface = font.render(text, True, text_color)
    window.blit(text_surface, (x + (width - text_surface.get_width()) // 2, y + (height - text_surface.get_height()) // 2))

# Função para desenhar o título
def draw_title():
    title_text = "Brilliant Melody"
    colors = [GREEN, BLUE, YELLOW, RED]
    x = (WIDTH - sum(large_font.size(letter)[0] for letter in title_text)) // 2  # Centralizar o título
    for i, letter in enumerate(title_text):
        color = colors[i % len(colors)]
        letter_surface = large_font.render(letter, True, color)
        window.blit(letter_surface, (x, 50))
        x += letter_surface.get_width()  # Ajustar a posição x para a próxima letra

# Função para quebrar o texto em várias linhas
def wrap_text(text, font, max_width):
    lines = []
    words = text.split(' ')
    current_line = words[0]

    for word in words[1:]:
        # Tenta adicionar a próxima palavra à linha atual
        test_line = current_line + ' ' + word
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    
    lines.append(current_line)  # Adiciona a última linha
    return lines

# Função para desenhar as regras de forma centralizada
def draw_rules():
    window.fill(GRAY)

    # Caixa de Regras
    pygame.draw.rect(window, WHITE, (50, 100, 500, 300))  # Caixa com fundo branco
    pygame.draw.rect(window, BLACK, (50, 100, 500, 300), 5)  # Borda preta

    # Texto das regras
    rules_text = """Regras:

O jogo consiste em uma plataforma de 4 cores (Azul, Amarelo, Verde e Vermelho), ela emitirá uma sequência de luzes
e sons e o jogador deverá decorar e acertar a sequência, assim avançando para o próximo nível."""

    # Quebrando o texto em várias linhas para caber na caixa
    lines = wrap_text(rules_text, font, 480)  # Tamanho máximo da linha 480 pixels
    line_height = font.get_height()

    # Calculando a altura inicial para centralizar verticalmente
    y_offset = 120  # Start drawing a little below the title bar (above the box)

    # Desenhando as linhas na tela
    for line in lines:
        line_surface = font.render(line, True, BLACK)
        x_offset = (WIDTH - line_surface.get_width()) // 2  # Centraliza horizontalmente
        window.blit(line_surface, (x_offset, y_offset))
        y_offset += line_height  # Atualiza a posição para a próxima linha

    # Botão de Voltar
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

# Função para o menu
def menu():
    running = True
    while running:
        window.fill(GRAY)

        # Desenhar o título centralizado
        draw_title()

        # Desenhar os botões
        draw_button("Iniciar", 200, 200, BUTTON_WIDTH, BUTTON_HEIGHT, GREEN, WHITE)
        draw_button("Opções", 200, 270, BUTTON_WIDTH, BUTTON_HEIGHT, BLUE, WHITE)
        draw_button("Regras", 200, 340, BUTTON_WIDTH, BUTTON_HEIGHT, YELLOW, WHITE)
        draw_button("Sair", 200, 410, BUTTON_WIDTH, BUTTON_HEIGHT, RED, WHITE)

        # Verificar eventos
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                # Verificar se o botão "Iniciar" foi clicado
                if 200 <= mouse_x <= 400 and 200 <= mouse_y <= 250:
                    running = False  # Fecha o menu e inicia o jogo
                    start_game()  # Chama o jogo

                # Verificar se o botão "Opções" foi clicado
                elif 200 <= mouse_x <= 400 and 270 <= mouse_y <= 320:
                    options()  # Exibe opções

                # Verificar se o botão "Regras" foi clicado
                elif 200 <= mouse_x <= 400 and 340 <= mouse_y <= 390:
                    draw_rules()  # Exibe as regras

                # Verificar se o botão "Sair" foi clicado
                elif 200 <= mouse_x <= 400 and 410 <= mouse_y <= 460:
                    running = False  # Sai do jogo

        pygame.display.update()

# Função para iniciar o jogo
def start_game():
    # Aqui, chame o seu arquivo V4.py (ajuste o caminho se necessário)
    subprocess.run(['python', 'V4.py'])  # Altere o nome se necessário

# Chama o menu para começar
menu()
