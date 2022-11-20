from otree.api import *
import random
from cardcalculate import check_straight_flush, check_four_of_a_kind, check_full_house, check_flush, check_straight, check_three_of_a_kind, check_two_pairs, check_one_pairs
# from otree_tools.models import fields as tool_models

doc = """
gains from trade
"""

class C(BaseConstants):
    NAME_IN_URL = 'exchange'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    NumOfCardsRecieved = 5
    NumOfCardsPlayable = 5
    # PY = payoff

    # PY_pair     = cu(5)
    # PY_pairs    = cu(10)
    # PY_tri      = cu(15)
    # PY_straight = cu(20)
    # PY_flush    = cu(25)
    # PY_tripair  = cu(30)
    # PY_quad     = cu(35)
    # PY_SF       = cu(40)

    


class Subsession(BaseSubsession):
    def initial_card(self):

        deck = []
        # suit = [100, 200, 300, 400]
        suit = ["♠", "♥", "♦", "♣"]
        for i in range(13):
            for j in range(4):
                card = str(suit[j] + str((i+1).zfill(2)))
                deck.append(card)
        
        random.shuffle(deck)
        self.card_deck = str(c2s(deck))
    deal = models.BooleanField(initial=0)
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    
    def initial_card_received(self):
        id = int(self.group.get_player_by_id)
        cards = self.pick_cards(self, id)
        self.cards_received = cards

    def pick_cards(self, id):
        get_card= s2c(self.subsession.card_deck)
        chosencard = get_card[id*C.NumOfCardsRecieved, (id +1) C.NumOfCardsRecieved]
        return c2s(chosencard)
    
    card_choose = models.StringField()
    card_switched = models.StringField()

    
    
    # card_received = models.LongStringField()
    # card_chosen =  tool_models.MultipleChoiceModelField(label="Please select the three correct statements",
                                                            #   min_choices=C.NumOfCardsPlayable, max_choices=C.NumOfCardsPlayable)
    PY_solo = models.CurrencyField(default = 0)
    PY_coop = models.CurrencyField(default = 0)
    pass



# FUNCTIONS


# def deal(group: Group):
#     deck = s2c(group.card_deck)
#     group.get_players[0]
#     p1 = group.get_player_by_id("player 1")
#     p2 = group.get_player_by_id("player 2")

#     p1_card_get = deck[:C.NumOfCardsRecieved]
#     deck = deck[C.NumOfCardsRecieved:]
#     p2_card_get = deck[:C.NumOfCardsRecieved]
#     deck = deck[C.NumOfCardsRecieved:]

#     group.card_deck = c2s(deck)
#     p1.card_received = c2s(p1_card_get)
#     p2.card_received = c2s(p2_card_get)
    
    
def c2s(cards):
    # card to string
    cardstring = ""
    for card in cards:
        cardstring += (str(card))
    return cardstring

def s2c(cardstring):
    # string to card
    cards = []
    for i in range(len(cardstring)/3):
        cards.append(''.join(cardstring[i*3,(i+1)*3]))
    return cards

def check_cu(player:Player):
    cards = s2c(player.card_chosen)
    cards2d = [C.NumOfCardsPlayable][2]
    for i in range(C.NumOfCardsPlayable):
        cards2d[i][0] = cards[i]%100
        cards2d[i][1] = cards[i]/100
    # 
    sorted(cards2d,key=lambda x: x[0])

    if check_straight_flush(cards2d):
        return 9
    if check_four_of_a_kind(cards2d):
        return 8
    if check_full_house(cards2d):
        return 7
    if check_flush(cards2d):
        return 6
    if check_straight(cards2d):
        return 5
    if check_three_of_a_kind(cards2d):
        return 4
    if check_two_pairs(cards2d):
        return 3
    if check_one_pairs(cards2d):
        return 2
    return 0

    
# https://briancaffey.github.io/2018/01/02/checking-poker-hands-with-python.html/


# def exchange_card(group:Group):

# def set_payoffs(group: Group):


# def solo_payoff(player: Player):
    # payoff_matrix = {
    #     (False, True): C.PAYOFF_A,
    #     (True, True): C.PAYOFF_B,
    #     (False, False): C.PAYOFF_C,
    #     (True, False): C.PAYOFF_D,
    # }
    # other = other_player(player)
    # player.payoff = payoff_matrix[(player.cooperate, other.cooperate)]
    


# PAGES

class solo(Page):
    form_model = "player"
    form_fields = ["card_choose"]
    
    @staticmethod
    def live_method(player, data):
        if data["information_type"] ==
    pass


class ResultsWaitPage(WaitPage):
    pass

class groupexchange(Page):
    form_model = "player"
    form_fields = ["card_choose"]
    
    @staticmethod
    def live_method(player, data):
        if data["information_type"] ==
    pass



class Results(Page):
    pass


page_sequence = [solo, ResultsWaitPage, Results]
# page_sequence = [MyPage, Results]