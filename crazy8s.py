from sopel import plugin
import cards

the_deck = None
player_turn

# follow command by two nicks to play
@plugin.command('start8s')
def start8s(bot, trigger):
    the_deck = cards.Deck(cards.french_suits, cards.card_ranks_52_ace_high)
    the_deck.shuffle()
    players = []
    for player_nick_arg in trigger.groups()[2:5]:
        if player_nick_arg:
            players.append(player_nick_arg)
    bot.say(str(players))
    eights_game = cards.GameCrazyEights(players,the_deck)
    #iterate through player hands and nicks
    for the_hand, player_nick in zip(eights_game.player_hands, players):
        #print(str(the_hand) + ' ' + player_nick) 
        hand_output = ''
        for the_card in the_hand:
            hand_output += the_card.rank+the_card.suit+' '
        bot.say(hand_output, player_nick)
    eights_game.

