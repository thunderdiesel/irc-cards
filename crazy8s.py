from sopel import plugin
import cards

# To Do: Make errors in class surface, make errors here exceptions

# follow command by two nicks to play
# To Do: Make sure enough players specified
@plugin.command('start8s')
def start8s(bot, trigger):
    the_deck = cards.Deck(cards.french_suits, cards.card_ranks_52_ace_high)
    the_deck.shuffle()
    players = []
    for player_nick_arg in trigger.groups()[2:5]:
        if player_nick_arg:
            players.append(player_nick_arg)
    bot.say("Eights: "+str(players))
    bot.memory['eights_game'] = cards.GameCrazyEights(players,the_deck)
    #iterate through player hands and nicks
    for a_player in bot.memory['eights_game'].player_hands:
        #print(str(the_hand) + ' ' + player_nick) 
        hand_output = ''
        for the_card in bot.memory['eights_game'].player_hands[a_player]:
            hand_output += the_card.rank+the_card.suit+' '
        #bot.say("Eights: "+hand_output, a_player)
        #For debugging also put the hand in the main channel
        bot.say("Eights: "+a_player+" "+hand_output)
    #Flip first card, if it's an eight, the first player must choose a suit.
    bot.memory['eights_game'].flip_first_card()
    bot.say("Eights: "+bot.memory['eights_game'].discard_pile[-1].rank+bot.memory['eights_game'].discard_pile[-1].suit)
    #Clear next_suit if discard pile has an eight
    if bot.memory['eights_game'].discard_pile[-1].rank == "8":
        bot.say("Eights: First player must choose suit with .wild8s")
        bot.memory['eights_game'].next_suit = None
    bot.memory['eights_game'].player_turn = players[0]
    bot.say("Eights: Next turn is for "+bot.memory['eights_game'].player_turn)

@plugin.command('wild8s')
def wild8s(bot, trigger):
    if bot.memory['eights_game'] is None:
        bot.say("Eights: No game running!")
        return
    if trigger.nick != bot.memory['eights_game'].player_turn:
        bot.say("Eights: It is not your turn!")
        return
    if bot.memory['eights_game'].discard_pile[-1].rank == "8":
        if trigger.groups()[2] in cards.french_suits:
            bot.memory['eights_game'].next_suit = trigger.groups()[2]
            bot.say(f"Eights: {trigger.nick} has declared the suit to be {bot.memory['eights_game'].next_suit}!")
            if bot.memory['eights_game'].game_start is False:
                #Set turn to next player
                #I should use functions to set all these vars shouldn't I?
                current_player_index = bot.memory['eights_game'].the_players.index(bot.memory['eights_game'].player_turn)
                if current_player_index < bot.memory['eights_game'].num_players - 1:
                    bot.memory['eights_game'].player_turn = bot.memory['eights_game'].the_players[current_player_index + 1]
                else:
                    bot.memory['eights_game'].player_turn = bot.memory['eights_game'].the_players[0]
                return
        else:
            bot.say("Eights: Invalid suit!")
            return
    else:
        bot.say("Eights: No wild card!")
        return

@plugin.command('disc8s')
def disc8s(bot,trigger):
    if bot.memory['eights_game'] is None:
        bot.say("Eights: No game running!")
        return
    if trigger.nick != bot.memory['eights_game'].player_turn:
        bot.say("Eights: It is not your turn!")
        return
    if bot.memory['eights_game'].next_suit is None:
        bot.say("Eights: Suit not declared!")
    cmd_rank = trigger.groups()[2]
    cmd_suit = trigger.groups()[3]
    cmd_card = cards.Card(cmd_rank, cmd_suit)
    if cmd_card in bot.memory['eights_game'].player_hands[str(trigger.nick)]:  
        bot.say("Eights: Card in hand!")
        bot.memory['eights_game'].discard_card(str(trigger.nick), cmd_card)
        bot.memory['eights_game'].game_start = False
        if len(bot.memory['eights_game'].player_hands[str(trigger.nick)]) == 0:
            bot.say(str(trigger.nick)+" has won!")
            del bot.memory['eights_game']
        #For debugging also put the hand in the main channel
        bot.say("Eights: "+bot.memory['eights_game'].discard_pile[-1].rank+bot.memory['eights_game'].discard_pile[-1].suit)
        #Check if it's an 8 (next_suit will have been cleared) and inform players. If not, advance turn.
        if bot.memory['eights_game'].next_suit is None:
            bot.say("Eights: Current player must choose suit with .wild8s")
            return
        else:
            #Set turn to next player
            #I should use functions to set all these vars shouldn't I?
            current_player_index = bot.memory['eights_game'].the_players.index(bot.memory['eights_game'].player_turn)
            if current_player_index < bot.memory['eights_game'].num_players - 1:
                bot.memory['eights_game'].player_turn = bot.memory['eights_game'].the_players[current_player_index + 1]
            else:
                bot.memory['eights_game'].player_turn = bot.memory['eights_game'].the_players[0]
        hand_output = ''
        for the_card in bot.memory['eights_game'].player_hands[bot.memory['eights_game'].player_turn]:
            hand_output += the_card.rank+the_card.suit+' '
        bot.say("Eights: "+bot.memory['eights_game'].player_turn+" "+hand_output)
        bot.say("Eights: Next turn is for "+bot.memory['eights_game'].player_turn)
    else:
        bot.say("Eights: Card not in hand!")

#Should add a check to see if you need to draw, although it harms you.
@plugin.command('draw8s')
def draw8s(bot,trigger):
    if str(trigger.nick) != bot.memory['eights_game'].player_turn:
        bot.say("Eights: It is not your turn!")
        return
    bot.memory['eights_game'].draw_card(str(trigger.nick))
    hand_output = ''
    for the_card in bot.memory['eights_game'].player_hands[bot.memory['eights_game'].player_turn]:
        hand_output += the_card.rank+the_card.suit+' '
    bot.say("Eights: "+bot.memory['eights_game'].player_turn+" "+hand_output)    
