import PySimpleGUI as sg
from config import *

sg.theme('Dark Green 5')
col1 = [[sg.Text('S hand', font=fontAb)], \
        [sg.Listbox(values = BN_form_card_list, no_scrollbar = True, select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, \
                    font=fontA, size=(5,13), key = 'S_hand')]]
col2 = [[sg.Text('N hand', font=fontAb)], \
        [sg.Listbox(values = BN_form_card_list, no_scrollbar = True, select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, \
                    font=fontA, size=(5,13), key = 'N_hand')]]
col3 = [[sg.Text('Hand', font=fontAb)], [sg.OptionMenu(values = our_hands_list, default_value='-', key = 'hand1')], \
        [sg.OptionMenu(values = our_hands_list, default_value='-', key = 'hand2')],\
        [sg.OptionMenu(values = our_hands_list, default_value='-', key = 'hand3')]]
col4 = [[sg.Text('Card 1', font=fontAb)], [sg.OptionMenu(values = plan_list, default_value='-', key = 'card11')], \
        [sg.OptionMenu(values = plan_list, default_value='-', key = 'card12')], \
        [sg.OptionMenu(values = plan_list, default_value='-', key = 'card13')]]
col5 = [[sg.Text('Card 3', font=fontAb)], [sg.OptionMenu(values = plan_list, default_value='-', key = 'card31')],\
        [sg.OptionMenu(values = plan_list, default_value='-', key = 'card32')], \
        [sg.OptionMenu(values = plan_list, default_value='-', key = 'card33')]]
col6 = [[sg.Text('Finesse', font=fontAb)],[sg.Checkbox('', key = 'cb1')], [sg.Checkbox('', key = 'cb2')],\
        [sg.Checkbox('', key = 'cb3')]]

layout = [[sg.Column(col1, element_justification='c'), sg.VSeparator(), sg.Column(col2, element_justification='c')],\
          [sg.Column(col3, element_justification='c'), sg.Column(col4, element_justification='c'),\
           sg.Column(col5, element_justification='c'), sg.Column(col6, element_justification='c')], \
          [sg.Checkbox('Show tricks', font=fontA, default=True, key = 'cb_tricks'), \
           sg.Checkbox('Show hands after each trick', font = fontA, default=False, key = 'cb_hands')],\
          [sg.Button('Submit', button_color=button_colors, font = fontAb, key = 'Submit'), \
            sg.Button('Clear', button_color=button_colors, font = fontAb, key = 'Clear'), \
           sg.Button('Clear output', button_color=button_colors, font=fontAb, key='ClearOut')],\
          [sg.Output(size=(40,10), echo_stdout_stderr = echo_in_console,  font=fontA, key='OUTPUT')]]

window = sg.Window(
    'Bridge Option Evaluator', layout, default_button_element_size=(4, 2), font=fontA)