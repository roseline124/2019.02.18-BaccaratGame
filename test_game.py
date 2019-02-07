#coding = utf-8
import sys, pygame
from pygame.locals import *

pygame.init()
win=pygame.display.set_mode((800,400))
pygame.display.set_caption("Baccarat")
run=True

while run : 
    pygame.time.delay(100)
    
    for event in pygame.event.get() :
        if event.type == pygame.QUIT : 
            run = False 
            
    #characters
    pygame.draw.rect(win, (255,0,0), (50,50,40,60)) #win 디스플레이에 캐릭터
    
    #update
    pygame.display.update()
            
pygame.quit()