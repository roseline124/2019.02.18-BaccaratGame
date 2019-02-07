#coding = utf-8
import sys
import pygame as pg
from pygame.locals import *

SCREEN_SIZE = (800,500)
BLACK = (0,0,0)
CARD_SIZE = (180,270)
CARD_LOCATION = [30,30]
FPS = 30 


SCREEN_SIZE = (800,500)
BLACK = (0,0,0)
CARD_SIZE = (180,270)
CARD_LOCATION = [30,30]
FPS = 30 


class Background(pg.sprite.Sprite):
    def __init__(self, image_file, LOCATION):
        pg.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pg.image.load(image_file)
        self.image = pg.transform.scale(self.image,SCREEN_SIZE)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = LOCATION
        

class Cards(pg.sprite.Sprite) :
    def __init__(self, image_file, LOCATION) :
        pg.sprite.Sprite.__init__(self)  #sprite initializer
        self.image = pg.image.load(image_file)
        self.image_size = CARD_SIZE
        self.image = pg.transform.scale(self.image, self.image_size)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = LOCATION 
        

class Baccarat : 
    def __init__(self) :
        pg.init()
        pg.display.set_caption('Baccarat')
        self.screen = pg.display.set_mode(SCREEN_SIZE)
        self.clock = pg.time.Clock()
        
        #make sprites
        self.cards = Cards('card.png', CARD_LOCATION)
        self.background = Background('background_image.jpg', (0,0))
        
        #sprites group
        self.sprites = pg.sprite.Group()
        self.sprites.add(self.cards)
        self.sprites.add(self.background)
        
        
    def run(self) :
        self.playing = True 
        self.drag = False
        
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
            
            #Quit
            if event.type == pg.QUIT :
                self.quit()
            elif event.type == pg.KEYDOWN :
                if event.key == pg.K_ESCAPE :
                    self.quit()
                    
            #Mouse 
            elif event.type == pg.MOUSEBUTTONDOWN :
                if event.button == 1 :
                    if self.cards.rect.collidepoint(event.pos) :
                        self.drag = True
                        self.pos_X, self.pos_Y = event.pos
                        self.s_X, self.s_Y = (self.cards.rect.x, self.cards.rect.y)
                        self.offset_X = self.s_X - self.pos_X 
                        self.offset_Y = self.s_Y - self.pos_Y  
                                     
            elif event.type == pg.MOUSEBUTTONUP : 
                if event.button == 1 :
                    self.drag = False 
                 
            elif event.type == pg.MOUSEMOTION : 
                if self.drag : 
                    self.pos_X, self.pos_Y = event.pos

                    self.cards.rect.x = self.offset_X + self.pos_X 
                    self.cards.rect.y = self.offset_Y + self.pos_Y        

        
                    
    def update(self) :
        pg.display.update()
        pg.display.flip() #draw 
        
    def draw(self) :
        self.screen.fill(BLACK)
        self.screen.blit(self.background.image, self.background.rect)
        self.screen.blit(self.cards.image, self.cards.rect)
 
        self.clock.tick(FPS)


#run
baccarat = Baccarat()
baccarat.run()
