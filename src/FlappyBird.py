import pygame
import sys
import random
from pygame.locals import *
from pygame import Rect, init, time, display
from pygame.event import pump
from pygame.image import load
from pygame.surfarray import array3d, pixels_alpha


class FlappyBird():
    
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

        def update(self, flying, gameOver, action):
            if flying == True:
                THRESHOLD = 8
                self.vel += 0.5
                if self.vel > THRESHOLD:
                    self.vel = THRESHOLD
                if self.rect.bottom < 768:
                    self.rect.y += int(self.vel)

            if gameOver == False:
                # jump:  pygame.mouse.get_pressed()[0] == 1 | action == 1 
                if action == 1 and self.clicked == False:
                    self.clicked = True
                    self.vel = -10
                if action == 0:
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
            self.PIPE_GAP = 100
            self.SCROLL_SPEED = 4
            # poistion 1 from top, -1 from the bottom
            if position == 1:
                self.image = pygame.transform.flip(self.image, False, True)
                self.rect.bottomleft = [x, y - self.PIPE_GAP]
            else:
                self.rect.topleft = [x, y + self.PIPE_GAP]

        def update(self):
            self.rect.x -= self.SCROLL_SPEED
            if self.rect.right < 0:
                self.kill()

    class Button():
        def __init__(self, x, y, image):
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)

        def draw(self, screen):
            action = False

            pos = pygame.mouse.get_pos()

            if self.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1:
                    action = True
            screen.blit(self.image, (self.rect.x, self.rect.y))

            return action

    def __init__(self) -> None:
        pygame.init()
        self.flying = False
        self.gameOver = False
        self.score = 0
        

        self.SCREEN_HEIGHT = 514
        self.SCREEN_WIDTH = 288 
        self.PIPE_FREQUENCY = 1500 #ms
        self.SCROLL_SPEED = 4

        self.lastPipe = pygame.time.get_ticks()
        self.fps = 30

        self.font = pygame.font.SysFont('Bauhaus 93', 60)
        self.textColor = (255, 255, 255)

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Flappy Bird")

        self.background = pygame.image.load('img/bg.png') #sky
        self.ground = pygame.image.load('img/ground.png')

        #Image = pygame.image.load('img/restart.png')

        self.groundScroll = 0

        self.clock = pygame.time.Clock()

        self.passPipe = False
        
        self.birdGroup = pygame.sprite.Group()
        self.pipeGroup = pygame.sprite.Group()

        self.flappyBird = self.Bird(100, int(self.SCREEN_HEIGHT / 2))
        self.birdGroup.add(self.flappyBird)

        #self.Button = self.Button(self.SCREEN_WIDTH // 2 - 50, self.SCREEN_HEIGHT // 2 - 100, self.ButtonImage)

    def drawText(self, text, font, textColor, x, y):
        img = self.font.render(text, True, self.textColor)
        self.screen.blit(img, (x, y))

    def resetGame(self):
        self.pipeGroup.empty()
        self.birdGroup.empty()

        self.flappyBird = self.Bird(100, int(self.SCREEN_HEIGHT / 2))
        self.birdGroup.add(self.flappyBird)
        #self.flappyBird.change()
        return 0

    def play(self, action):
        reward = 0.1
        done = False
        self.clock.tick(self.fps)

        self.screen.blit(self.background, (0,0))

        self.birdGroup.draw(self.screen)
        self.birdGroup.update(self.flying, self.gameOver, action)

        self.pipeGroup.draw(self.screen)
        

        self.screen.blit(self.ground, (self.groundScroll,self.SCREEN_HEIGHT * 0.90))

        if len(self.pipeGroup) >  0:
            if self.birdGroup.sprites()[0].rect.left > self.pipeGroup.sprites()[0].rect.left \
                and self.birdGroup.sprites()[0].rect.right < self.pipeGroup.sprites()[0].rect.right \
                and self.passPipe == False:
                    self.passPipe = True
            if self.passPipe == True:
                if self.birdGroup.sprites()[0].rect.right > self.pipeGroup.sprites()[0].rect.right:
                    self.passPipe = False
                    self.score += 1
                    reward = 1

        self.drawText(str(self.score), self.font, self.textColor, int(self.SCREEN_WIDTH / 2), 20)

        if self.flappyBird.rect.bottom >= self.SCREEN_HEIGHT * 0.90 or self.flappyBird.rect.top <= 0\
            or pygame.sprite.groupcollide(self.birdGroup, self.pipeGroup, False, False):
            self.gameOver = True
            self.flying = False
            reward = -1

        if self.gameOver == False and self.flying == True:
            # Generate pipe
            timeNow = pygame.time.get_ticks()
            if timeNow - self.lastPipe > self.PIPE_FREQUENCY:
                pipeHeight = random.randint(-60, 60)
                bottomPipe = self.Pipe(self.SCREEN_WIDTH, int(self.SCREEN_HEIGHT / 2) + pipeHeight, -1)
                topPipe = self.Pipe(self.SCREEN_WIDTH, int(self.SCREEN_HEIGHT / 2) + pipeHeight, 1)
                self.pipeGroup.add(bottomPipe)
                self.pipeGroup.add(topPipe)
                self.lastPipe = timeNow
            # Scroll the self.ground
            self.groundScroll -= self.SCROLL_SPEED
            if abs(self.groundScroll) > 35:
                self.groundScroll = 0
            self.pipeGroup.update()

        if self.gameOver == True:
            done = True
            #if self.Button.draw(self.screen): # this is for normal flappy bird
            self.score = self.resetGame()     
            self.gameOver = False
            self.flying = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if self.flying == False and self.gameOver == False: # event.type == pygame.MOUSEBUTTONDOWN and 
                self.flying = True
        
        pygame.display.update()
        image = array3d(pygame.display.get_surface())

        return image, reward, done

# flap = FlappyBird()

# while True:
#     rand = random.randint(0,1)
#     flap.play(rand)