import pygame
import os
import neat
import time
#windons frame constants
WIN_WIDTH=600
WIN_HEIGHT=800
BIRD_IMGS=[pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird1.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird2.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird3.png")))]
PIPE_IMG=pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")))
BASE_IMG=pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")))
BG_IMG=pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bg.png")))

class Bird:
    IMGS=BIRD_IMGS
    MIX_ROTATION=25
    ROTATION_VELOCITY=20
    ANIMATION_TIME=5

#initiating variable in the class
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.tilt=0
        self.tick_count=0
        self.velocity=0
        self.height=self.y
        self.img_count=0
        self.img=self.IMGS[0]
        
#makin the bird jump
    def jump(self):
        self.velocity=-10.5
        self.tick_count=0
        self.height=self.y

#foumal for downward acceleration
    def move(self):
        self.tick_count +=1
        displacement = self.velocity*self.tick_count+1.5*self.tick_count**2

        #terminal velocity
        if displacement >=16:
            displacement = 16

        if displacement < 0:
            displacement -= 2

        self.y=self.y=displacement
        
        if displacement < 0 or self.y < self.height + 50:
            if self.tilt < self.MIX_ROTATION:
                self.tilt = self.MIX_ROTATION
        
        else:
            if self.tilt >- 90:
                self.tilt -= self.ROTATION_VELOCITY

    def draw(self, windon):
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4+1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rectangle = rotated_image.get_rect(center = self.img.get_rect(top_Left = (self.x,self.y)).center)
        windon.blit(rotated_image,new_rectangle.top_left)