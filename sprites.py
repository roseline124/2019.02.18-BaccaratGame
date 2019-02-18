from settings import *
import sys 
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


class User(pg.sprite.Sprite) :
    def __init__(self) :
        pg.sprite.Sprite.__init__(self)
        self.earnings = 0
        self.loss = 0

    def get_score(self, earnings, loss) :
        USER_PROFILE['SCORE'] += int(round(earnings))
        USER_PROFILE['SCORE'] -= loss 
        
        return USER_PROFILE['SCORE']

    def rank(self) :
        if USER_PROFILE['SCORE'] <= 150000 :
            USER_PROFILE['GRADE'] = 'Bronze'
        elif USER_PROFILE['SCORE'] <= 250000 : 
            USER_PROFILE['GRADE'] = 'GOLD'
        elif USER_PROFILE['SCORE'] <= 500000 : 
            USER_PROFILE['GRADE'] = 'Platinum'
        elif USER_PROFILE['SCORE'] <= 1000000 : 
            USER_PROFILE['GRADE'] = 'Diamond'
        elif USER_PROFILE['SCORE'] <= 2500000 : 
            USER_PROFILE['GRADE'] = 'Master'
        elif USER_PROFILE['SCORE'] > 5000000 : 
            USER_PROFILE['GRADE'] = 'Grand Master'

        return USER_PROFILE['GRADE']
            
class Chips(pg.sprite.Sprite) :
    def __init__(self, game, chips) :
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)  #자기 자신과 baccarat로 부터 받은 그룹 초기화
        self.game = game 
        self.chip = chips
        self.drag = False
        self.is_betted = False
        self.is_selected = False
    
    def make(self, image_file, location) :
        self.image = pg.image.load(image_file)
        self.image = pg.transform.scale(self.image,CHIP_SIZE)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = location 

    def bet(self, tb_dict) : 
        self.is_selected = False

        if self.rect.collidedict(tb_dict) :
            if self.is_betted == False : 
                self.is_betted = True 
                self.tb = self.rect.collidedict(tb_dict)

                CURRENT_BET[self.tb[1]] += self.chip #베팅 금액 테이블에 올리기
                USER_PROFILE['SEED_MONEY'] -= self.chip
                print(CURRENT_BET,"|", USER_PROFILE['SEED_MONEY'])
    
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
    def __init__(self, game, image_file, call_func=None, args=None) :
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game 
        self.is_clicked = False
        self.image = pg.image.load(image_file)
        self.image = pg.transform.scale(self.image, BTN_SIZE)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = BTN_LOCATION

        #this button is trigger to call func() with args 
        self.func = call_func 
        self.args = args
 
    def clicked(self) :
        """if button is clicked, return 1 / else return 0 """
        if self.is_clicked == False : 
            self.is_clicked = True

            if self.func != None :
                self.func(self.args)

    def update(self) :
        for event in self.game.get_events : 
            if event.type == pg.MOUSEBUTTONDOWN : 
                if (self.rect.collidepoint(event.pos)) & (event.button == 1) : 
                    self.clicked() 

class Flag(pg.sprite.Sprite) :
    def __init__(self, game, image_file) :
        self.groups = game.flag_sprites
        pg.sprite.Sprite.__init__(self, self.groups) 
        self.game = game

        self.image = pg.image.load(image_file)
        self.image = pg.transform.scale(self.image, FLAG_SIZE)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = FLAG_BLIND_LOCATION
        self.vy = 0 
      
    def move_to(self) :
        """move from blind_location to flag_location"""
        self.vy = 0 

        if (self.game.game_over) & (self.game.is_announced == False): 
            self.vy = +FLAG_SPEED if self.rect.y < FLAG_LOCATION[1] else 0 
            self.game.is_announced = True if self.rect.y > FLAG_LOCATION[1] else False

        if self.vy != 0 : 
            self.vy*= VY_TIME

    def update(self) :
        self.move_to()
        self.rect.y += self.vy*self.game.dt 

