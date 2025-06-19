import pygame
import random
import os
import tkinter as tk
from tkinter import messagebox
from recursos.funcoes import inicializarBancoDeDados
from recursos.funcoes import escreverDados
import pyttsx3
import json
import speech_recognition as sr

pygame.init()
inicializarBancoDeDados()
tamanho = (1000,700)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode( tamanho ) 
pygame.display.set_caption("DBZ")
icone = pygame.image.load("assets/icone.jpg")
pygame.display.set_icon(icone)
branco = (255,255,255)
preto = (0, 0 ,0)

goku_niveis = [
    pygame.transform.scale(pygame.image.load("assets/goku.png"), (200, 200)),          # Base
    pygame.transform.scale(pygame.image.load("assets/goku_ssj1.png"), (200, 200)),     # SSJ1
    pygame.transform.scale(pygame.image.load("assets/goku_ssj2.png"), (260, 260)),     # SSJ2
    pygame.transform.scale(pygame.image.load("assets/goku_ssj3.png"), (260, 260)),     # SSJ3
    pygame.transform.scale(pygame.image.load("assets/goku_god.png"), (300, 300)),      # God
    pygame.transform.scale(pygame.image.load("assets/goku_blue.png"), (300, 300)),     # Blue
    pygame.transform.scale(pygame.image.load("assets/goku_bluekaioken.png"), (300, 300)), # Blue Kaioken
    pygame.transform.scale(pygame.image.load("assets/goku_ui.png"), (350, 350)),       # UI
    pygame.transform.scale(pygame.image.load("assets/goku_mui.png"), (350, 350))       # MUI
]
fundoStart = pygame.image.load("assets/fundoStart.png")
fundoStart = pygame.transform.scale(fundoStart, (1000, 700))
fundoJogo = pygame.image.load("assets/fundoJogo.png")
fundoJogo = pygame.transform.scale(fundoJogo, (1000, 700))
fundoDead = pygame.image.load("assets/fundoDead.png")
fundoDead = pygame.transform.scale(fundoDead, (1000, 700))
ki = pygame.image.load("assets/ki.png")
ki = pygame.transform.scale(ki, (80, 80))
coracao_img = pygame.image.load("assets/coracao.png")
coracao_img = pygame.transform.scale(coracao_img, (40, 40))
kiSound = pygame.mixer.Sound("assets/ki_blast.mp3")
explosaoSound = pygame.mixer.Sound("assets/fracassado.mp3")
transformSound = pygame.mixer.Sound("assets/transform.mp3")
fonteMenu = pygame.font.SysFont("comicsans",25)
fonteMorte = pygame.font.SysFont("arial",120)
imagem_objeto = pygame.image.load("assets/objetovoando.png")
imagem_objeto = pygame.transform.scale(imagem_objeto, (50, 50))
objeto_largura, objeto_altura = imagem_objeto.get_size()
pygame.mixer.music.load("assets/blizzard.mp3")

def tela_instrucoes(nome):
    descricao_font = pygame.font.SysFont("comicsans", 28)
    dica_font = pygame.font.SysFont("comicsans", 24)

    # Tamanhos do quadro laranja
    largura_box = 900
    altura_box = 300
    x_box = (tamanho[0] - largura_box) // 2
    y_box = (tamanho[1] - altura_box) // 2

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    return  # Sai da tela e começa o jogo

        tela.blit(fundoJogo, (0, 0))  # Fundo do jogo

        # Cria um retângulo laranja opaco no centro
        pygame.draw.rect(tela, (255, 140, 0), (x_box, y_box, largura_box, altura_box), border_radius=20)

        # Título
        titulo = fonteMorte.render("DRAGON BLAST Z", True, preto)
        tela.blit(titulo, ((tamanho[0] - titulo.get_width()) // 2, y_box + 20))

        # Descrição (centralizada dentro do box)
        descricao = descricao_font.render("DESVIE DOS ATAQUES DE KI PARA PROTEGER A TERRA!", True, preto)
        tela.blit(descricao, ((tamanho[0] - descricao.get_width()) // 2, y_box + 130))

        # Dica para começar
        dica = dica_font.render("Pressione ENTER para começar", True, preto)
        tela.blit(dica, ((tamanho[0] - dica.get_width()) // 2, y_box + 200))

        pygame.display.update()
        relogio.tick(60)


def jogar():
        # Variáveis do objeto voador
    posicaoXObjeto = 0
    posicaoYObjeto = 40
    velocidadeObjeto = 5
    direcaoObjeto = 1
    objeto_largura, objeto_altura = imagem_objeto.get_size()

    largura_janela = 300
    altura_janela = 100
    def obter_nome():
        global nome
        nome = entry_nome.get()  # Obtém o texto digitado
        if not nome:  # Se o campo estiver vazio
            messagebox.showwarning("Aviso", "DIGITE SEU NOME, INSETO!")  # Exibe uma mensagem de aviso
        else:
            #print(f'Nome digitado: {nome}')  # Exibe o nome no console
            root.destroy()  # Fecha a janela após a entrada válida
        falar_boas_vindas(nome)
        tela_instrucoes(nome)  # Mostra a tela laranja antes do jogo começar

    def reconhecer_voz():
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Fale o seu nome:")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

            try:
                nome_reconhecido = recognizer.recognize_google(audio, language='pt-BR')
                print(f"Você disse: {nome_reconhecido}")

                # Preenche o campo de texto com o nome reconhecido
                entry_nome.delete(0, tk.END)  # Limpa o campo
                entry_nome.insert(0, nome_reconhecido)  # Coloca o nome reconhecido

            except sr.UnknownValueError:
                print("Não consegui entender o que você falou.")
            except sr.RequestError:
                print("Erro no serviço de reconhecimento.")
        
    def falar_boas_vindas(nome):
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)  # Velocidade da fala
        engine.setProperty('volume', 1.0)  # Volume máximo
        texto = f"Bem-vindo ao jogo, {nome}!"
        engine.say(texto)
        engine.runAndWait()            

        raio_sol = 100
        direcao_pulso = 1

    # Criação da janela principal
    root = tk.Tk()
    # Obter as dimensões da tela
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    pos_x = (largura_tela - largura_janela) // 2
    pos_y = (altura_tela - altura_janela) // 2
    root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
    root.title("Informe seu nome, guerreiero Z")
    root.protocol("WM_DELETE_WINDOW", obter_nome)

    # Entry (campo de texto)
    entry_nome = tk.Entry(root)
    entry_nome.pack()

    # Botão para pegar o nome
    botao = tk.Button(root, text="Enviar", command=obter_nome)
    botao.pack()
    botao_voz = tk.Button(root, text="Falar Nome", command=reconhecer_voz)
    botao_voz.pack()
    # Inicia o loop da interface gráfica
    root.mainloop()
    

    posicaoXPersona = 400
    posicaoYPersona = 300
    movimentoXPersona  = 0
    movimentoYPersona  = 0
    posicaoXKi = 400
    posicaoYKi = -240
    velocidadeKi = 50
    pygame.mixer.Sound.play(kiSound)
    pygame.mixer.music.play(-1)
    pontos = 0
    nivel_goku = 0
    larguraPersona = 50
    alturaPersona = 50
    larguaKi  = 50
    alturaKi  = 250
    dificuldade  = 30
    nivel_anterior = -1
    vidas = 3
    animando_transformacao = False
    indice_frame = 0
    tempo_ultimo_frame = 0
    fps_animacao = 15
    transformacao_atual = 0
    pause = False
    raio_sol = 100
    direcao_pulso = 1
    posicaoXObjeto = 0
    posicaoYObjeto = 20  # posição no topo da tela
    velocidadeObjeto = 5

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    pause = not pause  # alterna pausa/despausa
                    

        if pause:
            # Cria uma superfície transparente do tamanho da tela
            overlay = pygame.Surface(tamanho)
            overlay.set_alpha(180)  # Transparência (0 totalmente transparente, 255 opaco)
            overlay.fill((50, 50, 50))  # Cor cinza escuro
            
            # Desenha a superfície transparente sobre a tela
            tela.blit(overlay, (0, 0))
            
            # Desenha o texto de pausa sobre o overlay
            texto_pausa = fonteMenu.render("Jogo Pausado - Pressione SPACE para continuar", True, (0, 0, 0))
            tela.blit(texto_pausa, (tamanho[0] // 2 - texto_pausa.get_width() // 2, tamanho[1] // 2 - texto_pausa.get_height() // 2))
            
            pygame.display.update()
            relogio.tick(15)
            continue

        # Aqui a parte nova que substitui o controle via eventos KEYDOWN/KEYUP
        teclas = pygame.key.get_pressed()
        movimentoXPersona = 0
        movimentoYPersona = 0

        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            movimentoXPersona = 15
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            movimentoXPersona = -15
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_RIGHT]:
            movimentoXPersona = 15
        if teclas[pygame.K_LEFT] or teclas[pygame.K_LEFT]:
            movimentoXPersona = -15 

        # Atualiza o nível e seleciona o sprite correspondente
        nivel_goku = pontos // 25
        if nivel_goku >= len(goku_niveis):
            nivel_goku = len(goku_niveis) - 1

        if nivel_goku != nivel_anterior:
            pygame.mixer.Sound.play(transformSound)
            nivel_anterior = nivel_goku    

        goku = goku_niveis[nivel_goku]

        sprite_largura = goku.get_width()
        sprite_altura = goku.get_height()

        posicaoXPersona += movimentoXPersona
        posicaoYPersona += movimentoYPersona

        if posicaoXPersona < 0:
            posicaoXPersona = 0
        elif posicaoXPersona > tamanho[0] - sprite_largura:
            posicaoXPersona = tamanho[0] - sprite_largura

        if posicaoYPersona < 0:
            posicaoYPersona = 0
        elif posicaoYPersona > tamanho[1] - sprite_altura:
            posicaoYPersona = tamanho[1] - sprite_altura

        posicaoXObjeto += velocidadeObjeto * direcaoObjeto

        if posicaoXObjeto + objeto_largura >= tamanho[0]:
            direcaoObjeto = -1  # Inverter direção para esquerda
        elif posicaoXObjeto <= 0:
            direcaoObjeto = 1  # Inverter direção para direita

        if posicaoXObjeto + objeto_largura >= tamanho[0]:
            direcaoObjeto = -1  # vira pra esquerda

        elif posicaoXObjeto <= 0:
            direcaoObjeto = 1  # vira pra direita

        # Desenha o objeto
        tela.blit(imagem_objeto, (posicaoXObjeto, posicaoYObjeto))

        tela.fill(branco)
        tela.blit(fundoJogo, (0,0) )
        tela.blit(imagem_objeto, (posicaoXObjeto, posicaoYObjeto))
                # Atualiza o tamanho do sol (efeito de pulsação)
        raio_sol += direcao_pulso * 0.5
        if raio_sol >= 100:
            direcao_pulso = -1
        elif raio_sol <= 60:
            direcao_pulso = 1

        # Desenha o sol
        pygame.draw.circle(tela, (255, 255, 0), (150, 150), int(raio_sol))

            # Desenha as vidas (corações) no topo direito
        for i in range(vidas):
            x_pos = tamanho[0] - (i + 1) * (coracao_img.get_width() + 10)
            y_pos = 10
            tela.blit(coracao_img, (x_pos, y_pos))

        nivel_goku = pontos // 20  # Sobe de nível a cada 20 pontos
        if nivel_goku >= len(goku_niveis):
            nivel_goku = len(goku_niveis) - 1

        # Atualiza a imagem do Goku
        goku = goku_niveis[nivel_goku]

        # Desenha o Goku na tela (adicionar esta linha)
        tela.blit(goku, (posicaoXPersona, posicaoYPersona))

        
        posicaoYKi = posicaoYKi + velocidadeKi
        if posicaoYKi > 700:
            posicaoYKi = -240
            pontos = pontos + 1
            velocidadeKi = velocidadeKi + 0.5
            posicaoXKi = random.randint(0,1000)
            pygame.mixer.Sound.play(kiSound)
            
            
        tela.blit( ki, (posicaoXKi, posicaoYKi) )
        
        texto = fonteMenu.render("Pontos: "+str(pontos), True, preto)
        tela.blit(texto, (15,15))

        texto_pausa = fonteMenu.render("Press Space to Pause Game", True, preto)
        # Posiciona um pouco à direita do texto dos pontos (por exemplo, 150 pixels depois)
        tela.blit(texto_pausa, (15 + texto.get_width() + 20, 15))
        
        # Cria retângulos para o Goku e o míssil (use as medidas reais da imagem)
        rect_goku = pygame.Rect(posicaoXPersona, posicaoYPersona, 200, 200)  # tamanho do goku_niveis (200x200)
        rect_missil = pygame.Rect(posicaoXKi, posicaoYKi, 80, 80)   # tamanho do ki (80x80)

        if rect_goku.colliderect(rect_missil):
            vidas -= 1
            if vidas <= 0:
                escreverDados(nome, pontos)
                dead()
            else:
                # Resetar posição do míssil e talvez tocar um som de dano
                posicaoYKi = -240
                posicaoXKi = random.randint(0, tamanho[0] - ki.get_width())
                pygame.mixer.Sound.play(explosaoSound)  # opcional: som de dano
                        
        else:
                print("Ainda Vivo, mas por pouco!")

        
        pygame.display.update()
        relogio.tick(60)


def start():
    larguraButton = 300
    alturaButton = 100

    x_central = (tamanho[0] - larguraButton) // 2
    y_inicio = (tamanho[1] - alturaButton) // 2
    y_espaco = 20  # Espaço entre os botões
        

    while True:
        for evento in pygame.event.get():
            
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 140
                    alturaButtonStart  = 35
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 140
                    alturaButtonQuit  = 35

                
            elif evento.type == pygame.MOUSEBUTTONUP:
                # Verifica se o clique foi dentro do retângulo
                if startButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonStart = 150
                    alturaButtonStart  = 40
                    jogar()
                if quitButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonQuit = 150
                    alturaButtonQuit  = 40
                    quit()
                    
            
            
        tela.fill(branco)
        tela.blit(fundoStart, (0,0) )

        startTexto = fonteMenu.render("Jogar", True, preto)
        startButton = pygame.draw.rect(tela, branco, (x_central, y_inicio, larguraButton, alturaButton), border_radius=15)
        tela.blit(startTexto, (
            x_central + (larguraButton - startTexto.get_width()) // 2,
            y_inicio + (alturaButton - startTexto.get_height()) // 2
        ))

        quitTexto = fonteMenu.render("Sair", True, preto)
        quitButton = pygame.draw.rect(tela, branco, (x_central, y_inicio + alturaButton + y_espaco, larguraButton, alturaButton), border_radius=15)
        tela.blit(quitTexto, (
            x_central + (larguraButton - quitTexto.get_width()) // 2,
            y_inicio + alturaButton + y_espaco + (alturaButton - quitTexto.get_height()) // 2
        ))
                
        pygame.display.update()
        relogio.tick(60)


def dead():
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(explosaoSound)

    larguraButtonStart = 150
    alturaButtonStart  = 40
    larguraButtonQuit = 150
    alturaButtonQuit  = 40
    
    # Carregar dados do log
    try:
        with open("base.atitus", "r") as arquivo:
            log_partidas = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        log_partidas = {}

    # Pega os últimos 5 registros (os últimos inseridos)
    ultimos_registros = list(log_partidas.items())[-5:]

    fonte_titulo = pygame.font.SysFont("arial", 50)
    fonte_log = pygame.font.SysFont("comicsans", 28)
    fonte_botao = pygame.font.SysFont("comicsans", 25)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 140
                    alturaButtonStart  = 35
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 140
                    alturaButtonQuit  = 35

            elif evento.type == pygame.MOUSEBUTTONUP:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 150
                    alturaButtonStart  = 40
                    jogar()
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 150
                    alturaButtonQuit  = 40
                    quit()

        tela.fill(branco)
        tela.blit(fundoDead, (0,0))

        # Título
        titulo = fonte_titulo.render("Dados de Partida (Últimos 5)", True, preto)
        tela.blit(titulo, ((tamanho[0] - titulo.get_width()) // 2, 30))

        # Mostrar os registros
        y_offset = 120
        for i, (nome, dados) in enumerate(ultimos_registros):
            texto = f"{i+1}. {nome} - {dados['pontos']} pontos - {dados['data_hora']}"
            texto_renderizado = fonte_log.render(texto, True, preto)
            tela.blit(texto_renderizado, (50, y_offset))
            y_offset += 40

        # Botões
        startButton = pygame.draw.rect(tela, branco, (10,10, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonte_botao.render("Iniciar Game", True, preto)
        tela.blit(startTexto, (25,12))
        
        quitButton = pygame.draw.rect(tela, branco, (10,60, larguraButtonQuit, alturaButtonQuit), border_radius=15)
        quitTexto = fonte_botao.render("Sair do Game", True, preto)
        tela.blit(quitTexto, (25,62))

        pygame.display.update()
        relogio.tick(60)


start()

