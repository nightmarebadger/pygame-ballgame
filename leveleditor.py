# coding=utf-8


from __future__ import division, print_function
import pygame, random, sys, shutil
from pygame.locals import *
from colors import *

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
            

class Ball(pygame.sprite.Sprite):
    image_red = pygame.image.load("images/ball/red.png")
    image_green = pygame.image.load("images/ball/green.png")
    image_blue = pygame.image.load("images/ball/blue.png")
    
    def __init__(self, editor, x, y, rad, vx, vy, color, split_times, split_into, type="normal"):
        pygame.sprite.Sprite.__init__(self)
       
        self.editor = editor

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
            self.image = pygame.transform.scale(Ball.image_red.convert_alpha(), (2 * self.rad, 2 * self.rad))
        elif(self.color == "green"):
            self.image = pygame.transform.scale(Ball.image_green.convert_alpha(), (2 * self.rad, 2 * self.rad))
        elif(self.color == "blue"):
            self.image = pygame.transform.scale(Ball.image_blue.convert_alpha(), (2 * self.rad, 2 * self.rad))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        if(type != "menu"):
            if(self.rect.top < 0):
                self.rect.top = 0
            if(self.rect.bottom > self.editor.heightcheck):
                self.rect.bottom = self.editor.heightcheck
            if(self.rect.left < 0):
                self.rect.left = 0
            if(self.rect.right > self.editor.widthcheck):
                self.rect.right = self.editor.widthcheck
        
    def update(self):
        global x,y
        self.rect.center = (x, y)
        if(self.rect.top < 0):
            self.rect.top = 0
        if(self.rect.bottom > self.editor.heightcheck):
            self.rect.bottom = self.editor.heightcheck
        if(self.rect.left < 0):
            self.rect.left = 0
        if(self.rect.right > self.editor.widthcheck):
            self.rect.right = self.editor.widthcheck
        
            
    def draw(self):
        self.editor.surface.blit(self.image, self.rect)
    
    def paint(self):
        global x,y
        tmpball = Ball(self.editor, x, y, self.rad, self.vx, self.vy, self.color, self.split_times, self.split_into)
        self.editor.ballGroup.add(tmpball)
        

    def rescale(self):
        global x,y
        if(self.color == "red"):
            self.image = pygame.transform.scale(Ball.image_red.convert_alpha(), (2 * self.rad, 2 * self.rad))
        elif(self.color == "green"):
            self.image = pygame.transform.scale(Ball.image_green.convert_alpha(), (2 * self.rad, 2 * self.rad))
        elif(self.color == "blue"):
            self.image = pygame.transform.scale(Ball.image_blue.convert_alpha(), (2 * self.rad, 2 * self.rad))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        
            
class Editor:
    def __init__(self, windowwidth, windowheight, widthcheck = None, heightcheck = None, fps=120):
        
        # Base game options
        self.windowwidth = windowwidth
        self.windowheight = windowheight

        # Extra game options
        if(widthcheck == None):
            self.widthcheck = windowwidth
        else:
            self.widthcheck = widthcheck
        if(heightcheck == None):
            self.heightcheck = windowheight
        else:
            self.heightcheck = heightcheck

        self.caption = "Level editor"
        
        self.fps = fps

    
    def setup(self):           
        pygame.init()
        pygame.display.set_caption(self.caption)
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode((self.windowwidth, self.windowheight), SRCALPHA)
        self.level = pygame.Surface((self.widthcheck, self.heightcheck))
        self.level.fill(WHITE)
        
        
        self.ballGroup = pygame.sprite.RenderPlain()
        
        
    def mainloop(self):
        global x,y, onMouse, globalcount
        #self.clock.tick()
        while True:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if(event.type == QUIT):
                    terminate()
                elif(event.type == KEYDOWN):
                    if(event.key == K_ESCAPE):
                        terminate()
                    if(event.key == ord('a')):
                        globalcount -= 1
                        if(globalcount < 0):
                            globalcount = 0
                        else:
                            onMouse = itemsList[globalcount]
                    if(event.key == ord('s')):
                        try:
                            globalcount += 1
                            onMouse = itemsList[globalcount]
                        except:
                            globalcount -= 1


                elif(event.type == MOUSEMOTION):
                    x,y = event.pos
                elif(event.type == MOUSEBUTTONDOWN):
                    """
                        1: levi
                        2: srednji
                        3: desni
                        4: kolešček gor
                        5: kolešček dol
                        8: stranski
                    
                    """
                    #print("Mouse at ({0}, {1}), button {2}".format(event.pos[0], event.pos[1], event.button))
                    if(event.button == 1):
                        flag = False
                        for foo in menuballGroup:
                            if(foo.rect.collidepoint(event.pos)):
                                flag = True
                                count = 0
                                for i in itemsList:
                                    if(i.color == foo.color):
                                        globalcount = count
                                    count += 1
                                onMouse = itemsList[globalcount]
                        if(not flag):
                            onMouse.paint()
                    if(event.button == 4):
                        onMouse.rad += 2
                        if(onMouse.rad < 1):
                            onMouse.rad = 1
                        onMouse.rescale()
                    if(event.button == 5):
                        onMouse.rad -= 2
                        if(onMouse.rad < 1):
                            onMouse.rad = 1
                        onMouse.rescale()
            
            onMouse.update()
            self.draw()
                        
    def draw(self):
        self.surface.fill(GRAY)
        self.surface.blit(self.level, (0,0))
        
        # Nariši vse kar je potrebno
        for ball in self.ballGroup:
            self.surface.blit(ball.image, ball.rect)
        menuballGroup.draw(self.surface)
            
        global onMouse
        onMouse.draw()
        
        pygame.display.update()
        


x = y = 0
editor = Editor(800, 800, widthcheck=800, heightcheck=600)
editor.setup()

ballRed = Ball(editor, x, y, 80, 0, 0, "red", 1, 1)
ballBlue = Ball(editor, x, y, 80, 0, 0, "blue", 1, 1)
ballGreen = Ball(editor, x, y, 80, 0, 0, "green", 1, 1)

"""
    'Menu' balls
"""

menuballRed = Ball(editor, 125, 700, 75, 0, 0, "red", 1, 1, type="menu")
menuballBlue = Ball(editor, editor.widthcheck//2, 700, 75, 0, 0, "blue", 1, 1, type="menu")
menuballGreen = Ball(editor, editor.widthcheck-125, 700, 75, 0, 0, "green", 1, 1, type="menu")

menuballGroup = pygame.sprite.RenderPlain()
menuballGroup.add(menuballRed, menuballBlue, menuballGreen)



globalcount = 0
itemsList = [ballRed, ballBlue, ballGreen]

onMouse = itemsList[globalcount]


editor.mainloop()