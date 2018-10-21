import pygame
from pygame.locals import *
import os
import sys
import math
import random

pygame.init()

W, H = 800, 447
win = pygame.display.set_mode((W,H))
pygame.display.set_caption('Side Scroller')
bg = pygame.image.load(os.path.join('images','bg.png')).convert()
bgX = 0
bgX2 = bg.get_width()

clock = pygame.time.Clock()

class player(object):
    run = [pygame.image.load(os.path.join('images', str(x) + '.png')) for x in range(8,16)]
    jump = [pygame.image.load(os.path.join('images', str(x) + '.png')) for x in range(1,8)]
    slide = [pygame.image.load(os.path.join('images', 'S1.png')),pygame.image.load(os.path.join('images', 'S2.png')),pygame.image.load(os.path.join('images', 'S2.png')),pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')),pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S3.png')), pygame.image.load(os.path.join('images', 'S4.png')), pygame.image.load(os.path.join('images', 'S5.png'))]
    fall = pygame.image.load(os.path.join('images','0.png'))
    jumpList = [1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4]
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.jumping = False
        self.sliding = False
        self.slideCount = 0
        self.jumpCount = 0
        self.runCount = 0
        self.slideUp = False
        self.falling = False

    def draw(self, win):
        if self.falling:
            win.blit(self.fall,(self.x,self.y+30))
        elif self.jumping:
            self.y -= self.jumpList[self.jumpCount] * 1.2
            win.blit(self.jump[self.jumpCount//18], (self.x,self.y))
            self.jumpCount += 1
            if self.jumpCount > 108:
                self.jumpCount = 0
                self.jumping = False
                self.runCount = 0
            self.hitbox = (self.x+4,self.y,self.width-24,self.height-10)
        elif self.sliding or self.slideUp:
            if self.slideCount < 20:
                self.y += 1
            elif self.slideCount == 80:
                self.y -= 19
                self.sliding = False
                self.slideUp = True
            elif self.slideCount > 20 and self.slideCount <80:
                self.hitbox =(self.x,self.y+3,self.width-8,self.height-35)
            if self.slideCount >= 110:
                self.slideCount = 0
                self.slideUp = False
                self.runCount = 0
                self.hitbox = (self.x+4,self.y,self.width-24,self.height-10)
            win.blit(self.slide[self.slideCount//10], (self.x,self.y))
            self.slideCount += 1
        else:
            if self.runCount > 42:
                self.runCount = 0
            win.blit(self.run[self.runCount//6], (self.x,self.y))
            self.runCount += 1
            self.hitbox = (self.x+4,self.y,self.width-24,self.height-13)
        pygame.draw.rect(win,(255,0,0),self.hitbox,2)

class saw(object):
    img = [pygame.image.load(os.path.join('images','SAW0.png')), pygame.image.load(os.path.join('images','SAW1.png')) ,pygame.image.load(os.path.join('images','SAW2.png')),pygame.image.load(os.path.join('images','SAW3.png'))]
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.hitbox =(x,y,width,height)
        self.count = 0

    def draw(self,win):
        self.hitbox=(self.x +5,self.y+5,self.width -10,self.height)
        if self.count >= 8:
            self.count = 0
        win.blit(pygame.transform.scale(self.img[self.count//2], (64,64)), (self.x,self.y))
        self.count += 1
        pygame.draw.rect(win,(255,0,0), self.hitbox,2)
    
    def collide (self,rect):
        if rect[0]+rect[2] >self.hitbox[0] and rect[0]<self.hitbox[0]+self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1]:
                return True
            return False

class spike(saw):
    img = pygame.image.load(os.path.join('images','spike.png'))

    def draw(self,win):
        self.hitbox =(self.x+10,self.y,28,315)
        win.blit(self.img, (self.x,self.y))
        pygame.draw.rect(win, (255,0,0),self.hitbox,2)
    
    def collide (self,rect):
        if rect[0]+rect[2] >self.hitbox[0] and rect[0]<self.hitbox[0]+self.hitbox[2]:
            if rect[1] < self.hitbox[3]:
                return True
            return False

def redrawWindow():
    win.blit(bg, (bgX,0))
    win.blit(bg, (bgX2,0))
    runner.draw(win)
    for x in objects:
        x.draw(win)
    font = pygame.font.SysFont('comicsans',30)
    text = font.render('Score: ' + str(score),1,(255,255,255))
    win.blit(text,(700,10))
    pygame.display.update()

def UpdateFile():
    f= open('scores.txt','r')
    file = f.readlines()
    last = int(file[0])
    if last < int(score):
        f.close()
        file=open('scores.txt','w')
        file.write(str(score))
        file.close()
        return score
    return last

def endScreen():
    global pause, objects,fps,score
    runner.falling=False
    pause = 0
    objects = []
    fps = 60
    run=True
    while run:
        pygame.time.delay(100)
        win.blit(bg,(0,0))
        largeFont = pygame.font.SysFont('comicsans',80)
        previousScore = largeFont.render('Previous Score: ' + str(UpdateFile()),1,(255,255,255))
        win.blit(previousScore, (W/2 - previousScore.get_width()/2,200))
        newScore= largeFont.render('Score: '+ str(score),1,(255,255,255))
        win.blit(newScore,(W/2 - newScore.get_width()/2,320))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type ==pygame.MOUSEBUTTONDOWN:
                run = False
    score = 0

runner = player(200,313,64,64)
pygame.time.set_timer(USEREVENT+1,500)
pygame.time.set_timer(USEREVENT+2,random.randrange(3000,5000))
fps = 60
run=True

pause = 0
fallSpeed = 0 
objects = []

while run:
    score = fps//5 - 12
    if pause >0:
        pause +=1
        if pause > fallSpeed *2:
            endScreen()
    for o in objects:
        if o.collide(runner.hitbox):
            runner.falling = True
            if pause ==0:
                fallSpeed = fps
                pause = 1
        o.x -= 1.4
        if o.x < o.width *-1:
            objects.pop(objects.index(o))
    bgX -= 1.4
    bgX2 -= 1.4
    if bgX < bg.get_width() * -1:
        bgX = bg.get_width()
    if bgX2 < bg.get_width() * -1:
        bgX2 = bg.get_width()
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
        if not(runner.jumping) and not(runner.sliding):
            runner.jumping=True
    if keys[pygame.K_DOWN]:
        if not (runner.sliding) and not(runner.jumping):
            runner.sliding = True
    redrawWindow()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
            pygame.quit()
            sys.exit
        if event.type == USEREVENT+1:
            fps +=1
        if event.type == USEREVENT+2:
            r = random.randrange(0,2)
            if r == 0:
                objects.append(saw(810,310,64,64))
            else:
                objects.append(spike(810,0,48,320))
    clock.tick(fps)

    