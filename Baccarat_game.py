#Copyright@ roseline124

from Baccarat_resources import *

if __name__ == "__main__" :

    #users
    user = User(100*10000)

    #players
    player = Player('player')
    banker = Player('banker')

    #betting
    btb = Betting_table()
    btb.bet(user)

    #drawing
    ctb=Card_table()
    player.cards = ctb.draw(player)
    banker.cards = ctb.draw(banker)
    player.cards = ctb.draw(player)
    banker.cards = ctb.draw(banker)

    #scoring
    stb = Score_table(ctb.deck)
    stb.count(player)
    stb.count(banker)
    stb.check_value(player)
    stb.check_value(banker)

    #one more drawing?
    if (player.value == 'nothing') & (banker.value == 'nothing') :
        print("-------------------------------------------\n",
              "One more card!")

        ctb.one_more(player, banker)
    
    #scoring again
    stb.count(player)
    stb.count(banker)
    
    #recording game 
    rtb = Record_table()
    rtb.record_game(player, banker)
    
    #paying
    cash_tb = Cash_table(btb.bet_table, rtb.winner, rtb.tie, rtb.pair)
    cash_tb.pay(user)

    print("-------------------------------------------\n"
          "User score : %d\n" %user.score,
          "User money : %d\n" %user.seed_money,
          "User grade : %s\n" %user.grade,)

