import pickle
import pygame as pg

class User(pg.sprite.Sprite) :
    def __init__(self) :
        pg.sprite.Sprite.__init__(self)

        try : 
            self.user_profile = self.load_data()
            self.seed_money = self.user_profile['SEED_MONEY']
            self.grade = self.user_profile['GRADE']
            self.score = self.user_profile['SCORE']
            self.earnings = 0
            self.loss = 0
        
        except TypeError :
            self.__init__() 

    def get_score(self) :
        self.score += int(round(self.earnings))
        self.score -= self.loss 
        
        return self.score

    def get_money(self) :
        self.seed_money += int(round(self.earnings))
        self.seed_money -= self.loss

    def rank(self) :
        if self.score <= 150000 :
            self.grade = 'Bronze'
        elif self.score <= 250000 : 
            self.grade = 'GOLD'
        elif self.score <= 500000 : 
            self.grade = 'Platinum'
        elif self.score <= 1000000 : 
            self.grade = 'Diamond'
        elif self.score <= 2500000 : 
            self.grade = 'Master'
        elif self.score > 5000000 : 
            self.grade = 'Grand Master'

        return self.grade

    def load_data(self) :

        try : 
            with open('data/user_profile.p', "rb") as f :
                LOADED_USER_PROFILE = pickle.load(f)
                print("load:", LOADED_USER_PROFILE)

                return LOADED_USER_PROFILE

        except FileNotFoundError :

            USER_PROFILE = {
                    'SEED_MONEY' : 100*10000,
                    'GRADE' : 'GOLD',
                    'SCORE' : 25*10000,
                }

            with open('data/user_profile.p', 'wb') as f :
                pickle.dump(USER_PROFILE, f)

    def save_data(self) :

        with open('data/user_profile.p', 'wb') as f : 
            SAVE_USER_PROFILE = {'SEED_MONEY' : self.seed_money ,
                            'GRADE' : self.grade,
                            'SCORE' : self.score,
                            }
            
            pickle.dump(SAVE_USER_PROFILE, f)
            print("write:", SAVE_USER_PROFILE)
