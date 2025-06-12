import random

class Card:
    def __init__(self, rank, suit):
        self.suit = suit
        self.rank = rank
    def __eq__(self, other):
        return (self.suit == other.suit) and (self.rank == other.rank)


class Deck:
    def __init__(self, suits, ranks):
        self.suits = suits
        self.ranks = ranks
        self.cards = self._create_deck()

    def _create_deck(self):
        return [Card(rank, suit) for rank in self.ranks for suit in self.suits]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, num_cards):
        dealt_cards = []
        if num_cards > len(self.cards):
            num_cards = len(self.cards)
        for i in range(num_cards):
            dealt_cards.append(self.cards.pop())
        return dealt_cards


class GameCrazyEights:
    def __init__(self,the_players,deck):
        self.num_players = len(the_players)
        self.the_players = the_players
        self.deck = deck
        self.player_hands = self._deal_hands()
        #Put the rest of the deck in draw pile so just say 52.
        self.draw_pile = self.deck.deal(52)
        #Empty discard pile
        self.discard_pile = []
        self.next_suit = None
        self.player_turn = None
        self.game_start = True

    def _deal_hands(self):
        num_cards = 5
        hands = {}
        if self.num_players == 2:
            num_cards = 7
        for a_player in self.the_players:
            hands[a_player] = self.deck.deal(num_cards)
        return hands

    def flip_first_card(self):
        #Make sure this is the first move
        if len(self.discard_pile) > 0:
            raise Exception("Not the first move!")
        self.discard_pile.append(self.draw_pile.pop())
        self.next_suit = self.discard_pile[-1].suit

    def discard_card(self, a_player, the_card):
        #Make sure we have something to match
        if len(self.discard_pile) == 0:
            raise Exception("Nothing in discard!")
        #Check Rules
        if (the_card.suit == self.next_suit) or (the_card.rank == self.discard_pile[-1].rank):
            self.discard_pile.append(the_card)
            self.player_hands[a_player].remove(the_card)
            self.next_suit = the_card.suit
        elif the_card.rank == "8":
            self.discard_pile.append(the_card)
            self.player_hands[a_player].remove(the_card)
            self.next_suit = None
        else:
            raise Exception("Illegal Move!")

    def draw_card(self, the_player):
        #if the draw pile is empty refresh it from discard.
        if len(self.draw_pile) == 0:
            self.draw_pile = self.discard_pile[0:-1]
            del self.discard_pile[0:-1]
            self.draw_pile.shuffle()
        self.player_hands[the_player].append(self.draw_pile.pop())
    
        

french_suits = ["H", "D", "C", "S"]
card_ranks_52_ace_high = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
card_ranks_52_ace_low = ["A","2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]




