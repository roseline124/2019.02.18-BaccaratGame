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
        self.value = 'Nothing'
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
        self.chip = chips
        self.is_betted = False
        self.is_selected = False
    
    def new(self, image_file, location) :
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

class Card(pg.sprite.Sprite) :
    def __init__(self, game, image_file) :
        self.groups = game.card_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.image.load(image_file)
        self.image = pg.transform.scale(self.image, CARD_SIZE)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = BLIND_LOCATION

    def draw(self, game) :
        game.screen.blit(self.image, self.rect)

    def rotate(self, sprite_image) :
        pg.transform.rotate(sprite_image, 90)

    def move(self) :
        """move from blind_location to card_location"""
        self.rect.x -=10

class Button(pg.sprite.Sprite) :
    def __init__(self, game, image_file) :
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.is_clicked = False
        self.image = pg.image.load(image_file)
        self.image = pg.transform.scale(self.image, BTN_SIZE)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = BTN_LOCATION
 
    def clicked(self, event_pos) :
        """if button is clicked, return 1 / else return 0 """
        if (self.rect.collidepoint(event_pos)) & (self.is_clicked == False):
            self.is_clicked = True 
            return 1
        else :
            return 0 

    # def clicked(self, event_pos, func, args) :
    #     """if button is clicked, return 1 / else return 0 """
    #     if (self.rect.collidepoint(event_pos)) & (self.is_clicked == False):
    #         print("------------------------")
    #         self.is_clicked = True 
    #         func(args)
    #         return 1
    #     else :
    #         return 0 