#coding = utf-8
import sys
import pygame as pg
from pygame.locals import *

full_screen = (800,400)
black = (0,0,0)

class Background(pg.sprite.Sprite):
    def __init__(self, image_file, location):
        pg.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pg.image.load(image_file)
        self.image = pg.transform.scale(self.image,full_screen)
        self.rect = self.image.get_rect()
        self.rect.top, self.rect.left = location

class Baccarat : 
    def __init__(self) :
        pg.init()
        pg.display.set_caption('Baccarat')
        self.screen = pg.display.set_mode(full_screen)
        self.clock = pg.time.Clock()
        
        #initalize sprites
        self.background = Background('background_image.jpg', [0,0])
        
    def run(self) :
        self.playing = True 
        
        while self.playing : 
            pg.time.delay(100) #pause the program for the amount of time
            
            self.events()
            self.update()
            self.draw()

    
    def quit(self) :
        pg.quit()
        sys.exit()
    
    def events(self) :
        for event in pg.event.get() :
            if event.type == pg.QUIT :
                self.quit()
            if event.type == pg.KEYDOWN :
                if event.key == pg.K_ESCAPE :
                    self.quit()
                    
    def update(self) :
        pg.display.update()
        
    def draw(self) :
        self.screen.fill(black)
        self.screen.blit(self.background.image, self.background.rect)

baccarat = Baccarat()

baccarat.run()
