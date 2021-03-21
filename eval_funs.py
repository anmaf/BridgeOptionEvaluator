from itertools import combinations, groupby
# import pandas as pd
import PySimpleGUI as sg
from tabulate import tabulate

def get_opponent_cards(hand_1, hand_3, card_list):
    return [f for f in card_list if f not in hand_1 + hand_3]

def get_opponent_hands(opponent_cards):
    W_hands = []
    E_hands = []
    for k in range(len(opponent_cards)+1):
        W_hands_k = [list(x) for x in combinations(opponent_cards, k)]
        W_hands += W_hands_k
        E_hands += [list(set(opponent_cards) - set(x)) for x in W_hands_k]
    return W_hands, E_hands


def play_hand_2(card_1, hand_2, hand_3):
    #     print([card_1] + hand_3)
    opp_max = max([card_1] + hand_3)
    if len(hand_2) == 0:
        to_play = 0
    elif (card_1 >= 10 and card_1 + 1 in hand_2 and card_1 + 2 in hand_3):
        to_play = card_1 + 1
    elif max(hand_2) > opp_max:
        to_play = min([x for x in hand_2 if x > opp_max])
    else:
        to_play = min(hand_2)
    return to_play


def play_hand_4(card_1, card_2, card_3, hand_4):
    opp_max = max([card_1, card_3])
    if len(hand_4) == 0:
        to_play = 0
    elif card_2 < opp_max and max(hand_4) > opp_max:
        to_play = min([x for x in hand_4 if x > opp_max])
    else:
        to_play = min(hand_4)
    return to_play


def play_hand_1(card, hand):
    if len(hand) == 0:
        to_play = 0
    elif card == 'small':
        to_play = min(hand)
    elif card == 'reg':
        to_play = max(hand)
    else:
        to_play = card
    return to_play


def play_hand_3(card_1, card_2, card_3, finesse, hand_3, hand_4=[]):
    #     print(card_2, card_3)
    if len(hand_3) == 0:
        to_play = 0
    elif card_3 == 'small':
        to_play = min(hand_3)
    elif card_3 == 'reg':
        opp_max = max([card_2] + hand_4)
        if card_1 < opp_max and max(hand_3) > opp_max:
            to_play = min([x for x in hand_3 if x > opp_max])
        else:
            to_play = min(hand_3)
    elif card_2 > card_3 and not finesse:
        to_play = min(hand_3)
    elif finesse:
        if card_2 > max([card_3, card_1]) and max(hand_3) > card_2:
            to_play = min([x for x in hand_3 if x > card_2])
        else:
            to_play = card_3
    else:
        to_play = card_3 if card_3 in hand_3 else max(hand_3)
    return to_play


def declarer_trick(card_1, card_2, card_3, card_4):
    return (max([card_1, card_2, card_3, card_4]) in [card_1, card_3]) * 1


def make_trick(trick_plan, hand_1, hand_2, hand_3, hand_4):
    start_hand, card_1, card_3, finesse = trick_plan
    if start_hand == 1:
        h1, h2, h3, h4 = hand_1, hand_2, hand_3, hand_4
    else:
        h1, h2, h3, h4 = hand_3, hand_4, hand_1, hand_2
    played_card_1 = play_hand_1(card_1, h1)
    played_card_2 = play_hand_2(played_card_1, h2, h3)
    played_card_3 = play_hand_3(played_card_1, played_card_2, card_3, finesse, h3, h4)
    played_card_4 = play_hand_4(played_card_1, played_card_2, played_card_3, h4)
    return played_card_1, played_card_2, played_card_3, played_card_4


def update_hands(trick_plan, card_1, card_2, card_3, card_4, hand_1, hand_2, hand_3, hand_4):
    if trick_plan[0] == 1:
        c1, c2, c3, c4 = card_1, card_2, card_3, card_4
    else:
        c1, c2, c3, c4 = card_3, card_4, card_1, card_2
    new_hand_1 = [x for x in hand_1 if x != c1]
    new_hand_2 = [x for x in hand_2 if x != c2]
    new_hand_3 = [x for x in hand_3 if x != c3]
    new_hand_4 = [x for x in hand_4 if x != c4]
    return new_hand_1, new_hand_2, new_hand_3, new_hand_4


def run_plan(play_plan, hand_1, hand_2, hand_3, hand_4, show_tricks = True, show_hands = True):
    count_tricks = max(len(hand_1), len(hand_3))
    tricks_taken = 0
    H1, H2, H3, H4 = hand_1, hand_2, hand_3, hand_4
    print('---------------------------------------------------------')
    print('Starting hands: \n{}'.format([bridge_notation(h) for h in [hand_1, hand_2, hand_3, hand_4]]))
    i = 0
    while i < count_tricks:
        if i < len(play_plan):
            trick_plan = play_plan[i]
        else:
            if i < len(hand_1):
                trick_plan = (1, 'reg', 'reg', 0)
            else:
                trick_plan = (3, 'reg', 'reg', 0)
        C1, C2, C3, C4 = make_trick(trick_plan, H1, H2, H3, H4)
        played_cards = [bridge_notation(c) for c in [[C1], [C2], [C3], [C4]]]
        if show_tricks:
            print('T{}: {}'.format(i+1, [item for sublist in played_cards for item in sublist]))
        tricks_taken += declarer_trick(C1, C2, C3, C4)
        # print(tricks_taken)
        H1, H2, H3, H4 = update_hands(trick_plan, C1, C2, C3, C4, H1, H2, H3, H4)
        if show_hands:
            print([bridge_notation(h) for h in [H1, H2, H3, H4]])
        i += 1
    print('Tricks taken by declarer: {}'.format(tricks_taken))
    return tricks_taken


def bridge_notation(hand, sort_items=True):
    BN_hand = hand.copy()
    sign_dict = {11: 'J', 12: 'Q', 13: 'K', 14: 'A'}
    if sort_items:
        BN_hand.sort(reverse=True)
    for j in range(len(hand)):
        if BN_hand[j] in [11, 12, 13, 14]:
            BN_hand[j] = sign_dict[BN_hand[j]]
    return BN_hand


def CountFrequency(my_list):
    # Creating an empty dictionary
    freq = {}
    for item in my_list:
        if (item in freq):
            freq[item] += 1
        else:
            freq[item] = 1
    return freq


def process_data(play_plan, hand_1, hand_3, card_list = list(range(2,15)), show_tricks = True, show_hands = True):
    opponent_cards = get_opponent_cards(hand_1, hand_3, card_list)
    opp_hands_2, opp_hands_4 = get_opponent_hands(opponent_cards)
    plan_results = []
    for H2, H4 in zip(opp_hands_2, opp_hands_4):
        plan_results += [run_plan(play_plan, hand_1, H2, hand_3, H4, \
                                  show_tricks=show_tricks, show_hands=show_hands)]
    # df_results = (pd.Series(plan_results).value_counts() / len(opp_hands_2)).reset_index()
    # df_results.columns = ['Tricks', 'Freq']
    # print(tabulate(df_results.sort_values('Tricks', ascending=False), \
    #         headers = df_results.columns, showindex=False, tablefmt='psql', colalign=['center', 'decimal']))
    results = [[key, "{:.2%}".format(len(list(group))/len(plan_results))] \
               for key, group in groupby(sorted(plan_results))]
    results.sort(key=lambda x: -x[0])
    result_columns = ['Tricks', 'Freq']
    print(tabulate(results, headers = result_columns, \
                   tablefmt='psql', colalign=['center', 'decimal']))
    return
    # return df_results

def convert_bridge_notation(BN_hand):
    reverse_sign_dict = {'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    hand = BN_hand.copy()
    for j in range(len(hand)):
        if BN_hand[j] in 'AKQJ':
            hand[j] = reverse_sign_dict[BN_hand[j]]
        elif BN_hand[j] not in ['small', 'reg', '-']:
            hand[j] = int(hand[j])
    return hand

def run_hand_checks(s_hand, n_hand):
    return len([x for x in s_hand if x in n_hand])==0

def run_hand_len_checks(s_hand, n_hand):
    return len(s_hand) + len(n_hand) >= 7

def run_plan_checks(hand, card1, card3, first_hand = False):
    no_missings = hand != '-' and card1 != '-' and card3 != '-'
    all_missing = hand == '-' and card1 == '-' and card3 == '-'
    if first_hand:
        return no_missings
    else:
        return no_missings or all_missing

def run_input_checks(input_values):
    ok_hands = run_hand_checks(input_values['S_hand'], input_values['N_hand'])
    if not ok_hands:
        sg.popup('Duplicated cards in input')
        return False
    ok_len_hands = run_hand_len_checks(input_values['S_hand'], input_values['N_hand'])
    if not ok_len_hands:
        sg.popup('Less than 7 cards in 2 hands')
        return False
    ok_plan1 = run_plan_checks(input_values['hand1'], input_values['card11'], input_values['card31'], first_hand=True)
    ok_plan2 = run_plan_checks(input_values['hand2'], input_values['card12'], input_values['card32'])
    ok_plan3 = run_plan_checks(input_values['hand3'], input_values['card13'], input_values['card33'])
    if not (ok_plan1 and ok_plan2 and ok_plan3):
        sg.popup('Missed input in play plan')
        return False
    return True

def assign_hands(hand):
    if hand == 'S':
        return 1
    elif hand == 'N':
        return 3
    else:
        return 0

def strip_form_notation(input_list):
    return [x.strip('...') for x in input_list]

def make_play_plan(input_values):
    play_plan = list()
    print_play_plan = list()
    for i,j in enumerate(['1', '2', '3']):
        hand = assign_hands(input_values['hand'+j])
        if hand > 0:
            card1 = convert_bridge_notation([input_values['card1'+j]])[0]
            card3 = convert_bridge_notation([input_values['card3'+j]])[0]
            finesse = input_values['cb'+j]
            # print(hand, card1, card3, finesse)
            print_play_plan.append((input_values['hand'+j], input_values['card1'+j], \
                                   input_values['card3'+j], input_values['cb'+j]))
            play_plan.append((hand, card1, card3, finesse))
    return print_play_plan, play_plan

