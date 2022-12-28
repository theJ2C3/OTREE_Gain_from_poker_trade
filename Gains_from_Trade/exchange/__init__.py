from otree.api import *
import random
from collections import defaultdict

from cardcalculate import *
###################################################################################
#               need this for calculate many card based things                    #
###################################################################################

from io import BytesIO
from base64 import b64encode
import urllib
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator
import matplotlib
import matplotlib.patches as mpatches
import matplotlib.font_manager as fm
import numpy as np
# font = fm.FontProperties(fname='c:\\windows\\fonts\\simsun.ttc')  # speicify font
font = fm.FontProperties(fname='_static/global/simsun.ttc')  # speicify font
matplotlib.use('Agg')
doc = """
gains from trade
"""

class C(BaseConstants):
    NAME_IN_URL = 'exchange'
    INSTRUCTIONS_TEMPLATE = 'exchange/instructions.html'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 2
    # NumOfCardsRecieved = 7
    NumOfCardsRecieved = 5
    NumOfCardsPlayable = 5

class Subsession(BaseSubsession):
    strsolo = models.StringField(initial="")
    strcoop = models.StringField()
    pass

def creating_session(subsession):
    subsession.group_randomly()

class Group(BaseGroup):
    card_deck = models.LongStringField(initial= initial_card())
    deal = models.BooleanField(initial=False)
    pass

class Player(BasePlayer):
    switch_yet = models.IntegerField(initial=0)

    # cards_received = models.StringField(initial="101102103104105")
    cards_received = models.StringField(initial= serve_card(random.randint(0,3),C.NumOfCardsRecieved))
    card_choose = models.StringField(initial= "000")
    card_switched = models.StringField(initial= "000")
    card_get_for_deal = models.StringField(initial= "000")
    card_after_switched = models.StringField(initial= "000")
    # card_received = models.LongStringField()
    # card_chosen =  tool_models.MultipleChoiceModelField(label="Please select the three correct statements",
    # cards_received_gp = models.StringField(initial= serve_card(random.randint(0,3),C.NumOfCardsRecieved))
    # cards_received_gp=card_after_switched
    # need to be update
    card_choose_gp = models.StringField(initial= "000")
    card_switched_gp = models.StringField(initial= "000")
    card_get_for_deal_gp = models.StringField(initial= "000")
    card_after_switched_gp = models.StringField(initial= "000")
                                                            #   min_choices=C.NumOfCardsPlayable, max_choices=C.NumOfCardsPlayable)
    PY_solo = models.CurrencyField(initial=0)
    PY_coop = models.CurrencyField(initial=0)
    PY_gp = models.CurrencyField(initial=0)
    carddet_solo = models.StringField()
    carddet_coop = models.StringField()
    carddet_gp = models.StringField()
    
    pass

# FUNCTIONS
 

def check_switch_card_amount(group:Group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)

    if len(p1.card_switched) == len(p2.card_switched) and len(p2.card_switched) !=0:
        return True
    else:
        return False

def handing_cards(player:Player):
    l1 = s2c(player.card_choose)
    l2 = s2c(player.card_switched)
    l3 = [x for x in l1 if x not in l2]
    panother = player.group.get_others_in_group()[0]
    l4 = s2c(panother.card_switched)
    l3 +=l4
    player.card_after_switched = c2s(l3)

def set_payoff(player:Player):
    player.payoff = (player.PY_coop)+ (player.PY_solo)

def create_figure(player:Player):
    collect_num(player)
    if player.round_number == C.NUM_ROUNDS:
        # point_distribution =[ [_ for i in range(2)] for j in range(C.PLAYERS_PER_GROUP * len(player.group.get_players()))]
        # https://python-ecw.com/2020/05/29/python-matplotlib%E6%95%99%E5%AD%B8-%E5%85%A5%E9%96%80-%E6%95%A3%E4%BD%88%E5%9C%96/
        # 有需要將一班地跟有額外報酬分開來的情況可以參考這邊
        
        subsession = player.subsession

        solodta = subsession.strsolo
        coopdta = subsession.strcoop

        soloarray = []
        cooparray = []

        length = len(coopdta);   
        chars = 2
        for i in range(0, length, chars):  
            soloarray.append(int(solodta[ i : i+chars]))
            cooparray.append(int(coopdta[ i : i+chars]))
        # print(soloarray,cooparray)

        maxvalue = int(max(cooparray))

        # plt.clf()
        
        plt.figure(figsize=(5, 5))

        plt.scatter(soloarray, cooparray, color="blue")

        fig = plt.gcf()

        plt.xlabel("自行選擇牌後的報酬", fontproperties=font)
        plt.ylabel("有交易選項後的報酬", fontproperties=font)
        plt.title("報酬分布圖", fontproperties=font)    
        plt.xlim(0, maxvalue+20)
        plt.ylim(0, maxvalue+20)
        x = np.linspace(0, maxvalue+20, 1000)
        plt.plot(x, x)
        
        plt.plot([0, 0], [maxvalue +20, maxvalue +20],color="red")
        # plt.yticks(ylabel)
        # plt.xticks(xdata,xlabel)

        buf = BytesIO()        
        fig.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)

        string = b64encode(buf.read())

        return urllib.parse.quote(string)
    else:
        plt.figure(figsize=(7, 3))
        fig = plt.gcf()
        buf = BytesIO()        
        fig.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        string = b64encode(buf.read())
        # draw nothing
        return urllib.parse.quote(string)

def collect_num(player: Player):
    if player.round_number == C.NUM_ROUNDS:
        subsession = player.subsession
        solo = ""
        coop = ""
        for j in range(C.NUM_ROUNDS):
            for p in subsession.get_players():
                solo += str(int(p.in_round(j+1).PY_solo)).zfill(2)
                coop += str(int(p.in_round(j+1).PY_coop)).zfill(2)
        subsession.strsolo = solo 
        subsession.strcoop = coop 


def deal_cards(player: Player):
    deck = s2c(player.group.card_deck)
    # print(deck)
    id = player.id_in_group
    player.cards_received = str(c2s(deck[(id-1)*C.NumOfCardsRecieved:(id)*C.NumOfCardsRecieved]))

# PAGES

class Introduction(Page):
    def is_displayed(player: Player):
        player.group.card_deck =  initial_card()
        deal_cards(player)
        print(player.id_in_group, player.cards_received)
        return player.round_number == 1

class solo(Page):
    @staticmethod
    def js_vars(player:Player):
        return dict(
        cardrecieved = s2c(player.cards_received),
        getcardnum = C.NumOfCardsRecieved,
        havecardnum = C.NumOfCardsPlayable,
        py_solo = player.PY_solo,
        id = player.id_in_group
        )

    @staticmethod
    def live_method(player:Player, data):
        
        if data["information_type"] == "cards":
            player.card_choose = data["cards"]
            temp, player.carddet_solo = check_cu(s2c(player.card_choose))
            player.PY_solo = cu(temp*5)
            return {player.id_in_group:{"information_type": "py", "payoff" :player.PY_solo, "cardset" : player.carddet_solo }}
            
        # 這邊要計算並回傳cu
    pass
    # https://stackoverflow.com/questions/72243659/how-to-make-input-checkbox-update-price-total-using-values-include-additional

class ResultsWaitPage(WaitPage):
    pass

class pairexchange(Page):

    @staticmethod
    def js_vars(player:Player):
        return dict(
        cardchoose = s2c(player.card_choose),
        getcardnum = C.NumOfCardsRecieved,
        havecardnum = C.NumOfCardsPlayable,
        # chosen_yet = player.chosen_yet,
        # chosen_yet = 0,
        py_coop = player.PY_coop,
        card_get_for_deal = s2c(player.field_maybe_none("card_get_for_deal"))
        )

    @staticmethod
    def live_method(player:Player, data):
        another = player.get_others_in_group()[0]
        anotherid = another.id_in_group
        if data["information_type"] == "push":
            player.card_switched = data["cards"]
            player.switch_yet = 1
            # print("another",anotherid)
            # print(player.group.id_in_subsession,":", player.switch_yet, another.switch_yet)

            if player.switch_yet == 1 and another.switch_yet ==1:
                if check_switch_card_amount(player.group):
                    player.card_get_for_deal = another.card_switched
                    another.card_get_for_deal = player.card_switched
                    # print(player.card_get_for_deal, another.card_get_for_deal)
                    return {player.id_in_group:{"information_type": "offer", "samecardamount" :1, "offercard" : s2c(player.card_get_for_deal)}, 
                    anotherid:{"information_type": "offer", "samecardamount" :1, "offercard" :s2c(another.card_get_for_deal)}
                    }
                    # return {player.id_in_group:{"information_type": "py", "payoff" :player.PY_solo, "cardset" : player.carddet_solo }}
                else : 
                    # print("offer", False)
                    temp, player.carddet_coop = check_cu(s2c(player.card_choose))
                    player.PY_coop = cu(temp*5)
                    temp, another.carddet_coop = check_cu(s2c(another.card_choose))
                    another.PY_coop = cu(temp*5)
                    
                    return {player.id_in_group:{"information_type": "offer", "samecardamount" :0, "cardset" : player.carddet_coop, "payoff" :player.PY_coop }, 
                    anotherid:{"information_type": "offer", "samecardamount" :0, "cardset" : another.carddet_coop,"payoff" :another.PY_coop}
                    }
            else:
                print(" ")


        if data["information_type"] == "respond":
            # player.card_switched = data["cards"]
            player.switch_yet = 2
            if player.switch_yet == 2 and another.switch_yet ==2:
                if data["deal"] == "accepted":
                    # print("deal", True)
                    player.card_after_switched = c2s(list(set(s2c(player.card_choose)) - set(s2c(player.card_switched))))+   player.card_get_for_deal
                    another.card_after_switched = c2s(list(set(s2c(another.card_choose)) - set(s2c(another.card_switched))))+another.card_get_for_deal
                    print(player.id_in_group, player.card_after_switched, another.card_after_switched)
                    temp, player.carddet_coop = check_cu(s2c(player.card_after_switched))
                    player.PY_coop = cu(temp*5)
                    temp, another.carddet_coop = check_cu(s2c(another.card_after_switched))
                    another.PY_coop = cu(temp*5)
                    print(player.id_in_group, player.PY_coop,another.PY_coop)

                    return {player.id_in_group:{"information_type": "deal", "deal" :1, "cardset" : player.carddet_coop, "payoff" :player.PY_coop}, 
                    anotherid:{"information_type": "deal", "deal" :1, "cardset" :another.carddet_coop, "payoff" :another.PY_coop}
                    }
                else : 
                    # print("deal", True)
                    temp, player.carddet_coop = check_cu(s2c(player.card_choose))
                    player.PY_coop = cu(temp*5)
                    temp, another.carddet_coop = check_cu(s2c(another.card_choose))
                    another.PY_coop = cu(temp*5)
                    
                    return {player.id_in_group:{"information_type": "deal", "deal" :0, "cardset" : player.carddet_coop, "payoff" :player.PY_coop}, 
                    anotherid:{"information_type": "deal", "deal" :0, "cardset" : another.carddet_coop, "payoff" :another.PY_coop}
                    }
            else:
                return{player.id_in_group: "",
                anotherid:""}

    pass

# class ResultsWaitPage(WaitPage):
#     pass

class Results(Page):
    def is_displayed(player: Player):
        set_payoff(player)
        return player.round_number == C.NUM_ROUNDS
    def vars_for_template(player: Player):
        return {'my_img' : create_figure(player)}
    pass

page_sequence = [
    Introduction, 
    solo, 
    ResultsWaitPage, 
    pairexchange, 
    Results]
# page_sequence = [solo, ResultsWaitPage, groupexchange, Results]
# page_sequence = [solo, ResultsWaitPage, Results]
# page_sequence = [MyPage, Results]


# def card_set_type(value):
#     if value == 5:
#         return "一組對子"
#     if value == 10:
#         return "兩組對子"
#     if value == 15:
#         return "三條"
#     if value == 20:
#         return "順子"
#     if value == 25:
#         return "同花"
#     if value == 5:
#         return "葫蘆"
#     if value == 5:
#         return "鐵支"
#     if value == 5:
#         return "同花順"