from eval_funs import bridge_notation

card_list = list(range(2, 15))
card_type_list = ['small', 'reg', '-']
our_hands_list = ['S', 'N', '-']
fontA = ("Helvetica", 8)
fontAb = ("Helvetica-Bold", 8)
button_colors = ('yellow', 'darkgreen')
echo_in_console = False

BN_card_list = bridge_notation(card_list)
BN_form_card_list = ['...{}...'.format(card) for card in BN_card_list]
plan_list = bridge_notation(card_list) + card_type_list