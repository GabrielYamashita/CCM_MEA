# Imports de Bibliotecas
import re
import sys
import pygame
import keyboard
import serial
import time


# Cores da Tela
# Tela 
backgroundColor = (20, 28, 77)

# Cores da Caixa de Texto
textTextColor = (255, 255, 255)
textTitleColor = (50,50,50)

# Cores RPM
textTextColorRPM = backgroundColor
textTitleColorRPM = (211, 211, 211)

# Cores do Botão:
#Cores Normal
buttonTextColor = backgroundColor
buttonNormalColor = (255, 255, 255)
buttonHoverColor = (102, 102, 102)
buttonPressedColor = (51, 51, 51)

# Cores Emergência
buttonTextColorEmerg = (255, 255, 255)
buttonNormalColorEmerg = (255, 0, 0)
buttonHoverColorEmerg = (102, 0, 0)
buttonPressedColorEmerg = (51, 0, 0)


# Configurações da Tela do Pygame
pygame.init()

ratio = 2/3 # Resize do Tamanho da Tela
screen = pygame.display.set_mode((1920*ratio, 1080*ratio)) # Cria a Tela do Pygame
screen.fill(backgroundColor) # Cor de Fundo
clock = pygame.time.Clock() # Define o Clock

font = pygame.font.SysFont("Verdana", 18) # Define a Fonte e Tamanho


# Classe da Caixa de Texto
class Text():
    def __init__(self, x, y, width, height, textText='Text', type='Title', trackVariable=None): # Método de Inicialização do Objeto
        self.x = x # Posição na Tela || x
        self.y = y # Posição na Tela || y
        self.width = width # Tamanho da Caixa || x
        self.height = height # Tamanho da Caixa || y
        self.textText = textText # Texto dentro da Caixa
        self.type = type.lower() # Define o Tipo de Caixa de Texto
        self.trackVariable = trackVariable # Variável para Rastrear a Velocidade

        self.fillColors = { # Dicinário de Cores
            'textTextTitle': textTextColor,
            'title': textTitleColor,

            'textRPM': textTextColorRPM,
            'rpm': textTitleColorRPM
        }

        # Inicialização da Caixa e seus Conteúdos
        self.textSurface = pygame.Surface((self.width, self.height))
        self.textRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.textSurf = font.render(self.textText, True, self.setColor()[1])

        # Adiciona o Objeto a Lista
        objects.append(self)

    def setColor(self): # Método de Mudar as Cores da Caixa de Texto
        text = ''
        if self.type == 'rpm': # Ve o Tipo de Caixa de Texto || RPM
            textT = self.fillColors['textRPM']
            normalT = self.fillColors['rpm']
            text = 'RPM'

        else: # Ve o Tipo de Caixa de Texto || Normal
            textT = self.fillColors['textTextTitle']
            normalT = self.fillColors['title']

        return text, textT, normalT # Retorna a Cor da Caixa de Texto

    def changeName(self, nome): # Muda o Nome do Texto com a Variável de Reastreamento
        if nome != None:
            self.textSurf = font.render(f'{str(nome)} {self.setColor()[0]}', True, self.setColor()[1]) # Substitui o Texto
    def process(self): # Método para Executar a Caixa de Texto
        self.changeName(self.trackVariable) # Substitui a o Texto da Caixa de Texto

        self.textSurface.fill(self.setColor()[2]) # Substitui a Cor de Acordo com o Tipo de Texto

        self.textSurface.blit(self.textSurf, [ # Desenha a Caixa de Texto
            self.textRect.width/2 - self.textSurf.get_rect().width/2,
            self.textRect.height/2 - self.textSurf.get_rect().height/2,
        ])

        screen.blit(self.textSurface, self.textRect)


# Classe da Caixa de Botão
class Button():
    def __init__(self, x, y, width, height, comando, buttonText='Button', onClickFunction=None, onePress=False, type='Normal'):
        self.x = x # Posição na Tela || x
        self.y = y # Posição na Tela || y
        self.width = width # Tamanho da Caixa || x
        self.height = height # Tamanho da Caixa || y
        self.type = type.lower() # Define o Tipo de Caixa de Texto

        self.comando = comando # Recebe o Carácter, para ser Enviado pela Serial

        self.onClickFunction = onClickFunction # Recebe a Função a ser Executada, quando Pressionado
        self.onePress = onePress # Função de Múltiplos Cliques, ou Somente Um
        self.alreadyPressed = False # Flag para Checar se ja foi Clicado

        self.fillColors = { # Dicinário de Cores
            'textNormal': buttonTextColor,
            'normal': buttonNormalColor,
            'hover': buttonHoverColor,
            'pressed': buttonPressedColor,

            'textEmerg': buttonTextColorEmerg,
            'normalEmerg': buttonNormalColorEmerg,
            'hoverEmerg': buttonHoverColorEmerg,
            'pressedEmerg': buttonPressedColorEmerg
        }

        # Inicialização da Caixa e seus Conteúdos
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.buttonSurf = font.render(buttonText, True, self.setColor()[0])

        # Adiciona o Objeto a Lista
        objects.append(self)

    def setColor(self): # Método de Mudar as Cores da Caixa de Texto
        if self.type == 'emerg': # Ve o Tipo de Botão || Emergência
            textB = self.fillColors['textEmerg']
            normalB = self.fillColors['normalEmerg']
            hoverB = self.fillColors['hoverEmerg']
            pressedB = self.fillColors['pressedEmerg']

        else: # Ve o Tipo de Botão || Normal
            textB = self.fillColors['textNormal']
            normalB = self.fillColors['normal']
            hoverB = self.fillColors['hover']
            pressedB = self.fillColors['pressed']

        return textB, normalB, hoverB, pressedB # Retorna a Cor do Botão

    def process(self): # Método para Executar a Caixa de Texto
        mousePos = pygame.mouse.get_pos() # Recebe a Posição do Mouse
        self.buttonSurface.fill(self.setColor()[1]) # Colore com a Cor do Botão Normal

        if self.buttonRect.collidepoint(mousePos): # Checa se o Mouse está em cima do Botão
            self.buttonSurface.fill(self.setColor()[2]) # Colore com a Cor do Botão Hover

            if pygame.mouse.get_pressed(num_buttons=3)[0]: # Checa se o Botão Foi Clicado
                self.buttonSurface.fill(self.setColor()[3]) # Colore com a Cor do Botão Pressed

                if self.onePress: # Múltiplos Cliques
                    self.onClickFunction(self.comando) # Executa o Comando

                elif not self.alreadyPressed: # Um Clique
                    self.onClickFunction(self.comando) # Executa o Comando
                    self.alreadyPressed = True
                
            else: # Botão não Pressionado
                self.alreadyPressed = False

        self.buttonSurface.blit(self.buttonSurf, [ # Desenha a Caixa de Texto
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2,
        ])

        screen.blit(self.buttonSurface, self.buttonRect)


# Função para Mandar Comando para a Serial
def comandoSerial(comando):
    # Comando Recebido pela Tela
    print(f'\nComando "{comando}" efetuado.')
    ser.write(f"{comando}".encode('utf8'))

    time.sleep(0.15) # Espera para Chegar a Mensagem da Serial

    # Recebe a Mensagem da Núcleo pela Serial
    receive = ser.readline()
    receive = receive.decode('utf8').replace("\r", "").replace("\n", "")
    print(receive)

    if comando in ['<', '>', '-', '+']: # Checa se os Botões de Velocidade foram Pressionados
        result = re.findall(r"\((.*?)\)", receive)[0] # Recebe a Velocidade Atual do Motor
        if comando in ['<', '>']: # Velocidade do Motor A
            RPMA.trackVariable = result # Recebe a Velocidade Atual como Variável para Rastrear

        elif comando in ['-', '+']: # Velocidade do Motor A
            RPMB.trackVariable = result # Recebe a Velocidade Atual como Variável para Rastrear

# Variáveis
RPM1, RPM2 = 150, 150 # Velocidades de Início
Rot1, Rot2 = 10, 10 # Número de Rotações de Início

# Criação de Botões na Tela
objects = []


# Motor A:
Text(50, 60, 284, 50, 'Motor A')
Button(50, 120, 284, 73, 'e', 'Enable A', comandoSerial)
Button(50, 229, 284, 73, 'd', 'Disable A', comandoSerial)
Button(50, 338, 284, 73, 'h', 'Horário A', comandoSerial)
Button(50, 447, 284, 73, 'a', 'Anti-horário A', comandoSerial)

# Velocidade A
Text(394, 120, 156, 50, 'Vel. [10 - 150]')
RPMA = Text(394, 180, 156, 75, '# RPM A', 'RPM', RPM1)
Button(394, 270, 68, 55, '<', '-', comandoSerial)
Button(482, 270, 68, 55, '>', '+', comandoSerial)


# Motor B:
Text(715, 60, 284, 50, 'Motor B')
Button(715, 120, 284, 73, 'E', 'Enable B', comandoSerial)
Button(715, 229, 284, 73, 'D', 'Disable B', comandoSerial)
Button(715, 338, 284, 73, 'H', 'Horário B', comandoSerial)
Button(715, 447, 284, 73, 'A', 'Anti-horário B', comandoSerial)

# Velocidade B
Text(1059, 120, 156, 50, 'Vel. [10 - 150]')
RPMB = Text(1059, 180, 156, 75, '# RPM B', 'RPM', RPM2)
Button(1059, 270, 68, 55, '-', '-', comandoSerial)
Button(1147, 270, 68, 55, '+', '+', comandoSerial)
# Botão de Emergência:
Button(50, 570, 1180, 100, '!', 'Emergência', comandoSerial, False, 'emerg')


# Função Principal
def main():
    pygame.display.set_caption(f'(FPS: {int(clock.get_fps())}) Projeto - Centro de Controle de Motores') # Define o Título e Mostra o FPS

    for event in pygame.event.get(): # Checa pela Saída do Código
        if event.type == pygame.QUIT or keyboard.is_pressed('q'): # Se 'q' for Apertado Sai da Aplicação
            comandoSerial('q') # Manda 'q' pela Serial
            pygame.quit() # Fecha a Tela do Pygame
            sys.exit() # Sai do Interpretador

    for object in objects: # Checa o Estado dos Botões
        object.process() # Executa os Botões da Tela

    clock.tick(120) # Atualiza o Clock para 120 FPS
    pygame.display.flip() # Atualiza todo a Tela


# Comunicação com a Serial
port = 'COM4' # Porta de Comunicação
ser = serial.Serial(port, 9600, timeout=0) # Inícia a Porta Serial


# Loop Principal
firstTime = False # Checa se é a Primeira Vez
while True:
    if firstTime: # Checa se é a Primeira Vez Executando
        data = ser.readline() # Recebe a Primeira Leitura
        firstTime = False

    else: # Executa o main()
        main()