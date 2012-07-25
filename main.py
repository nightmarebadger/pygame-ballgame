# coding=utf-8

"""

* File Name : main.py

* Created By : Natan Žabkar, natan.zabkar@gmail.com 

* Creation Date : 17-03-2012

* Last Modified : 23.3.2012 1:52:46

"""

from __future__ import division, print_function
import pygame, random, sys, shutil
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

def drawText(text, font, surface, x, y, color, option="center"):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    if(option == "center"):
        textrect.center = (x, y)
    elif(option == "left"):
        textrect.left = x
        textrect.centery = y
    elif(option == "right"):
        textrect.right = x
        textrect.centery = y
    else:
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
        def __init__(self, name, x, y, ticked, width = 2, size = 25):
            pygame.sprite.Sprite.__init__(self)
            self.name = name
            self.ticked = ticked
            self.width = width
            self.size = size
            self.image = pygame.Surface((self.size, self.size))
            self.rect = self.image.get_rect()
            self.rect.center = (x,y)
            

        def clicked(self):
            self.ticked = not self.ticked
        
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
            two_player = False, show_fps = False, ball_debug = False, dirty = False, caption = "Ball game", backgroundCount = 1, configFile = "configuration/game.ini", fullscreen = False):
        
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
        self.fullscreen = fullscreen

        # Debug options
        self.show_fps = show_fps
        self.ball_debug = ball_debug
        self.dirty = dirty

        # Caption
        self.caption = caption

        # Score
        self.score = 0

        # Config file
        self.configFile = configFile
        self.applyConfig(self.readConfig())


    def applyConfig(self, dic):
        def tf(s):
            if(s in ["1", "true"]):
                return True
            return False

        if(dic):
            for i in dic:
                if(i == "width"):
                    self.windowwidth = int(dic[i])
                elif(i == "height"):
                    self.windowheight = int(dic[i])
                elif(i == "endinglevel"):
                    self.endingLevel = int(dic[i])
                elif(i == "gamefolder"):
                    self.gameFolder = dic[i]
                elif(i == "startinglevel"):
                    self.startingLevel = int(dic[i])
                elif(i == "widthcheck"):
                    self.widthcheck = int(dic[i])
                elif(i == "heightcheck"):
                    self.heightcheck = int(dic[i])
                elif(i == "fps"):
                    self.fps = int(dic[i])
                elif(i == "gravitation"):
                    self.gravitation = int(dic[i])
                elif(i == "twoplayer"):
                    self.two_player = tf(dic[i])
                elif(i == "showfps"):
                    self.show_fps = tf(dic[i])
                elif(i == "balldebug"):
                    self.ball_debug = tf(dic[i])
                elif(i == "dirty"):
                    self.dirty = tf(dic[i])
                elif(i == "caption"):
                    self.caption = dic[i]
                elif(i == "backgroundcount"):
                    self.backgroundCount = int(dic[i])
                elif(i == "fullscreen"):
                    self.fullscreen = tf(dic[i])


    def readConfig(self):
        foo = {}
        options = ["width", "height", "endinglevel", "gamefolder", "startinglevel", "widthcheck", "heightcheck", "fps", "gravitation", "twoplayer", "showfps", "balldebug", "dirty", "caption", "backgroundCount", "fullscreen"]
        try:
            with open(self.configFile, 'r') as f:
                for line in f:
                    line = line.strip()
                    if(len(line) > 0 and line[0] != '#'):
                        bar = line.split('=')
                        bar[0] = bar[0].strip().lower()
                        if(bar[0] in options):
                            foo[bar[0]] = bar[1].strip()
                        #print(line)
            return foo
        except:
            print("Ni fajla!")
            return None

    def applyTicktoConfig(self, changes):
        def tf(s):
            if(s):
                return '1'
            return '0'
        shutil.copy(self.configFile, self.configFile + ".backup")
        with open(self.configFile + ".backup", 'r') as base:
            with open(self.configFile, 'w') as new:
                for line in base:
                    write = True
                    foo = line.strip()
                    if(len(foo) > 0 and foo[0] != '#'):
                        bar = foo.split('=')
                        bar[0] = bar[0].strip().lower()
                        for i in changes.copy():
                            if(bar[0] == i):
                                new.write("{0} = {1}\n".format(i, tf(changes[i])))
                                write = False
                                del changes[i]
                    if(write):
                        new.write(line)
                for i in changes:
                    new.write("{0} = {1}\n".format(i, tf(changes[i])))


    def startGame(self):
        self.setup()
        self.startMenu()

    def newGame(self):
        pygame.mouse.set_visible(False)
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
        if(self.fullscreen):
            self.surface = pygame.display.set_mode((self.windowwidth, self.windowheight), FULLSCREEN)
        else:
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
            self.powerupGroup = pygame.sprite.RenderUpdates()
        else:
            self.playerGroup = pygame.sprite.RenderPlain()
            self.ballGroup = pygame.sprite.RenderPlain()
            self.arrowGroup = pygame.sprite.RenderPlain()
            self.powerupGroup = pygame.sprite.RenderPlain()

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
        self.powerupGroup.empty()

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
            self.powerupGroup.update(time/1000)

            # Drawing
            
            if(self.dirty):
                rect1 = self.playerGroup.draw(self.surface)
                rect2 = self.ballGroup.draw(self.surface)
                rect3 = self.arrowGroup.draw(self.surface)
                rect4 = self.powerupGroup.draw(self.surface)

                pygame.display.update(rect1 + rect2 + rect3 + rect4)
                self.playerGroup.clear(self.surface, self.background)
                self.ballGroup.clear(self.surface, self.background)
                self.arrowGroup.clear(self.surface, self.background)
                self.powerupGroup.clear(self.surface, self.background)
            else:
                self.surface.blit(self.background, (0, 0))
                self.playerGroup.draw(self.surface)
                self.ballGroup.draw(self.surface)
                self.arrowGroup.draw(self.surface)
                self.powerupGroup.draw(self.surface)
                pygame.display.update()

    ##############################
    #
    #    DIFFERENT MENU PAGES
    #
    ##############################


    def startMenu(self):
        pygame.mouse.set_visible(True)
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
        tmprect = drawText("Use arrow keys to move", normalFont(40), self.surface, self.windowwidth//2, base + add, WHITE)
        add += 1.5 * tmprect.height
        tmprect = drawText("and space to shoot.", normalFont(40), self.surface, self.windowwidth//2, base + add, WHITE)
        add += 1.5 * tmprect.height
        tmprect = drawText("Destroy all balls while dodging them!", normalFont(40), self.surface, self.windowwidth//2, base + add, WHITE)
        add += 1.5 * tmprect.height
        tmprect = drawText("Careful, you can't move and shoot at the same time ...", normalFont(40), self.surface, self.windowwidth//2, base + add, WHITE)
        pygame.display.update()
        self.waitForPlayerKeypress("any")

    def options(self):
        def applyTicks(ticks):
            for i in ticks:
                if(i.name == "fullscreen"):
                    self.fullscreen = i.ticked
                elif(i.name == "showfps"):
                    self.show_fps = i.ticked
                elif(i.name == "twoplayer"):
                    self.two_player = i.ticked

        self.surface.fill(BLACK)
        tickGroup = pygame.sprite.RenderPlain()
       
        hstart = 1/4 * self.windowheight
        hspace = 100
        vstart = 1/2 * self.windowwidth + 50 
        vspace = 60


        drawText("Fullscreen", normalFont(50), self.surface, vstart, hstart, WHITE, option = "right")
        drawText("Show FPS", normalFont(50), self.surface, vstart, hspace + hstart, WHITE, option = "right")
        drawText("Two players", normalFont(50), self.surface, vstart, 2*hspace + hstart, WHITE, option = "right")

        fullscreen = self.Tick("fullscreen", vstart + vspace, hstart, self.fullscreen)
        tickGroup.add(fullscreen)
        showfps = self.Tick("showfps", vstart + vspace, hspace + hstart, self.show_fps)
        tickGroup.add(showfps)
        twoplayer = self.Tick("twoplayer", vstart + vspace, 2*hspace + hstart, self.two_player)
        tickGroup.add(twoplayer)

        cancel = drawText("Cancel", normalFont(50), self.surface, 1/4 * self.windowwidth, self.windowheight - 100, WHITE) 
        accept = drawText("Accept", normalFont(50), self.surface, 3/4 * self.windowwidth, self.windowheight - 100, WHITE) 

        tickGroup.update()
        tickGroup.draw(self.surface)
        pygame.display.update()

        while_bool = True
        while while_bool:
            for event in pygame.event.get():
                if(event.type == QUIT):
                    terminate()
                elif(event.type == KEYDOWN):
                    if(event.key == K_ESCAPE):
                        terminate()
                elif(event.type == MOUSEBUTTONDOWN):
                    if(event.button == 1):
                        if(fullscreen.rect.collidepoint(event.pos)):
                            fullscreen.clicked()
                            fullscreen.update()
                            tickGroup.draw(self.surface)
                            pygame.display.update()
                        elif(showfps.rect.collidepoint(event.pos)):
                            showfps.clicked()
                            showfps.update()
                            tickGroup.draw(self.surface)
                            pygame.display.update()
                        elif(twoplayer.rect.collidepoint(event.pos)):
                            twoplayer.clicked()
                            twoplayer.update()
                            tickGroup.draw(self.surface)
                            pygame.display.update()
                        elif(cancel.collidepoint(event.pos)):
                            while_bool = False
                        elif(accept.collidepoint(event.pos)):
                            foo = {}
                            applyTicks(tickGroup)
                            for i in tickGroup:
                                foo[i.name] = i.ticked
                            self.applyTicktoConfig(foo)
                            while_bool = False
                            


    ##############################
    #
    #  DIFFERENT "POPUP" SCREENS
    #
    ##############################

    def gameWon(self):
        base = self.windowheight//2
        add = 0
        self.surface.fill(BLACK)
        drawText("You won the game!", normalFont(80), self.surface, self.windowwidth//2, base + add, WHITE)
        add = 100
        drawText("Press any key ... ", normalFont(20), self.surface, self.windowwidth//2, base + add, WHITE)
        pygame.display.update()
        self.waitForPlayerKeypress("any")

    def gameLost(self):
        base = self.windowheight//2
        add = 0
        self.surface.fill(BLACK)
        drawText("You lost ... :(", normalFont(80), self.surface, self.windowwidth//2, base + add, WHITE)
        add = 100
        drawText("Press any key ... ", normalFont(20), self.surface, self.windowwidth//2, base + add, WHITE)
        pygame.display.update()
        self.waitForPlayerKeypress("any")

    def levelWon(self):
        base = self.windowheight//2
        add = 0
        self.surface.fill(BLACK)
        drawText("Level won!", normalFont(80), self.surface, self.windowwidth//2, base + add, WHITE)
        add += 80
        drawText("Only {0} levels to go".format(self.endingLevel - self.currentLevel + 1), normalFont(30), self.surface, self.windowwidth//2, base + add, WHITE)
        add += 20
        drawText("Press any key ... ", normalFont(20), self.surface, self.windowwidth//2, base + add, WHITE)
        pygame.display.update()
        self.waitForPlayerKeypress("any")

    def getReady(self):
        base = self.windowheight//2
        add = 0
        self.surface.fill(BLACK)
        drawText("Get ready!", normalFont(80), self.surface, self.windowwidth//2, base + add, WHITE)
        add = 100
        drawText("Press any key ... ", normalFont(20), self.surface, self.windowwidth//2, base + add, WHITE)
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
        
        powerup = Powerup(self.game, self.rect.centerx, self.rect.bottom - self.rad/5, random.choice(("life", "invisibility", "power")))
        self.game.powerupGroup.add(powerup)
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


class Powerup(pygame.sprite.Sprite):
    def __init__(self, game, x, y, name):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.x = x
        self.y = y
        self.name = name
        self.v = 100
        self.move = 0
        self.width = 50
        self.height = 50
        self.timer = 5


        self.image = pygame.Surface((self.width, self.height))
        if(self.name == "life"):
            self.image.fill(RED)
        elif(self.name == "invisibility"):
            self.image.fill(BLUE)
        elif(self.name == "power"):
            self.image.fill(GREEN)
        else:
            self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.midtop = (self.x, self.y)
        self.mask = pygame.mask.from_surface(self.image, 0)
        self.mask.fill()
        
    def update(self, time):
        self.move += self.v * time
        if(self.rect.bottom < self.game.heightcheck):
            self.rect.move_ip(0, self.move)
            self.move -= int(self.move)
            if(self.rect.bottom < 0):
                self.rect.bottom = 0
        else:
            if(self.timer <= 0):
                self.kill()
            self.timer -= time
       

"""
    def __init__(self, windowwidth, windowheight, endingLevel,
            gameFolder = "levels", startingLevel = 1,
            widthcheck = None, heightcheck = None,
            fps = 120, gravitation = 100,
            two_player = False, show_fps = False, ball_debug = False, dirty = False, caption = "Awesome game! :D"):

"""

game = Game(800, 650, 6, heightcheck = 600, caption = "Ball game", backgroundCount = 4)
game.startGame()

