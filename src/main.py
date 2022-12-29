import pygame
import sys
import random
from pygame.locals import *

pygame.init()

SCREEN_HEIGHT = 936
SCREEN_WIDTH = 864 
PIPE_GAP = 75
PIPE_FREQUENCY = 1500 #ms
lastPipe = pygame.time.get_ticks()

font = pygame.font.SysFont('Bauhaus 93', 60)
textColor = (255, 255, 255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flap My Ass")

background = pygame.image.load('img/bg.png') #sky
ground = pygame.image.load('img/ground.png')

buttonImage = pygame.image.load('img/restart.png')

SCROLL_SPEED = 4  
groundScroll = 0

clock = pygame.time.Clock()
fps = 60
flying = False
gameOver = False

score = 0
passPipe = False

def drawText(text, font, textColor, x, y):
    img = font.render(text, True, textColor)
    screen.blit(img, (x, y))

def resetGame():
    global score
    pipeGroup.empty()
    flappyBird.rect.x = 100
    flappyBird.rect.y = int(SCREEN_HEIGHT / 2)
    flappyBird.change()
    return 0

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            image = pygame.image.load(f'img/bird{num}.png')
            self.images.append(image)
        self.image =self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):
        if flying == True:
            THRESHOLD = 8
            self.vel += 0.5
            if self.vel > THRESHOLD:
                self.vel = THRESHOLD
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)

        if gameOver == False:
            # jump
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False 

            self.counter += 1
            flapCooldown = 5

            if self.counter > flapCooldown:
                self.counter = 0
                self.index = (self.index + 1) % 3
            self.image = self.images[self.index]

            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)
            
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f'img/pipe.png')
        self.rect = self.image.get_rect()
        # poistion 1 from top, -1 from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - PIPE_GAP]
        else:
            self.rect.topleft = [x, y + PIPE_GAP]

    def update(self):
        self.rect.x -= SCROLL_SPEED
        if self.rect.right < 0:
            self.kill()

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        action = False

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action
birdGroup = pygame.sprite.Group()
pipeGroup = pygame.sprite.Group()

flappyBird = Bird(100, int(SCREEN_HEIGHT / 2))
birdGroup.add(flappyBird)

button = Button(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 100, buttonImage)

while True:
    clock.tick(fps)

    screen.blit(background, (0,0))

    birdGroup.draw(screen)
    birdGroup.update()

    pipeGroup.draw(screen)
    

    screen.blit(ground, (groundScroll,768))

    if len(pipeGroup) >  0:
        if birdGroup.sprites()[0].rect.left > pipeGroup.sprites()[0].rect.left \
            and birdGroup.sprites()[0].rect.right < pipeGroup.sprites()[0].rect.right \
            and passPipe == False:
                passPipe = True
        if passPipe == True:
            if birdGroup.sprites()[0].rect.right > pipeGroup.sprites()[0].rect.right:
                passPipe = False
                score += 1
    drawText(str(score), font, textColor, int(SCREEN_WIDTH / 2), 20)
    if flappyBird.rect.top <= 0\
       or pygame.sprite.groupcollide(birdGroup, pipeGroup, False, False):
       gameOver = True

    if flappyBird.rect.bottom >= 768:
        gameOver = True
        flying = False

    if gameOver == False and flying == True:
        #print(len(pipeGroup))
        # Generate pipe
        timeNow = pygame.time.get_ticks()
        if timeNow - lastPipe > PIPE_FREQUENCY:
            pipeHeight = random.randint(-100, 100)
            bottomPipe = Pipe(SCREEN_WIDTH, int(SCREEN_HEIGHT / 2) + pipeHeight, -1)
            topPipe = Pipe(SCREEN_WIDTH, int(SCREEN_HEIGHT / 2) + pipeHeight, 1)
            pipeGroup.add(bottomPipe)
            pipeGroup.add(topPipe)
            lastPipe = timeNow
        # Scroll the ground
        groundScroll -= SCROLL_SPEED
        if abs(groundScroll) > 35:
            groundScroll = 0
        pipeGroup.update()

    if gameOver == True:
        if button.draw():
            score = resetGame()     
            gameOver = False
            flying = False
            
            #birdGroup.sprites()[0].image = birdGroup.sprites()[0].images[birdGroup.sprites()[0].index]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and gameOver == False:
            flying = True
    
    pygame.display.update()
