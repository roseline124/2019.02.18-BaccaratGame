#Color
BLACK = (0,0,0)

#Size
SCREEN_SIZE = (800,500)
CARD_SIZE = (120,180)
TB_SIZE = (100,150)
CHIP_SIZE = (50,50)
BTN_SIZE = (200,50)

#Position
TB_P_POS = (100,100)
TB_P_PAIR_POS = (210,100)
TB_TIE_POS = (320,100)
TB_B_PAIR_POS = (430,100)
TB_B_POS = (540,100)

#Play chips
ORANGE_CHIP = 1
GREEN_CHIP = 5
RED_CHIP = 50
BLUE_CHIP = 100
BLACK_CHIP = 500 

PLAY_CHIPS = [ORANGE_CHIP, GREEN_CHIP, RED_CHIP, BLUE_CHIP, BLACK_CHIP]

CHIP_LOCATION = [25,400]
CHIP_LOCATION2 = [125,400]
CHIP_LOCATION3 = [225,400]
CHIP_LOCATION4 = [325,400]
CHIP_LOCATION5 = [425,400]

BTN_LOCATION = [550,425]

BLIND_LOCATION = [900, 50]
CARD_LOCATIONS = [
        [50,50],
        [380,50],
        [180,50],
        [510,50],
#One more card (horizontal)
        [50,240],
        [380,240],
]


FPS = 60

#Current_bet 
CURRENT_BET = {
                "player" : 0,
                "player_pair" :0,
                "tie" : 0,
                "banker_pair" : 0,
                "banker" : 0
                }

#Cards Deck
DECK = {
        'Ace' : 1, 
        2:2, 3:3, 
        4:4, 5:5, 
        6:6, 7:7, 
        8:8, 9:9, 
        10:0, 'J':0, 
        'Q':0, 'K':0
        }

#Record 
CURRENT_RECORD = {
        'winner' : '',
        'tie' : False,
        'player_pair' : False,
        'banker_pair' : False
}

USER_PROFILE = {
        'SEED_MONEY' : 100*10000,
        'GRADE' : 'GOLD',
        'SCORE' : 25*10000
}

