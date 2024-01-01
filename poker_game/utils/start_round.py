from poker_game.utils.at_most_one_not_all_in_or_folded import check_at_most_one_not_all_in_or_folded
from poker_game.utils.betting_round import betting_round
from poker_game.utils.clean_up import clean_up
from poker_game.utils.get_and_pay_winners import pay_winners
from poker_game.utils.objects_on_table import Deck
from poker_game.utils.pot_management import check_if_rest_folded_and_pay
import logging

logger = logging.getLogger(__name__)

def start_round(table, seed=None):
    # reset the deck
    deck = Deck(seed=seed)

    # Reset community cards at the beginning of each round
    table.community_cards = []

    # print the dealer button
    logger.debug(f"the dealer is {table.dealer.name}.")

    # copy the player list to easily keep track of players
    # create a temporary deque to easily rotate 
    table.players_game = table.players
    # table.players_game.rotate(-table.small_blind_seat)
    # table.players_game = list(table.players)

    # Deal two private cards to each player
    # (Chosen to stay the closest to the real game, by not dealing two at once)
    for player in table.players_game:
        player.receive_card(deck.deal())
    for player in table.players_game:
        player.receive_card(deck.deal())

    # Betting Round 1
    logger.debug(f"Players can make their first bet.")
    betting_round(table, preflop_round=True)
    if check_if_rest_folded_and_pay(table) == True:
        return True
    
    logger.debug(f"Bets are made") 
    logger.debug(f"Total betted {sum(player.total_in_pots_this_game for player in table.players)}.")

    # Deal the flop (three community cards)
    table.community_cards.append(deck.deal())
    table.community_cards.append(deck.deal())
    table.community_cards.append(deck.deal())
    for card in table.community_cards:
        logger.debug(f"On the table comes {card.rank} of {card.suit}.")

    # Betting Round 2: flop
    if check_at_most_one_not_all_in_or_folded:
        print('Everybody is all in, no more bets!')
    
    else:
        logger.debug(f"Players can bet on the flop.")
        betting_round(table)
        logger.debug(f"Total is {sum(player.total_in_pots_this_game for player in table.players)}.")
    
    if check_if_rest_folded_and_pay(table):
        return True
    
    # Deal the turn (one additional community card)
    table.community_cards.append(deck.deal())
    logger.debug(f"On the table comes {table.community_cards[3].rank} of {table.community_cards[3].suit}.") 

    # Betting Round 3
    if check_at_most_one_not_all_in_or_folded:
        print('Everybody is all in, no more bets!')
    
    else:
        logger.debug(f"Players can bet on the flop.")
        betting_round(table)
        logger.debug(f"Total is {sum(player.total_in_pots_this_game for player in table.players)}.")
    
    if check_if_rest_folded_and_pay(table):
        return True
    
    # Deal the river (one final community card)
    table.community_cards.append(deck.deal())
    logger.debug(f"On the table comes {table.community_cards[4].rank} of {table.community_cards[4].suit}.") 

    # Betting Round 4
    if check_at_most_one_not_all_in_or_folded:
        print('Everybody is all in, no more bets!')
    
    else:
        logger.debug(f"Players can bet on the river, final bet!")
        betting_round(table)
        logger.debug(f"Total is {sum(player.total_in_pots_this_game for player in table.players)}.")
    
    if check_if_rest_folded_and_pay(table):
        return True
    
    # Determine the winner(s)
    logger.debug(f"Pay_the_winner(s)")
    pay_winners(table)

    # Clean up
    clean_up(table)

    return table