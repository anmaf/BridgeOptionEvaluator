import PySimpleGUI as sg
from eval_funs import *
from layout import window

# Loop forever reading the window's values, updating the Input field

def run_eval():
    while True:
        event, values = window.read()  # read the window
        if event == sg.WIN_CLOSED:  # if the X button clicked, just exit
            break
        if event == 'Clear':  # clear keys if clear button
            window['S_hand'].SetValue([])
            window['N_hand'].SetValue([])
            for hand_id in ['1', '2', '3']:
                window['hand' + hand_id].Update('-')
                window['cb' + hand_id].Update(False)
            for card_id in ['11', '12', '13', '31', '32', '33']:
                window['card' + card_id].Update('-')
        if event == 'ClearOut':
            window['OUTPUT'].Update('')
        elif event == 'Submit':
            if run_input_checks(values):
                S_hand = convert_bridge_notation(
                    strip_form_notation(values['S_hand']))
                N_hand = convert_bridge_notation(
                    strip_form_notation(values['N_hand']))
                print_play_plan, play_plan = make_play_plan(values)
                print('Play plan: {}'.format(print_play_plan))
                process_data(
                    play_plan,
                    S_hand,
                    N_hand,
                    show_tricks=values['cb_tricks'],
                    show_hands=values['cb_hands'])
            else:
                pass
    return
