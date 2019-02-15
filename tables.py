from settings import *
import sys 
import pygame as pg
import random

class Bet_Table(pg.sprite.Sprite) :
    def __init__(self, game, image_file, location) :
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        
        self.image = pg.image.load(image_file)
        self.image = pg.transform.scale(self.image,TB_SIZE)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = location

class Card_Table(pg.sprite.Sprite) :
    def __init__(self) :
        pg.sprite.Sprite.__init__(self)

    def deal(self, player) :
        self.card = random.sample(DECK.keys(), 1)
        player.cards.append(self.card[0])
       
        # print(player.role,"Draw |", player.cards)
        return self.card[0]

    #one_more_card 
    def one_more(self, player, banker) :
        #player's 'one more card'
        self.deal(player)

        #banker's 'one more card'
        if banker.score <= 2 : 
            self.deal(banker)
        elif (banker.score == 3) & (player.cards[2] != 8) :
            self.deal(banker)
        elif (banker.score == 4) & (player.cards[2] in range(2,8)) :
            self.deal(banker)
        elif (banker.score == 5) & (player.cards[2] in range(4,8)) :
            self.deal(banker)
        elif (banker.score == 6) & (player.cards[2] in range(6,8)) :
            self.deal(banker)
        print("player one more :", player.cards)
        print("banker one more :", player.cards)


class Score_Table(pg.sprite.Sprite) :
    def __init__(self) :
        pg.sprite.Sprite.__init__(self)

    def count(self, player) :
        self.num = [0,0,0]
        
        for i in range(2) : 
            self.num[i] = DECK[player.cards[i]]
        
        self.card_sum = sum(self.num)%10
        player.score = self.card_sum

    def check_value(self, player) :
        #Natural
        if player.score >= 8 :
            player.value = 'natural'
        
        #Stand
        elif player.score >= 6 : 
            if (player.role == 'banker') & (player.score==6) :
                player.value = 'nothing'
            else : 
                player.value = 'stand'
                    
        #Nothing 
        else : 
            player.value = 'nothing'


class Record_table(pg.sprite.Sprite) : 
    def __init__(self) :
        pg.sprite.Sprite.__init__(self)

    def record(self, player, banker) :
        #win & lose
        if player.score > banker.score : 
            player.record['win'] += 1
            banker.record['lose'] += 1
            CURRENT_RECORD['winner'] = player.role
            
        elif player.score < banker.score :
            player.record['lose'] += 1
            banker.record['win'] += 1
            CURRENT_RECORD['winner'] = banker.role

        #tie
        elif player.score == banker.score :
            player.record['tie'] += 1
            banker.record['tie'] += 1
            CURRENT_RECORD['tie'] = True

        #pair
        if player.cards[0] == player.cards[1] :
            player.record['pair'] += 1
            CURRENT_RECORD['player_pair'] = True

        if banker.cards[0] == banker.cards[1] :
            banker.record['pair'] += 1
            CURRENT_RECORD['banker_pair'] = True


class Cash_Table(pg.sprite.Sprite) :
    def __init__(self) :
        pg.sprite.Sprite.__init__(self)
    
    def pay(self, user) :
        #win & lose
        if CURRENT_RECORD['winner'] == 'player' : 
            user.earnings += CURRENT_BET['player']*2
            CURRENT_BET['player'] = 0
        elif CURRENT_RECORD['winner'] == 'banker' :
            user.earnings += CURRENT_BET['banker']*1.95
            CURRENT_BET['banker'] = 0
            
        #tie
        elif CURRENT_RECORD['tie'] == True : 
            user.earnings += CURRENT_BET['tie']*8
            CURRENT_BET['tie'] = 0
        
        #pair
        if CURRENT_RECORD['player_pair']==True :
            user.earnings += CURRENT_BET['player_pair']*11
            CURRENT_BET['player_pair'] = 0
        
        if CURRENT_RECORD['banker_pair']==True :
            user.earnings += CURRENT_BET['banker_pair']*11
            CURRENT_BET['banker_pair'] = 0
      
        USER_PROFILE['SEED_MONEY'] += user.earnings
        user.loss = sum(CURRENT_BET.values())
        print("you got", user.earnings,"!")
        print("you lost", user.loss,"!")
        print("your money :", USER_PROFILE['SEED_MONEY'])

