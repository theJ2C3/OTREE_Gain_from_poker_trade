from collections import defaultdict
import random

def initial_card():
    deck = []
    suit = [100, 200, 300, 400]
    for i in range(13):
        for j in range(4):
            card = int(suit[j] + i+1)
            deck.append(card)
    
    random.shuffle(deck)
    returnitem = str(c2s(deck))
    # return models.StringField(returnitem)
    return returnitem

def serve_card(ramnum, NumOfCardsRecieved):
    deck = []
    suit = [100, 200, 300, 400]
    for i in range(13):
        for j in range(4):
            card = int(suit[j] + i+1)
            deck.append(card)
    
    random.shuffle(deck)
    returnitem = str(c2s(deck[ramnum*NumOfCardsRecieved:(ramnum+1)*NumOfCardsRecieved]))
    # return models.StringField(returnitem)
    return returnitem

def c2s(cards):
    # card to string
    cardstring = ""
    for card in cards:
        cardstring += (str(card))
    return cardstring

def s2c(cardstring):
    if cardstring is None:
        return ""
    length = len(cardstring);   
    chars = 3
    # Stores the array of string  
    equalStr = []
    # Check whether a string can be divided into n equal parts  
    if (length % chars ==0):
        for i in range(0, length, chars):  
            equalStr.append(cardstring[ i : i+chars])
            # part = str[ i : i+chars]
            # equalStr.append(part)
    return equalStr


def check_cu(cards):
    # cards = s2c(player.card_choose) ===set as input
    cards2d =[[0 for i in range(2)] for j in range(len(cards))]

    # https://briancaffey.github.io/2018/01/02/checking-poker-hands-with-python.html/
    for i in range(len(cards)):
        cards2d[i][1] = int(cards[i])%100
        cards2d[i][0] = int(cards[i])//100

    if check_straight_flush(cards2d):
        return (8, "同花順")
    if check_four_of_a_kind(cards2d):
        return (7, "鐵支")
    if check_full_house(cards2d):
        return (6 , "葫蘆")
    if check_flush(cards2d):
        return (5, "同花")
    if check_straight(cards2d):
        return (4,"順子")
    if check_three_of_a_kind(cards2d):
        return (3, "三條")
    if check_two_pairs(cards2d):
        return (2, "兩組對子")
    if check_one_pairs(cards2d):
        return 1, "一組對子"
    return 0, ""


def check_straight_flush(hand):
    if check_flush(hand) and check_straight(hand):
        return True
    else:
        return False

def check_four_of_a_kind(hand):
    values = [i[1] for i in hand]
    value_counts = defaultdict(lambda:0)
    for v in values:
        value_counts[v]+=1
    if sorted(value_counts.values()) == [1,4]:
        return True
    return False

def check_full_house(hand):
    values = [i[1] for i in hand]
    value_counts = defaultdict(lambda:0)
    for v in values:
        value_counts[v]+=1
    if sorted(value_counts.values()) == [2,3]:
        return True
    return False

def check_flush(hand):
    suits = [i[0] for i in hand]
    if len(set(suits))==1:
        return True
    else:
        return False

def check_straight(hand):
    values = [i[1] for i in hand]
    value_counts = defaultdict(lambda:0)
    for v in values:
        value_counts[v] += 1
    rank_values = [i for i in values]
    value_range = max(rank_values) - min(rank_values)
    if len(set(value_counts.values())) == 1 and (value_range==4):
        return True
    else:
        #check straight with low Ace
        if set(values) == set(["A", "2", "3", "4", "5"]):
            return True
        return False

def check_three_of_a_kind(hand):
    values = [i[1] for i in hand]
    value_counts = defaultdict(lambda:0)
    for v in values:
        value_counts[v]+=1
    if set(value_counts.values()) == set([3,1]):
        return True
    else:
        return False

def check_two_pairs(hand):
    values = [i[1] for i in hand]
    value_counts = defaultdict(lambda:0)
    for v in values:
        value_counts[v]+=1
    if sorted(value_counts.values())==[1,2,2]:
        return True
    else:
        return False

def check_one_pairs(hand):
    values = [i[1] for i in hand]
    value_counts = defaultdict(lambda:0)
    for v in values:
        value_counts[v]+=1
    if 2 in value_counts.values():
        return True
    else:
        return False



# a = [
# [1,1],
# [1,2],
# [1,3],
# [1,4],
# [1,5]
# ]


# def check_cu(cards2d):
#     if check_straight_flush(cards2d):
#         return 8
#     if check_four_of_a_kind(cards2d):
#         return 7
#     if check_full_house(cards2d):
#         return 6
#     if check_flush(cards2d):
#         return 5
#     if check_straight(cards2d):
#         return 4
#     if check_three_of_a_kind(cards2d):
#         return 3
#     if check_two_pairs(cards2d):
#         return 2
#     if check_one_pairs(cards2d):
#         return 1
#     return 0

# check_cu(a)