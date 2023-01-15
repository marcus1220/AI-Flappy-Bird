import pygame
import neat
import os
import time
import random

#window frame constants
WIN_WIDTH = 550
WIN_HEIGHT = 800

#images
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))


#creating the bird class
class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROTATION_VELOCITY = 20
    ANIMATION_TIME = 5

    #initiating variables in the class (sort of like the starting identity of the bird)
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.velocity = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]


    #responsible for making the bird jump
    def jump(self):
        self.velocity = -10.5 #its negative as the bird is constantly wanting to fall down
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        #formula for downward acceleration
        displacement = self.velocity * self.tick_count + 1.5 * self.tick_count ** 2

        #terminal velocity 
        if displacement >= 16:
            displacement = 16

        if displacement < 0:
            displacement -= 2

        #updating the y-axis
        self.y = self.y + displacement

        #tilts the bird up, otherwise down
        if displacement < 0 or self.y < self.height + 50:  
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else: 
            if self.tilt > -90:
                self.tilt -= self.ROTATION_VELOCITY


    def draw(self, window):
        self.img_count += 1

        #animating the bird flying
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME *2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME *3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME *4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME *4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME *2

        #hitbox for the bird
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rectangle = rotated_image.get_rect(center = (self.x, self.y))
        window.blit(rotated_image, new_rectangle.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

#class for base
class Pipe:
    GAP = 200
    VELOCITY = 5


    def __init__(self,x):
        self.x=x
        self.height=0
        self.hop=0
        self.botton=0
        self.PIPE_TOP=pygame.transform.flip(PIPE_IMG,False,True)
        self.PIPE_BOTTON=PIPE_IMG
        self.passed=False
        self.set_height()

#random height
    def set_height(self):
        self.height=random.randrange(50,450)
        self.top=self.height-self.PIPE_TOP.get_height()
        self.botton=self.height+self.GAP

    def move(self):
        self.x-=self.VELOCITY

    def draw(self,window):
        window.blit(self.PIPE_TOP,(self.x,self.top))
        window.blit(self.PIPE_BOTTON,(self.x,self.botton))
    
    def collide(self,bird,window):
        bird_mask=bird.get_mask()
        top_mask=pygame.mask.from_surface(self.PIPE_TOP)
        botton_mask=pygame.mask.from_surface(self.PIPE_BOTTON)
        top_offset=(self.x-bird.x,self.top-round(bird.y))
        botton_offset=(self.x-bird,self.botton-round.y)
        top_point=bird_mask.overlap(top_mask, top_offset)
        botton_point=bird_mask.overlap(botton_mask, botton_offset)

        if top_point or botton_point:
            return True
        return False


class Base:
    VELOCITY = 5
    width = BASE_IMG.get_width()
    img=BG_IMG

    def __init__(self,y):
        self.y=y
        self.x1=0
        self.x2=self.WIDTH

    def move(self):
        self.x1-=self.VELOCITY
        self.x2-=self.VELOCITY
        
        if self.x1+self.width <0:
            self.x1=self.x2+self.WIDTH

        if self.x2+self.width <0:
            self.x2=self.x1+self.WIDTH

    def draw(self,window):
        window.blit(self.IMG,(self.x1,self.y))
        window.blit(self.IMG,(self.x2,self.y))




def draw_window(window, bird):
    window.blit(BG_IMG, (0,0))
    bird.draw(window)
    pygame.display.update()

def main():
    bird = Bird(200, 200)
    window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    fps = pygame.time.Clock()

    run = True
    while run:
        fps.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        bird.move()
        draw_window(window, bird)

    pygame.quit()
    quit()


main()
