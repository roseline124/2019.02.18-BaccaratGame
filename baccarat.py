# coding = utf-8
import sys
import pygame as pg
from settings import *
from tables import *
from sprites import *
from pygame.locals import *
import time

#Baccarat.py
class Baccarat : 
    def __init__(self) :
        pg.init()
        pg.display.set_caption('Baccarat')
        self.screen = pg.display.set_mode(SCREEN_SIZE)
        self.clock = pg.time.Clock()
    
    def new(self) : #init sprites

        """init index equals blit index"""
        self.all_sprites = pg.sprite.Group() #sprites.group
        self.card_sprites = pg.sprite.Group() 
        self.flag_sprites = pg.sprite.Group() 
        self.background = Background(self, 'image/background_image.png', (0,0))
        
        #gamers
        self.user = User()
        self.player = Player('player')
        self.banker = Player('banker')

        #chip's value #orange(1), green(5), red(50), blue(100), black(500)
        self.chips_list = [ Chips(self, PLAY_CHIPS[chip]) for chip in PLAY_CHIPS ]

        #chip's image
        for i in range(len(self.chips_list)) : 
            self.chips_list[i].make( ('image/'+list(PLAY_CHIPS.keys())[i]+'.png'), CHIP_LOCATIONS[i]  ) 
        
        #tables
        self.card_table = Card_Table(self)
        self.score_table = Score_Table(self)
        self.record_table = Record_table(self)
        self.cash_table = Cash_Table(self)


        #betting tables 
        self.tb_list = [Bet_Table(self,('image/tb_'+BET_OPTIONS[i]+'.png'), BETTING_POS[i]) for i in range(5)]
        self.betting_table = {}

        for k,v in zip(self.tb_list, BET_OPTIONS) :
            self.betting_table[k] = v 
        
        #dealed cards
        self.card_list = list(map(lambda n : self.card_table.deal(n), [self.player, self.banker, self.player, self.banker ]))
        self.card_list = [Card(self, ('image/card_'+str(self.card_list[i])+'.png'), CARD_LOCATIONS[i][0]) for i in range(4)]

        #trigger button #write func, instead of func()
        self.finish_btn = Button(self, 'image/finish_btn.png', FIN_BTN_LOCATION, FIN_BTN_SIZE)

        self.flag = Flag(self, 'image/winner_flag.png')


    def run(self) :
        print("run again")
        self.new()
        self.playing = True 
        self.paused = False 
        #control this game
        self.deal_finished = False
        self.need_one_more = False
        self.game_over = False 
        self.full_drew = False
        self.is_announced = False
        self.is_created = False

        while self.playing : 

            self.dt = self.clock.tick(FPS) / 1000
            pg.time.delay(100) #pause ms the program for more accuracy 
            self.events()
            self.update()
            self.draw()

            #play again?
            if self.game_over & (self.is_created==False) : 
                #Yes or No Button
                self.yes_btn = Button(self, 'image/yes_btn.png', YES_BTN_LOCATION, YES_NO_BTN_SIZE, self.run) 
                self.no_btn = Button(self, 'image/no_btn.png', NO_BTN_LOCATION, YES_NO_BTN_SIZE, self.quit) 
                self.is_created = True 

                # if self.play_again() : 
                    # self.run()
                # else:
                    # break


    def quit(self) :
        pg.quit()
        sys.exit()
    
    def events(self) :
        self.get_events = pg.event.get()
        for event in self.get_events :
            
            #Quit
            if event.type == pg.QUIT :
                self.quit()
            elif event.type == pg.KEYDOWN :
                if event.key == pg.K_ESCAPE :
                    self.quit()
            else : 
                return self.get_events

    def update(self) :
        self.all_sprites.update()
        self.card_sprites.update()
        self.score_table.update()
        self.card_table.update()
        self.record_table.update()
        self.cash_table.update()
        self.flag_sprites.update()
        pg.display.flip() #draw 
        
    def draw(self) :
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)

        #deal card
        if self.finish_btn.is_clicked :
            self.card_sprites.draw(self.screen)
            self.deal_finished = True 

        #count score
        if self.score_table.is_counted : 
            self.screen.blit(self.score_table.text_p_score, P_SCORE_LOCATION)
            self.screen.blit(self.score_table.text_b_score, B_SCORE_LOCATION)

        #check value
        if self.score_table.is_checked : 
            self.screen.blit(self.score_table.text_p_value, P_VALUE_LOCATION)
            self.screen.blit(self.score_table.text_b_value, B_VALUE_LOCATION)

        #one more card
        if (self.card_table.hand_is_full) & (self.full_drew==False): 
            self.full_drew = True
            self.card_list.append(Card(self, ('image/card_'+str(self.player.cards[2])+'.png'), CARD_LOCATIONS[4][0],is_normal=False))
            
            if len(self.banker.cards) == 3 : 
                self.card_list.append(Card(self, ('image/card_'+str(self.banker.cards[2])+'.png'), CARD_LOCATIONS[5][0],is_normal=False))

        #record : show winner


if __name__ == "__main__":
    baccarat = Baccarat()

    baccarat.run()