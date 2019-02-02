#Copyright@roseline124

import random

"""
Users
"""
class User :
    
    def __init__(self, seed_money) :
        self.earnings = 0 
        self.seed_money = seed_money 
        self.grade = 'Bronze'
        self.score = int(round(self.earnings))
        
    def rank(self) :
        if self.score <= 1000000 :
            self.grade = 'Bronze'
        elif self.score <= 5000000 : 
            self.grade = 'Platinum'
        elif self.score <= 10000000 : 
            self.grade = 'Diamond'
        elif self.score <= 25000000 : 
            self.grade = 'Master'
        elif self.score > 50000000 : 
            self.grade = 'Grand Master'
            
        return self.grade

"""
Players
"""
class Player : 
    
    def __init__(self, name) :
        
        self.name = name
        self.cards = []
        self.score = 0
        self.value = 'Nothing'
        self.record = {'win' : 0, 'lose' : 0, 'pair' : 0, 'tie' : 0 }

class Betting_table :
    
    def __init__(self) :
        self.bet_table = {'player' : 0,
                          'player_pair' : 0, 
                          'banker' : 0,
                          'banker_pair' : 0,
                          'tie' : 0,} 

    def bet(self, user) :
        #user betting 
        print("[1. Player 2. Player pair 3. Banker 4. Banker pair 5. Tie]\n",
                  "-------------------------------------------\n",
                  "Your Capital : %d 원\n" %(user.seed_money),
                  "Please bet your money")
        
        for k in self.bet_table :
            self.bet_table[k] = int(input("%s :" %k))
            user.seed_money -= self.bet_table[k] 
            
        return self.bet_table, user.seed_money

class Card_table : 
    
    def __init__(self) :
        self.deck = {'Ace' : 1, 
                    2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9, 
                    10:0, 'J':0, 'Q':0, 'K':0}

    def draw(self, player) :
        print("Draw!")
        
        self.card = random.sample(self.deck.keys(), 1)
        player.cards.append(self.card[0])

        print(player.cards)
        
        return player.cards 

    #game class로 옮기기 
    def one_more(self, player, banker) :
        
        #player's 'one more card'
        self.draw(player)

        #banker's 'one more card'
        if banker.score <= 2 : 
            self.draw(banker)

        elif (banker.score == 3) & (player.cards[2] != 8) :
            self.draw(banker)

        elif (banker.score == 4) & (player.cards[2] in range(2,8)) :
            self.draw(banker)

        elif (banker.score == 5) & (player.cards[2] in range(4,8)) :
            self.draw(banker)

        elif (banker.score == 6) & (player.cards[2] in range(6,8)) :
            self.draw(banker)
        
        return player.cards, banker.cards


class Score_table(Card_table) : #record_table은 따로   
    
    def __init__(self, deck) :
        self.deck = deck
    
    def count(self, player) :
        self.num = [0,0,0]
        
        for i in range(2) : 
            self.num[i] = self.deck[player.cards[i]]
        
        self.card_sum = sum(self.num)%10
        player.score = self.card_sum
        
        return player.score, self.num

    def check_value(self, player) :
        #Natural
        if player.score >= 8 :
            player.value = 'natural'
        
        #Stand
        elif player.score >= 6 : 
            if (player.name == 'banker') & (player.score==6) :
                player.value = 'nothing'
                
            else : 
                player.value = 'stand'
                    
        #Nothing 
        else : 
            player.value = 'nothing'
            
        return player.value

class Record_table : 
    
    def __init__(self) :
        self.winner = ''
        self.pair = ''
        self.tie = False

    #player means 'player' only in this function
    def record_game(self, player, banker) :
        
        #win & lose
        if player.score > banker.score : 
            player.record['win'] += 1
            banker.record['lose'] += 1
            self.winner = player.name
            
        elif player.score < banker.score :
            player.record['lose'] += 1
            banker.record['win'] += 1
            self.winner = banker.name

        #tie
        elif player.score == banker.score :
            player.record['tie'] += 1
            banker.record['tie'] += 1
            self.tie = True

        #pair
        if player.cards[0] == player.cards[1] :
            player.record['pair'] += 1
            self.pair = player.name

        elif banker.cards[0] == banker.cards[1] :
            banker.record['pair'] += 1
            self.pair = banker.name
            
        return player.record, banker.record, self.winner

class Cash_table(Betting_table, Record_table) :
    
    def __init__(self, bet_table, winner, tie, pair) :
        self.bet_table = bet_table
        self.winner = winner
        self.tie = tie
        self.pair = pair
    
    def pay(self, user) :
        
        #win & lose
        if self.winner == 'player' : 
            user.earnings += self.bet_table['player']*2
            
        elif self.winner == 'banker' :
            user.earnings += self.bet_table['banker']*1.95
            
        #tie
        elif self.tie == True : 
            user.earnings += self.bet_table['tie']*8
        
        #pair
        if self.pair=='player' :
            user.earnings += self.bet_table['plaeyr_pair']*11
        elif self.pair=='banker' :
            user.earnings += self.bet_table['banker_pair']*11
            
        user.seed_money += user.earnings
            
        return user.seed_money 
