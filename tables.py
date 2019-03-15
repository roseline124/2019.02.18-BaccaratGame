from settings import *
from user_profile import *
import sys, random 
import pygame as pg

class Bet_Table(pg.sprite.Sprite) :
    def __init__(self, game, image_file, location) :
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.text = pg.font.SysFont('arial', 20)
        self.game = game

        self.image = pg.image.load(image_file)
        self.image = pg.transform.scale(self.image,TB_SIZE)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = location
    
    def show_bet(self) :
        self.bet_money = self.text.render( ("bet money : " + str(sum(CURRENT_BET.values()))),False,BLACK)
        self.curr_money = self.text.render(("current money : "+str(self.game.user.seed_money)),False,BLACK)
        self.grade = self.text.render(("your rank : "+str(self.game.user.grade)), False, BLACK)

        self.game.screen.blit(self.bet_money, USER_PROFILE_LOCATION[0])
        self.game.screen.blit(self.curr_money, USER_PROFILE_LOCATION[1])
        self.game.screen.blit(self.grade, USER_PROFILE_LOCATION[2])

    def update(self) :
        self.show_bet()

class Card_Table(pg.sprite.Sprite) :
    def __init__(self, game) :
        pg.sprite.Sprite.__init__(self)
        self.game = game 
        self.hand_is_full = False 

    def deal(self, player) :
        self.card = random.sample(DECK.keys(), 1)
        player.cards.append(self.card[0])
       
        return self.card[0]

    def one_more(self) :
        
        self.player = self.game.player
        self.banker = self.game.banker

        self.hand_is_full = True

        print("-------------------------------------------\n"+
            "<one more card>")

        #player's 'one more card'
        self.deal(self.player)

        #banker's 'one more card'
        if self.banker.score <= 2 : 
            self.deal(self.banker)
        elif (self.banker.score == 3) & (self.player.cards[2] != 8) :
            self.deal(self.banker)
        elif (self.banker.score == 4) & (self.player.cards[2] in range(2,8)) :
            self.deal(self.banker)
        elif (self.banker.score == 5) & (self.player.cards[2] in range(4,8)) :
            self.deal(self.banker)
        elif (self.banker.score == 6) & (self.player.cards[2] in range(6,8)) :
            self.deal(self.banker)
        print("player one more :", self.player.cards)
        print("banker one more :", self.banker.cards)
        print("-------------------------------------------\n")


    def update(self) :
        if (self.game.need_one_more) & (self.hand_is_full == False): 

            self.one_more()


class Score_Table(pg.sprite.Sprite) :
    def __init__(self, game) :
        pg.font.init()
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.is_counted = False 
        self.is_checked = False 
        self.is_one_more_check = False
        self.text = pg.font.SysFont('arial', 20,bold=1)

    def count(self, player) :
        self.card_num = len(player.cards) #one more card에 대비 
        self.num = [ DECK[player.cards[i]] for i in range(self.card_num) ]

        self.card_sum = sum(self.num)%10
        player.score = self.card_sum

        return self.card_sum


    def check_value(self, player) :
        self.value = '' 

        #Natural
        if player.score >= 8 :
            self.value = 'natural'
        
        #Stand
        elif player.score >= 6 : 
            self.value = 'nothing' if (player.role == 'banker') & (player.score==6) else 'stand'
                    
        #Nothing 
        else : 
            self.value = 'nothing'

        return self.value


    def update(self) :
        if ((self.game.deal_finished) & (self.is_counted == False)) |  ((self.game.full_drew) & (self.is_one_more_check==False)) :
            print("counting")
            self.p_score = self.count(self.game.player)
            self.b_score = self.count(self.game.banker)

            self.text_p_score = self.text.render(('Player Score : '+ str(self.p_score)), False, BLACK)
            self.text_b_score = self.text.render(('Banker Score : '+ str(self.b_score)), False, BLACK)

            self.is_counted = True #role such as 'break' 
            self.is_checked = False # for one more check
            self.is_one_more_check = True if self.game.full_drew else False

        if ((self.is_counted) & (self.is_checked == False)) : 
            print("checking")
            self.p_value = self.check_value(self.game.player)
            self.b_value = self.check_value(self.game.banker)

            self.font_color = RED if self.is_one_more_check else BLACK
            self.cation = "[One]" if self.is_one_more_check else ''

            self.text_p_value = self.text.render((self.cation+'Player Value : '+self.p_value), False, self.font_color)
            self.text_b_value = self.text.render((self.cation+'Banker Value : '+self.b_value), False, self.font_color)

            self.game.need_one_more = True if (self.p_value == 'nothing') & (self.b_value == 'nothing') & (self.is_one_more_check==False) else False
            self.game.game_over = False if self.game.need_one_more else True  

            self.is_checked = True #role such as 'break' 


class Record_table(pg.sprite.Sprite) : 
    def __init__(self, game) :
        self.game = game
        pg.sprite.Sprite.__init__(self)
        self.is_recorded = False
        self.text = pg.font.SysFont('arial', 20, bold=1)

    def record(self) :
        self.player = self.game.player
        self.banker = self.game.banker

        #win & lose
        if self.player.score > self.banker.score : 
            self.player.record['win'] += 1
            self.banker.record['lose'] += 1
            CURRENT_RECORD['winner'] = self.player.role
            
        elif self.player.score < self.banker.score :
            self.player.record['lose'] += 1
            self.banker.record['win'] += 1
            CURRENT_RECORD['winner'] = self.banker.role

        #tie
        elif self.player.score == self.banker.score :
            self.player.record['tie'] += 1
            self.banker.record['tie'] += 1
            CURRENT_RECORD['tie'] = True

        #pair
        if self.player.cards[0] == self.player.cards[1] :
            self.player.record['pair'] += 1
            CURRENT_RECORD['player_pair'] = True

        if self.banker.cards[0] == self.banker.cards[1] :
            self.banker.record['pair'] += 1
            CURRENT_RECORD['banker_pair'] = True

        print(CURRENT_RECORD)

    def update(self):
        if (self.game.game_over) & (self.is_recorded == False) : 
            print("recording")
            self.is_recorded = True
            self.record()


class Cash_Table(pg.sprite.Sprite) :
    def __init__(self, game) :
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.user = self.game.user
        self.text = pg.font.SysFont('arial', 20, bold=1)
        self.is_paid = False 
        

    def pay(self) :
        self.winner = CURRENT_RECORD['winner']
        self.tie = CURRENT_RECORD['tie']
        self.p_pair = CURRENT_RECORD['player_pair']
        self.b_pair = CURRENT_RECORD['banker_pair']

        #win & lose
        if self.winner == 'player' : 
            self.user.earnings += CURRENT_BET['player']*2 
            CURRENT_BET['player'] = 0
        elif self.winner == 'banker' :
            self.user.earnings += CURRENT_BET['banker']*1.95 
            CURRENT_BET['banker'] = 0
            print("winner -- ")
        #tie
        elif self.tie == True : 
            self.user.earnings += CURRENT_BET['tie']*8
            CURRENT_BET['tie'] = 0
            print("tie -- ")

        
        #pair
        if self.p_pair==True :
            self.user.earnings += CURRENT_BET['player_pair']*11
            CURRENT_BET['player_pair'] = 0
        
        if self.b_pair==True :
            self.user.earnings += CURRENT_BET['banker_pair']*11
            CURRENT_BET['banker_pair'] = 0
            print("pair -- ")

        self.user.seed_money += self.user.earnings
        self.user.loss = sum(CURRENT_BET.values())
        self.is_paid = True 
        print("you got", self.user.earnings,"!")
        print("you lost", self.user.loss,"!")

    def show_winner(self) :
        #text
        if self.winner : 
            self.winner = self.text.render("Winner : "+ CURRENT_RECORD['winner'],False, GRAY )
            self.game.screen.blit(self.winner, RECORD_LOCATION[0])
        
        elif self.tie : 
            self.tie = self.text.render("Tie",False, GRAY)
            self.game.screen.blit(self.tie, RECORD_LOCATION[0])
        
        if self.p_pair :
            self.p_pair = self.text.render("Palyer Pair", False, GRAY)
            self.game.screen.blit(self.p_pair, RECORD_LOCATION[0])

        if self.b_pair : 
            self.b_pair = self.text.render("Banker Pair", False, GRAY)
            self.game.screen.blit(self.b_pair, RECORD_LOCATION[0])


    def update(self) :
        if self.game.record_table.is_recorded : 
            self.pay() if self.is_paid == False else self.show_winner()