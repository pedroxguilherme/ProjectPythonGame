import pygame
from random import randrange
import time

# Inicializando o mixer de áudio do pygame
pygame.mixer.init()

# Carregando os sons
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
pygame.display.set_caption("Brilliant Melody - Multiplayer")

# Inicializando fonte
pygame.font.init()
fonte = pygame.font.SysFont("Comic Sans MS", 30)

# Variáveis do Jogo
click_on_off = 0
sequencia_do_jogo = []
resposta = []
jogador_atual = 1  # Alterna entre 1 e 2
repeticao_das_cores = 0
em_execucao = False  # Controle de quando o jogo realmente começa
jogador_esperando_resposta = {1: False, 2: False}  # Indica se o jogador está esperando para dar resposta
jogador_erro = None  # Controla quem errou


def exibir_status():
    """Exibe o jogador atual na tela."""
    pygame.draw.rect(window, branco, (0, 0, 600, 50))
    texto = fonte.render(f"Jogador {jogador_atual}", 1, preto)
    window.blit(texto, (10, 10))
    pygame.display.update()


# Funções para o layout do jogo
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
    exibir_status()


# Funções de destaque para botões
def destacar_cor(cor, window):
    cores = [verde_escuro, vermelho_escuro, amarelo_escuro, azul_escuro]
    if cor != -1:
        cores[cor] = [verde, vermelho, amarelo, azul][cor]
    pygame.draw.rect(window, cores[0], (100, 100, 200, 200))
    pygame.draw.rect(window, cores[1], (300, 100, 200, 200))
    pygame.draw.rect(window, cores[2], (100, 300, 200, 200))
    pygame.draw.rect(window, cores[3], (300, 300, 200, 200))
    pygame.draw.rect(window, preto, (100, 300, 400, 10))
    pygame.draw.rect(window, preto, (300, 100, 10, 400))
    pygame.draw.circle(window, branco, (300, 300), 300, 100)
    pygame.draw.circle(window, preto, (300, 300), 90)
    pygame.draw.circle(window, preto, (300, 300), 210, 10)
    texto = fonte.render("Melody", 1, branco)
    window.blit(texto, (260, 275))
    exibir_status()


# Lógica do jogo
def alternar_jogador():
    """Alterna para o próximo jogador."""
    global jogador_atual
    jogador_atual = 2 if jogador_atual == 1 else 1


def fim_de_jogo(vencedor):
    """Exibe o vencedor e reinicia o jogo."""
    game_over.play()
    pygame.draw.rect(window, branco, (0, 0, 600, 50))
    texto = fonte.render(f"Jogador {vencedor} venceu!", 1, vermelho)
    window.blit(texto, (150, 250))
    pygame.display.update()
    time.sleep(3)
    sequencia_do_jogo.clear()
    resposta.clear()
    alternar_jogador()
    global em_execucao
    em_execucao = False  # Fim do jogo


def atualizar_jogo():
    """Atualiza o estado do jogo."""
    global repeticao_das_cores
    if resposta == sequencia_do_jogo:
        repeticao_das_cores = 1
        resposta.clear()
        sequencia_do_jogo.append(randrange(4))
        jogador_esperando_resposta[jogador_atual] = False
    elif len(resposta) > 0 and resposta[-1] != sequencia_do_jogo[len(resposta) - 1]:
        fim_de_jogo(2 if jogador_atual == 1 else 1)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if repeticao_das_cores:
        inicio(window)
        time.sleep(0.5)
        for cor in sequencia_do_jogo:
            destacar_cor(cor, window)
            [green_sound, red_sound, yellow_sound, blue_sound][cor].play()
            time.sleep(0.5)
            inicio(window)
            time.sleep(0.5)
        repeticao_das_cores = 0
        jogador_esperando_resposta[jogador_atual] = True  # Habilita a espera pela resposta após a repetição das cores

    if em_execucao:  # O jogo começa quando o jogador clica para iniciar
        atualizar_jogo()

    # Clique no botão central para começar
    if not em_execucao and (mouse[0] - 300) ** 2 + (mouse[1] - 300) ** 2 <= 6400:  # Dentro do círculo
        destacar_cor(-1, window)  # Não altera cor
        if click[0] == 1 and click_on_off == 0:  # Clica uma vez
            game_start.play()
            repeticao_das_cores = 1
            sequencia_do_jogo.append(randrange(4))
            resposta.clear()
            jogador_esperando_resposta[jogador_atual] = False
            em_execucao = True  # O jogo começa de fato aqui

    # Verificando cliques nas áreas das cores
    if jogador_esperando_resposta[jogador_atual] and click[0] == 1 and click_on_off == 0:  # Apenas quando o clique é válido
        click_on_off = 1
        if 100 <= mouse[0] <= 300 and 100 <= mouse[1] <= 300:
            resposta.append(0)
            green_sound.play()
        elif 300 <= mouse[0] <= 500 and 100 <= mouse[1] <= 300:
            resposta.append(1)
            red_sound.play()
        elif 100 <= mouse[0] <= 300 and 300 <= mouse[1] <= 500:
            resposta.append(2)
            yellow_sound.play()
        elif 300 <= mouse[0] <= 500 and 300 <= mouse[1] <= 500:
            resposta.append(3)
            blue_sound.play()

    if click[0] == 0:
        click_on_off = 0

    pygame.display.update()
