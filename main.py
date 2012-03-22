# coding=utf-8

"""

* File Name : main.py

* Created By : Natan Žabkar, natan.zabkar@gmail.com 

* Creation Date : 17-03-2012

* Last Modified : 22.3.2012 3:33:01

"""

from __future__ import division, print_function
import pygame, random, sys
from pygame.locals import *
from colors import *


# Constants
font_debug = False

def terminate():
    pygame.quit()
    sys.exit()

def normalFont(size, font_name = "menu_font"):

    if(font_debug):
        print("------------")
        print(size)
        print(pygame.font.Font("fonts/{0}.ttf".format(font_name), size).get_height())
        print(pygame.font.SysFont(None, size).get_height())
        print(pygame.font.Font("fonts/{0}.ttf".format(font_name), int(size * 0.54)).get_height())
    try:
        return pygame.font.Font("fonts/{0}.ttf".format(font_name), size * 0.54)
    except:
        return pygame.font.Font(None, size)

def drawText(text, font, surface, x, y, color):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)
    return textrect







##############################
#
#          LEVELS
#
##############################

class Game:
    class Tick(pygame.sprite.Sprite):
        def __init__(self, x, y, ticked, width = 2, size = 20):
            pygame.sprite.Sprite.__init__(self)
            self.ticked = ticked
            self.width = width
            self.size = size
            self.image = pygame.Surface((self.size, self.size))
            self.rect = self.image.get_rect()
            self.rect.center = (x,y)
            

        def read(self):
            pass
        
        def update(self):
            self.image.fill(WHITE)
            self.image.fill(BLACK, rect=(self.width, self.width, self.rect.width - 2*self.width, self.rect.height - 2*self.width))
            if(self.ticked):
                pygame.draw.line(self.image, WHITE, (0,0), (self.size, self.size), self.width)
                pygame.draw.line(self.image, WHITE, (0, self.size - 1), (self.size - 1, 0), self.width)



    def __init__(self, windowwidth, windowheight, endingLevel,
            gameFolder = "levels", startingLevel = 1,
            widthcheck = None, heightcheck = None,
            fps = 120, gravitation = 100,
            two_player = False, show_fps = False, ball_debug = False, dirty = False, caption = "Awesome game! :D", backgroundCount = 1):
        
        # Base game options
        self.windowwidth = windowwidth
        self.windowheight = windowheight
        self.gameFolder = gameFolder
        self.startingLevel = startingLevel
        self.endingLevel = endingLevel
        self.currentLevel = startingLevel

        # Extra game options
        if(widthcheck == None):
            self.widthcheck = windowwidth
        else:
            self.widthcheck = widthcheck
        if(heightcheck == None):
            self.heightcheck = windowheight
        else:
            self.heightcheck = heightcheck
        self.fps = fps
        self.gravitation = gravitation
        self.two_player = two_player
        self.backgroundCount = backgroundCount

        # Debug options
        self.show_fps = show_fps
        self.ball_debug = ball_debug
        self.dirty = dirty

        # Caption
        self.caption = caption

        # Score
        self.score = 0

    def startGame(self):
        self.setup()
        self.startMenu()

    def newGame(self):
        self.currentLevel = self.startingLevel
        self.gameReset()
        self.getReady()
        while True:
            self.levelReset()
            self.gameLoop()
            if(self.levelwon):
                self.currentLevel += 1
                if(self.currentLevel > self.endingLevel):
                    self.gameWon()
                    return True
                self.levelWon()
            elif(self.levellost):
                self.gameLost()
                return True
        

    def setup(self, reset = False):
        # Pygame stuff setup
        pygame.init()
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode((self.windowwidth, self.windowheight))
        pygame.display.set_caption(self.caption)
        self.background = pygame.image.load("images/background/{0}.png".format(random.randint(1,self.backgroundCount))).convert()

        if(self.dirty):
            self.surface.blit(self.background, (0,0))
            pygame.display.update()

        # Sprite groups
        if(self.dirty):
            self.playerGroup = pygame.sprite.RenderUpdates()
            self.ballGroup = pygame.sprite.RenderUpdates()
            self.arrowGroup = pygame.sprite.RenderUpdates()
        else:
            self.playerGroup = pygame.sprite.RenderPlain()
            self.ballGroup = pygame.sprite.RenderPlain()
            self.arrowGroup = pygame.sprite.RenderPlain()

        # Player setup
        if(not self.two_player):
            ply = Player(self, self.windowwidth//2, self.windowheight-50, 300, K_LEFT, K_RIGHT, K_SPACE)
            self.playerGroup.add(ply)
        else:
            ply = Player(self, 3 * self.windowwidth//4, self.windowheight-50, 300, K_LEFT, K_RIGHT, K_SPACE)
            self.playerGroup.add(ply)
            ply = Player(self, self.windowwidth//4, self.windowheight-50, 300, ord('a'), ord('d'), ord('1'), 2)
            self.playerGroup.add(ply)

    def levelReset(self):
        self.background = pygame.image.load("images/background/{0}.png".format(random.randint(1,self.backgroundCount))).convert()
        self.playerGroup.empty()
        self.ballGroup.empty()
        self.arrowGroup.empty()

        if(self.dirty):
            self.surface.blit(self.background, (0,0))
            pygame.display.update()

        if(not self.two_player):
            ply = Player(self, self.windowwidth//2, self.windowheight-50, 300, K_LEFT, K_RIGHT, K_SPACE)
            self.playerGroup.add(ply)
        else:
            ply = Player(self, 3 * self.windowwidth//4, self.windowheight-50, 300, K_LEFT, K_RIGHT, K_SPACE)
            self.playerGroup.add(ply)
            ply = Player(self, self.windowwidth//4, self.windowheight-50, 300, ord('a'), ord('d'), ord('1'), 2)
            self.playerGroup.add(ply)

    def gameReset(self):
        self.score = 0
        self.levelReset()

    def readLevel(self):
        
        def returnNum(foo):
            if(foo[0] == '*'):
                return_value = random.choice((-1,1))
                foo = foo[1:]
            else:
                return_value = 1
            if('(' in foo):
                foo = foo[1:-1]
                foo = foo.split(',')
                return_value *= random.randint(int(foo[0]), int(foo[1]))
            else:
                return_value *= int(foo)

            return return_value
        
#        name = "{0}/level{1}.lvl".format(self.gameFolder, self.currentLevel)
        with open("{0}/level{1}.lvl".format(self.gameFolder, self.currentLevel)) as f:
            for line in f:
                if(line[0] != '#'):
                    foo = line.split()
                    if(len(foo) == 8):
                        x = returnNum(foo[0])
                        y = returnNum(foo[1])
                        rad = returnNum(foo[2])
                        vx = returnNum(foo[3])
                        vy = returnNum(foo[4])
                        color = foo[5]
                        split_times = returnNum(foo[6])
                        split_into = returnNum(foo[7])
                        if(self.ball_debug):
                            print("------------------")
                            print("x: {0}".format(x))
                            print("y: {0}".format(y))
                            print("rad: {0}".format(rad))
                            print("vx: {0}".format(vx))
                            print("vy: {0}".format(vy))

                        ball = Ball(self, x, y, rad, vx, vy, color, split_times, split_into)
                        self.ballGroup.add(ball)

    def waitForPlayerKeypress(self, continueKey, endKey = K_ESCAPE):
        while True:
            for event in pygame.event.get():
                if(event.type == QUIT):
                    terminate()
                elif(event.type == KEYDOWN):
                    if(event.key == K_ESCAPE):
                        terminate()
                    elif(event.key == continueKey):
                        return True
                    elif(event.key == endKey):
                        terminate()
                    if(continueKey == "any"):
                        return True
                elif(event.type == MOUSEBUTTONDOWN):
                    if(continueKey == "any" or continueKey == "mouse"):
                        return True

    def gameLoop(self):
        self.levelwon = False
        self.levellost = False
        self.continue_playing = True
        self.readLevel()
        if(self.show_fps):
            count = 0
        self.clock.tick()
        while self.continue_playing:
            #print("Playing... playing...!")
            time = self.clock.tick(self.fps)
            if(self.show_fps):
                count += time
                if(count >= 1000):
                    print(self.clock.get_fps())
                    count = 0
            for event in pygame.event.get():
                if(event.type == QUIT):
                    terminate()
                elif(event.type == KEYDOWN):
                    if(event.key == K_ESCAPE):
                        terminate()
                    elif(event.key == ord('f')):
                        count = 0
                        self.show_fps = not self.show_fps
                    for ply in self.playerGroup:
                        if(event.key == ply.leftKey):
                            ply.left = True
                        elif(event.key == ply.rightKey):
                            ply.right = True
                        elif(event.key == ply.shootingKey):
                            ply.shooting = True
                elif(event.type == KEYUP):
                    for ply in self.playerGroup:
                        if(event.key == ply.leftKey):
                            ply.left = False
                        elif(event.key == ply.rightKey):
                            ply.right = False
                        elif(event.key == ply.shootingKey):
                            ply.shooting = False
            

            # Update all groups
            self.ballGroup.update(time/1000)
            self.playerGroup.update(time/1000)
            self.arrowGroup.update(time/1000)

            # Drawing
            
            if(self.dirty):
                rect1 = self.playerGroup.draw(self.surface)
                rect2 = self.ballGroup.draw(self.surface)
                rect3 = self.arrowGroup.draw(self.surface)

                pygame.display.update(rect1 + rect2 + rect3)
                self.playerGroup.clear(self.surface, self.background)
                self.ballGroup.clear(self.surface, self.background)
                self.arrowGroup.clear(self.surface, self.background)
            else:
                self.surface.blit(self.background, (0, 0))
                self.playerGroup.draw(self.surface)
                self.ballGroup.draw(self.surface)
                self.arrowGroup.draw(self.surface)
                pygame.display.update()

    ##############################
    #
    #    DIFFERENT MENU PAGES
    #
    ##############################


    def startMenu(self):
        repeat = False
        while_loop = True
        self.surface.fill(BLACK)
        newgame_rect = drawText("New game", normalFont(60), self.surface, self.windowwidth//2, 1/4 * self.windowheight, WHITE)
        instructions_rect = drawText("Instructions", normalFont(60), self.surface, self.windowwidth//2, 5/12 * self.windowheight, WHITE)
        options_rect = drawText("Options", normalFont(60), self.surface, self.windowwidth//2, 7/12 * self.windowheight, WHITE)
        quit_rect = drawText("Quit", normalFont(60), self.surface, self.windowwidth//2, 3/4 * self.windowheight, WHITE)
        pygame.display.update()
        while while_loop:
            for event in pygame.event.get():
                if(event.type == QUIT):
                    terminate()
                elif(event.type == KEYDOWN):
                    if(event.key == K_ESCAPE):
                        terminate()
                    elif(event.key == K_SPACE):
                        if(self.newGame()):
                            repeat = True
                            while_loop = False
                elif(event.type == MOUSEBUTTONDOWN):
                    if(event.button == 1):
                        if(newgame_rect.collidepoint(event.pos)):
                            if(self.newGame()):
                                repeat = True
                                while_loop = False
                        elif(instructions_rect.collidepoint(event.pos)):
                            self.instructions()
                            repeat = True
                            while_loop = False
                        elif(options_rect.collidepoint(event.pos)):
                            self.options()
                            repeat = True
                            while_loop = False
                        elif(quit_rect.collidepoint(event.pos)):
                            terminate()
        if(repeat):
            self.startMenu()

    def instructions(self):
        base = self.windowheight//2 - 77
        add = 0
        self.surface.fill(BLACK)
        tmprect = drawText("Use arrow keys to move", normalFont(40, None), self.surface, self.windowwidth//2, base + add, WHITE)
        add += 1.5 * tmprect.height
        tmprect = drawText("and space to shoot.", normalFont(40), self.surface, self.windowwidth//2, base + add, WHITE)
        add += 1.5 * tmprect.height
        tmprect = drawText("Destroy all balls while dodging them!", normalFont(40), self.surface, self.windowwidth//2, base + add, WHITE)
        add += 1.5 * tmprect.height
        tmprect = drawText("Careful, you can't move and shoot at the same time ...", normalFont(40), self.surface, self.windowwidth//2, base + add, WHITE)
        pygame.display.update()
        self.waitForPlayerKeypress("any")

    def options(self):
        self.surface.fill(BLACK)
        tickGroup = pygame.sprite.RenderPlain()
        tickGroup.add(self.Tick(300,300,False))
        tickGroup.add(self.Tick(500,500,True))

        tickGroup.update()
        tickGroup.draw(self.surface)
        print(tickGroup)
        pygame.display.update()
        self.waitForPlayerKeypress("any")

    ##############################
    #
    #  DIFFERENT "POPUP" SCREENS
    #
    ##############################

    def gameWon(self):
        base = self.windowheight//2
        add = 0
        self.surface.fill(BLACK)
        tmprect = drawText("You won the game!", normalFont(80), self.surface, self.windowwidth//2, base + add, WHITE)
        add = 100
        tmprect = drawText("Press any key ... ", normalFont(20), self.surface, self.windowwidth//2, base + add, WHITE)
        pygame.display.update()
        self.waitForPlayerKeypress("any")

    def gameLost(self):
        base = self.windowheight//2
        add = 0
        self.surface.fill(BLACK)
        tmprect = drawText("You lost ... :(", normalFont(80), self.surface, self.windowwidth//2, base + add, WHITE)
        add = 100
        tmprect = drawText("Press any key ... ", normalFont(20), self.surface, self.windowwidth//2, base + add, WHITE)
        pygame.display.update()
        self.waitForPlayerKeypress("any")

    def levelWon(self):
        base = self.windowheight//2
        add = 0
        self.surface.fill(BLACK)
        tmprect = drawText("Level won!", normalFont(80), self.surface, self.windowwidth//2, base + add, WHITE)
        add += 80
        tmprect = drawText("Only {0} levels to go".format(self.endingLevel - self.currentLevel + 1), normalFont(30), self.surface, self.windowwidth//2, base + add, WHITE)
        add += 20
        tmprect = drawText("Press any key ... ", normalFont(20), self.surface, self.windowwidth//2, base + add, WHITE)
        pygame.display.update()
        self.waitForPlayerKeypress("any")

    def getReady(self):
        base = self.windowheight//2
        add = 0
        self.surface.fill(BLACK)
        tmprect = drawText("Get ready!", normalFont(80), self.surface, self.windowwidth//2, base + add, WHITE)
        add = 100
        tmprect = drawText("Press any key ... ", normalFont(20), self.surface, self.windowwidth//2, base + add, WHITE)
        pygame.display.update()
        self.waitForPlayerKeypress("any")


##############################
#
#          CLASSES
#
##############################

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y, speed, leftKey, rightKey, shootingKey, player_number = 1):
        pygame.sprite.Sprite.__init__(self)
        if(player_number == 1):
            self.image_left = pygame.image.load("images/player/ply1l.png")
            self.image_right = pygame.image.load("images/player/ply1r.png")
            self.image_normal = pygame.image.load("images/player/ply1n.png")
            self.image_shooting = pygame.image.load("images/player/ply1s.png")
        else:
            self.image_left = pygame.image.load("images/player/ply2l.png")
            self.image_right = pygame.image.load("images/player/ply2r.png")
            self.image_normal = pygame.image.load("images/player/ply2n.png")
            self.image_shooting = pygame.image.load("images/player/ply2s.png")

        self.game = game
        self.image = self.image_normal
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        self.speed = speed
        self.vx = 0
        self.leftKey = leftKey
        self.rightKey = rightKey
        self.shootingKey = shootingKey
        self.move = 0
        self.shooting = False
        self.arrow = None
        self.shooting_speed = 300
        self.left = False
        self.right = False

    def update(self, time):
        if(self.left == self.right):
            self.vx = 0
        elif(self.left):
            self.vx = -1
        elif(self.right):
            self.vx = 1
        if(self.shooting):
            self.image = self.image_shooting
        elif(self.vx < 0):
            self.image = self.image_left
        elif(self.vx > 0):
            self.image = self.image_right
        elif(self.vx == 0):
            self.image = self.image_normal

        if(not self.shooting):
            self.move += self.speed * self.vx * time
            if(self.move > 1 or self.move < 1):
                # Check if out of bounds
                # Left
                if(self.rect.left + int(self.move) >= 0):
                    self.rect.move_ip(int(self.move), 0)
                    self.move -= int(self.move)
                else:
                    self.rect.left = 0
                    self.move = 0
                # Right
                if(self.rect.right + int(self.move) <= self.game.widthcheck):
                    self.rect.move_ip(int(self.move), 0)
                    self.move -= int(self.move)
                else:
                    self.rect.right = self.game.widthcheck
                    self.move = 0

        if(self.hitBalls(self.game.ballGroup)):
            self.kill()
            if(not self.game.playerGroup):
                self.game.levellost = True
                self.game.continue_playing = False
#                terminate()
        if(self.shooting and self.arrow == None):
            self.shoot()
        if(not self.shooting and self.arrow != None):
            self.shoot_stop()

    def hitBalls(self, balls):
        for b in balls:
#            if self.rect.colliderect(b.rect):
            if(pygame.sprite.collide_mask(self, b)):
                return True
        return False

    def shoot(self):
        self.arrow = Arrow(self.game, self, self.rect.centerx, self.rect.top, 5, self.shooting_speed, BLACK)
        self.game.arrowGroup.add(self.arrow)

    def shoot_stop(self):
        self.arrow.kill()
        self.arrow = None

class Arrow(pygame.sprite.Sprite):

    def __init__(self, game, player, x, y, width, vy, color):
        pygame.sprite.Sprite.__init__(self)

        self.game = game
        self.player = player
        self.x = x
        self.y = y
        self.image = pygame.Surface((width, 1))
        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.x, self.y)
        self.mask = pygame.mask.from_surface(self.image, 0)
        self.mask.fill()
        self.vy = vy
        self.movey = 0

    def update(self, time):
        self.movey += time * self.vy
        if(self.rect.top - int(self.movey) < 0):
            self.player.shoot_stop()
        else:
            self.image = pygame.Surface((self.rect.width, self.rect.height + int(self.movey)))
            self.image.fill(BLACK)
            self.movey -= int(self.movey)
            self.rect = self.image.get_rect()
            self.rect.midbottom = (self.x, self.y)
            self.mask = pygame.mask.from_surface(self.image, 0)
            self.mask.fill()
            self.hitBalls(self.game.ballGroup)

    def hitBalls(self, balls):
        for b in balls:
#            if self.rect.colliderect(b.rect):
            if(pygame.sprite.collide_mask(self, b)):
                self.player.shoot_stop()
                b.split()
                return True
        return False

class Ball(pygame.sprite.Sprite):
    image_red = pygame.image.load("images/ball/red.png")
    image_green = pygame.image.load("images/ball/green.png")
    image_blue = pygame.image.load("images/ball/blue.png")

    def __init__(self, game, x, y, rad, vx, vy, color, split_times, split_into):
        pygame.sprite.Sprite.__init__(self)
       
        self.game = game

        self.xchange = 100
        self.ychange = 200

        self.vx = vx
        self.vy = vy
        self.movex = 0
        self.movey = 0
        self.rad = rad
        self.color = color
        self.split_times = split_times
        self.split_into = split_into

        if(self.color == "red"):
            self.image = pygame.transform.scale(Ball.image_red, (2 * self.rad, 2 * self.rad))
        elif(self.color == "green"):
            self.image = pygame.transform.scale(Ball.image_green, (2 * self.rad, 2 * self.rad))
        elif(self.color == "blue"):
            self.image = pygame.transform.scale(Ball.image_blue, (2 * self.rad, 2 * self.rad))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self, time):
        self.vy += time * self.game.gravitation
        self.move(time * self.vx, time * self.vy)
        if(self.game.ball_debug):
            print("------------------")
            print("x: {0}".format(self.rect.centerx))
            print("y: {0}".format(self.rect.centery))
            print("vx: {0}".format(self.vx))
            print("vy: {0}".format(self.vy))

    def move(self, x, y):
        self.movex += x
        self.movey += y

        self.rect.move_ip(int(self.movex), int(self.movey))
        self.movex -= int(self.movex)
        self.movey -= int(self.movey)
        # Bottom
        if(self.rect.bottom > self.game.heightcheck):
            self.rect.bottom = self.game.heightcheck
            self.movey = 0
            self.vy *= -1
        # Top
        if(self.rect.top < 0):
            self.rect.top = 0
            self.movey = 0
            self.vy *= -1
        # Left
        if(self.rect.left < 0):
            self.rect.left = 0
            self.movex = 0
            self.vx *= -1
        # Right
        if(self.rect.right > self.game.widthcheck):
            self.rect.right = self.game.widthcheck
            self.movex = 0
            self.vx *= -1

    def split(self):
        if(self.split_times > 0):
            self.kill()
            for i in range(self.split_into):
                ball = Ball(self.game, self.rect.centerx, self.rect.centery, self.rad//2, random.choice((-1,1)) * (self.vx + random.randint(-self.xchange, self.xchange)), random.choice((-1,1)) * (self.vy + random.randint(-self.ychange, -self.ychange)), self.color, self.split_times - 1, self.split_into)
                self.game.ballGroup.add(ball)
        else:
            self.kill()
        if(not self.game.ballGroup):
            self.game.levelwon = True
            self.game.continue_playing = False
#            self.game.gameWon(K_SPACE, ord('n'))




"""
    def __init__(self, windowwidth, windowheight, endingLevel,
            gameFolder = "levels", startingLevel = 1,
            widthcheck = None, heightcheck = None,
            fps = 120, gravitation = 100,
            two_player = False, show_fps = False, ball_debug = False, dirty = False, caption = "Awesome game! :D"):

"""

game = Game(800, 650, 6, heightcheck = 600, caption = "Ball game", backgroundCount = 4)
game.startGame()

