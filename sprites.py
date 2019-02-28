from settings import *
from user_profile import *
import sys, pickle
import pygame as pg

class Background(pg.sprite.Sprite):
    def __init__(self, game, image_file, location):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)

        self.image = pg.image.load(image_file)
        self.image = pg.transform.scale(self.image,SCREEN_SIZE)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = location
        
class Player(pg.sprite.Sprite) : 
    def __init__(self, role) :
        pg.sprite.Sprite.__init__(self)
        self.role = role
        self.cards = []
        self.score = 0
        self.value = ''
        self.record = {'win' : 0, 'lose' : 0, 'pair' : 0, 'tie' : 0 }  

class Chips(pg.sprite.Sprite) :
    def __init__(self, game, chips_price) :
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)  #자기 자신과 baccarat로 부터 받은 그룹 초기화
        self.game = game 
        self.chip_price = chips_price
        self.drag = False
        self.is_betted = False
        self.is_selected = False
        self.location = None
    
    def make(self, image_file, location) :
        self.image = pg.image.load(image_file)
        self.image = pg.transform.scale(self.image,CHIP_SIZE)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = location 
        self.location = location


    def bet(self, tb_dict) : 
        self.is_selected = False

        if self.rect.collidedict(tb_dict) :
            if self.is_betted == False : 
                self.is_betted = True 
                self.tb = self.rect.collidedict(tb_dict)

                CURRENT_BET[self.tb[1]] += self.chip_price #베팅 금액 테이블에 올리기
                self.game.user.seed_money -= self.chip_price
                print(CURRENT_BET,"|", self.game.user.seed_money)
    
    def mouse_down(self, event_pos) :
        if self.rect.collidepoint(event_pos) :
            self.is_selected=True
            self.pos_X, self.pos_Y = event_pos
            self.offset_X = self.rect.x - self.pos_X 
            self.offset_Y = self.rect.y - self.pos_Y 

            return self.offset_X, self.offset_Y

    def mouse_drag(self, event_pos, offset):
        if self.is_selected :
            self.pos_X, self.pos_Y = event_pos

            self.rect.x = offset[0] + self.pos_X 
            self.rect.y = offset[1] + self.pos_Y 

    def update(self) :

        for event in self.game.get_events :
            if event.type == pg.MOUSEBUTTONDOWN :
                if event.button == 1 : #event type이 mouse인 경우에만 button 요소가 생기므로 if문 안에 써주는 게 맞다. 
                    self.drag = True
                    self.offset = self.mouse_down(event.pos) 

            elif event.type == pg.MOUSEBUTTONUP : 
                if event.button == 1 : 
                    self.drag = False

                    if self.game.finish_btn.is_clicked == False : 
                        self.bet(self.game.betting_table)

                        if self.is_betted :
                            new_chip = Chips(self.game, self.chip_price)

                            chip_name = [c_name for c_name in PLAY_CHIPS if PLAY_CHIPS[c_name] == self.chip_price][0] 
                            new_chip.make(('image/'+chip_name+'.png'), self.location)

            elif event.type == pg.MOUSEMOTION  : 

                if self.drag : 
                    self.mouse_drag(event.pos, self.offset)



class Card(pg.sprite.Sprite) :
    def __init__(self, game, image_file, card_location, is_normal=True) :
        self.groups = game.card_sprites
        pg.sprite.Sprite.__init__(self, self.groups) #초기화해야 self.groups_list에 추가된다. 
        self.groups_list = game.card_sprites.sprites()
        self.game = game

        self.image = pg.image.load(image_file)
        self.image = pg.transform.scale(self.image, CARD_SIZE)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = BLIND_LOCATION
        self.destination = card_location
        self.vx = 0 
      
        if is_normal == False : 
            self.image = pg.transform.rotate(self.image, 90)
            self.rect.x, self.rect.y = ONE_MORE_CARD_BLIND_LOCATION

    def move_to(self) :
        """move from blind_location to card_location"""
        self.vx = 0 

        if self.game.deal_finished : 
            self.vx = -CARD_SPEED if self.rect.x > self.destination else 0 

        if self.vx != 0 : 
            self.vx*= VX_TIME

    def update(self) :
        self.move_to()
        self.rect.x += self.vx*self.game.dt 

class Button(pg.sprite.Sprite) :
    def __init__(self, game, image_file, location, size, call_func=None, args=None) :
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game 
        self.is_clicked = False
        self.image = pg.image.load(image_file)
        self.image = pg.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = location

        #this button is trigger to call func() with args 
        self.func = call_func 
        self.args = args
 
    def clicked(self) :
        """if button is clicked, return 1 / else return 0 """
        if self.is_clicked == False : 
            self.is_clicked = True

            if self.func != None :
                if self.args != None : 
                    self.func(self.args)
                else : 
                    self.func()

    def update(self) :
        for event in self.game.get_events : 
            if event.type == pg.MOUSEBUTTONDOWN : 
                if (self.rect.collidepoint(event.pos)) & (event.button == 1) : 
                    self.clicked() 
