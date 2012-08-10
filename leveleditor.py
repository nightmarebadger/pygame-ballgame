# coding=utf-8


from __future__ import division, print_function
import pygame, random, sys, shutil
from pygame.locals import *
from colors import *

def terminate():
    pygame.quit()
    sys.exit()
    
def normalFont(size, font_name = "menu_font"):

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
    
    #command = 'drawText("{0}", {1}, {2}, {3}, {4}, {5}, option="{6}")'.format(text, font, surface, x, y, color, option) 
        
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
        flag = True
        for foo in self.editor.ballGroup:
            if( ((foo.rect.centerx - x)**2 + (foo.rect.centery - y)**2)**(1/2) <= foo.rad + self.rad ):
                flag = False
                break
        if(flag):
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
        
    def drawArrow(self):
        pygame.draw.line(self.editor.surface, BLACK, self.rect.center, (self.rect.centerx + self.vx, self.rect.centery + self.vy), 3)
            
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
        
        self.menuRect = {}
        self.drawmenuRect = []
        self.menuRectSelected = {}
        self.drawmenuRectSelected = []
        
        foo = 'drawText("Save level", normalFont(50), self.surface, self.widthcheck + (self.windowwidth - self.widthcheck)/2, 50, BLUE)'
        self.menuItem(foo, "save")
        
        foo = 'drawText("Open level", normalFont(50), self.surface, self.widthcheck + (self.windowwidth - self.widthcheck)/2, 100, BLUE)'
        self.menuItem(foo, "open")
        
        foo = 'drawText("Delete chosen", normalFont(50), self.surface, self.widthcheck + (self.windowwidth - self.widthcheck)/2, 200, BLUE)'
        self.menuItem(foo, "delete", True)
        
        foo = 'drawText("Split times +1", normalFont(25), self.surface, self.widthcheck + (self.windowwidth - self.widthcheck)/2, 325, BLUE)'
        self.menuItem(foo, "splittimes+1", True)
        
        foo = 'drawText("Split times -1", normalFont(25), self.surface, self.widthcheck + (self.windowwidth - self.widthcheck)/2, 350, BLUE)'
        self.menuItem(foo, "splittimes-1", True)
        #foo = 'drawText("Split into: {0}", normalFont(50), self.surface, self.widthcheck + (self.windowwidth - self.widthcheck)/2, 300, BLUE)'
        #self.menuItem(foo, "delete")
        
        foo = 'drawText("Split into +1", normalFont(25), self.surface, self.widthcheck + (self.windowwidth - self.widthcheck)/2, 425, BLUE)'
        self.menuItem(foo, "splitinto+1", True)
        
        foo = 'drawText("Split into -1", normalFont(25), self.surface, self.widthcheck + (self.windowwidth - self.widthcheck)/2, 450, BLUE)'
        self.menuItem(foo, "splitinto-1", True)
        
        foo = 'drawText("Vx +1", normalFont(25), self.surface, self.widthcheck + (self.windowwidth - self.widthcheck)/2, 525, BLUE)'
        self.menuItem(foo, "vx+1", True)
        foo = 'drawText("Vx -1", normalFont(25), self.surface, self.widthcheck + (self.windowwidth - self.widthcheck)/2, 550, BLUE)'
        self.menuItem(foo, "vx-1", True)
        foo = 'drawText("Vx +10", normalFont(25), self.surface, self.widthcheck + (self.windowwidth - self.widthcheck)/2, 575, BLUE)'
        self.menuItem(foo, "vx+10", True)
        foo = 'drawText("Vx -10", normalFont(25), self.surface, self.widthcheck + (self.windowwidth - self.widthcheck)/2, 600, BLUE)'
        self.menuItem(foo, "vx-10", True)
        
        foo = 'drawText("Vy +1", normalFont(25), self.surface, self.widthcheck + (self.windowwidth - self.widthcheck)/2, 675, BLUE)'
        self.menuItem(foo, "vy+1", True)
        foo = 'drawText("Vy -1", normalFont(25), self.surface, self.widthcheck + (self.windowwidth - self.widthcheck)/2, 700, BLUE)'
        self.menuItem(foo, "vy-1", True)
        foo = 'drawText("Vy +10", normalFont(25), self.surface, self.widthcheck + (self.windowwidth - self.widthcheck)/2, 725, BLUE)'
        self.menuItem(foo, "vy+10", True)
        foo = 'drawText("Vy -10", normalFont(25), self.surface, self.widthcheck + (self.windowwidth - self.widthcheck)/2, 750, BLUE)'
        self.menuItem(foo, "vy-10", True)
        
        self.ballGroup = pygame.sprite.RenderPlain()
        self.arrow = False
        
    def menuItem(self, command, name, slc=False):
        if(slc):
            self.menuRectSelected[name] = eval(command)
            self.drawmenuRectSelected.append(command)
        else:
            self.menuRect[name] = eval(command)
            self.drawmenuRect.append(command)
        
        
    def mainloop(self):
        global x,y, onMouse, globalcount, selected
        while True:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if(event.type == QUIT):
                    terminate()
                elif(event.type == KEYDOWN):
                    if(event.key == K_ESCAPE):
                        terminate()
                    if(event.key == ord('a')):
                        if(selected):
                            selected = None
                        globalcount -= 1
                        if(globalcount < 0):
                            globalcount = 0
                        onMouse = itemsList[globalcount]
                    if(event.key == ord('s')):
                        if(selected):
                            selected = None
                        try:
                            globalcount += 1
                            onMouse = itemsList[globalcount]
                        except:
                            globalcount -= 1
                            onMouse = itemsList[globalcount]


                elif(event.type == MOUSEMOTION):
                    x,y = event.pos
                    if(pygame.mouse.get_pressed()[0]):
                        if(selected):
                            if(event.pos[0] <= self.widthcheck and event.pos[1] <= self.heightcheck):
                                selected.vx = event.pos[0] - selected.rect.centerx
                                selected.vy = event.pos[1] - selected.rect.centery
                            else:
                                if(event.pos[0] == selected.rect.centerx):
                                    selected.vx = 0
                                    selected.vy = self.heightcheck - selected.rect.centery
                                elif(event.pos[1] == selected.rect.centery):
                                    selected.vx = self.widthcheck - selected.rect.centerx
                                    selected.vy = 0
                                #elif(event.pos[0] > self.widthcheck and event.pos[1] > self.heightcheck):
                                else:
                                    tmpx1 = event.pos[0] - self.widthcheck
                                    tmpy1 = tmpx1*(event.pos[1] - selected.rect.centery)/(event.pos[0] - selected.rect.centerx)
                                    if(event.pos[1] - tmpy1 <= self.heightcheck and event.pos[0] > selected.rect.centerx):
                                        selected.vx = self.widthcheck - selected.rect.centerx
                                        selected.vy = event.pos[1] - tmpy1 - selected.rect.centery
                                    else:
                                        tmpy2 = event.pos[1] - self.heightcheck
                                        tmpx2 = tmpy2*(event.pos[0] - selected.rect.centerx)/(event.pos[1] - selected.rect.centery)
                                        selected.vx = event.pos[0] - tmpx2 - selected.rect.centerx
                                        selected.vy = self.heightcheck - selected.rect.centery
                                        
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
                        #flag = False
                        if(event.pos[0] <= self.widthcheck and event.pos[1] <= self.heightcheck):
                            if(globalcount >= 0):
                                onMouse.paint()
                            if(selected):
                                selected.vx = event.pos[0] - selected.rect.centerx
                                selected.vy = event.pos[1] - selected.rect.centery
                        else:
                            for foo in menuballGroup:
                                if(foo.rect.collidepoint(event.pos)):
                                    if(selected):
                                        selected = None
                                    #flag = True
                                    count = 0
                                    for i in itemsList:
                                        if(i.color == foo.color):
                                            globalcount = count
                                        count += 1
                                    onMouse = itemsList[globalcount]
                            for foo in self.menuRect.iteritems():
                                if(foo[1].collidepoint(event.pos)):
                                    #flag = True
                                    print(foo[0])
                            if(selected):
                                for foo in self.menuRectSelected.iteritems():
                                    if(foo[1].collidepoint(event.pos)):
                                        #flag = True
                                        if(foo[0] == "delete"):
                                            self.ballGroup.remove(selected)
                                            selected = None
                                        elif(foo[0] == "splittimes+1"):
                                            selected.split_times += 1
                                        elif(foo[0] == "splittimes-1"):
                                            selected.split_times -= 1
                                        elif(foo[0] == "splitinto+1"):
                                            selected.split_into += 1
                                        elif(foo[0] == "splitinto-1"):
                                            selected.split_into -= 1
                                        elif(foo[0] == "vx+1"):
                                            selected.vx += 1
                                        elif(foo[0] == "vx-1"):
                                            selected.vx -= 1
                                        elif(foo[0] == "vx+10"):
                                            selected.vx += 10
                                        elif(foo[0] == "vx-10"):
                                            selected.vx -= 10
                                        elif(foo[0] == "vy+1"):
                                            selected.vy += 1
                                        elif(foo[0] == "vy-1"):
                                            selected.vy -= 1
                                        elif(foo[0] == "vy+10"):
                                            selected.vy += 10
                                        elif(foo[0] == "vy-10"):
                                            selected.vy -= 10
                                        print(foo[0])
                            
                    elif(event.button == 3):
                        selectflag = True
                        for foo in self.ballGroup:
                            if( ((foo.rect.centerx - x)**2 + (foo.rect.centery - y)**2)**(1/2) <= foo.rad):
                                selectflag = False
                                selected = foo
                                globalcount = -1
                                break
                        if(selectflag):
                            selected = None
                        
                        
                    if(globalcount >= 0):
                        if(event.button == 4):
                            onMouse.rad += 2
                            if(onMouse.rad < 1):
                                onMouse.rad = 1
                            onMouse.rescale()
                        elif(event.button == 5):
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
            
        #global onMouse
        if(globalcount >= 0):
            onMouse.draw()
        
        #newgame_rect = drawText("New game", normalFont(60), self.surface, self.windowwidth//2, 1/4 * self.windowheight, BLUE)
        for foo in self.drawmenuRect:
            eval(foo)
            
        #if a ball is selected, draw something so we know :)
        if(selected):
            pygame.draw.circle(self.surface, BLACK, selected.rect.center, 10)
            selected.drawArrow()
            drawText("Split times: {0}".format(selected.split_times), normalFont(50), self.surface, self.widthcheck + (self.windowwidth - self.widthcheck)/2, 300, BLUE)
            drawText("Split into: {0}".format(selected.split_into), normalFont(50), self.surface, self.widthcheck + (self.windowwidth - self.widthcheck)/2, 400, BLUE)
            drawText("Vx: {0}".format(selected.vx), normalFont(50), self.surface, self.widthcheck + (self.windowwidth - self.widthcheck)/2, 500, BLUE)
            drawText("Vy: {0}".format(selected.vy), normalFont(50), self.surface, self.widthcheck + (self.windowwidth - self.widthcheck)/2, 650, BLUE)
            for foo in self.drawmenuRectSelected:
                eval(foo)
                          
        pygame.display.update()
        


x = y = 0
editor = Editor(1100, 800, widthcheck=800, heightcheck=600)

selected = None

editor.setup()

ballRed = Ball(editor, x, y, 80, 100, 200, "red", 1, 1)
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