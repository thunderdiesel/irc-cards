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
        bot.say("Eights: "+hand_output, a_player)
    #Flip first card, if it's an eight, the first player must choose a suit.
    bot.memory['eights_game'].flip_first_card()
    bot.say("Eights: "+bot.memory['eights_game'].discard_pile[-1].rank+bot.memory['eights_game'].discard_pile[-1].suit)
    if bot.memory['eights_game'].discard_pile[-1].rank == "8":
        bot.say("Eights: First player must choose suit with .wild8s")
    bot.memory['eights_game'].player_turn = players[0]
    bot.say("Eights: Next turn is for "+bot.memory['eights_game'].player_turn)

#ToDo: Suits shouldn't be hard coded
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
                return
        else:
                bot.say("Eights: Invalid suit!")
                return
    else:
        bot.say("Eights: No wild card!")
        return

# ToDo: input validation
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
    else:
        bot.say("Eights: Card not in hand!")
    


