import logging
from poker_game.utils.next_player import get_next_player

# Retrieve the already configured logger
logger = logging.getLogger('poker_game')

def clean_up(table):
    logger.debug(f'cleaning time for players {[player.name for player in table.players]}')
    
    # remove losers and pass on dealer button
    # get the dealer location, this has to happen here because:
    # dealer could be the one left
    # but also the next could

    # num_players = len(table.players)
    
    # # get the index of the current dealer
    # current_index_dealer = next((i for i, player in enumerate(table.players) if player == table.dealer), None)
    # if current_index_dealer is None:
    #     AssertionError()

    # # get the next player in the list who has more than 0 chips
    # # % is the modulo operator that loops around to 0
    # next_index = (current_index_dealer + 1) % num_players

    # # loop over the players until you find the next player with chips
    # while next_index != current_index_dealer:
    #     if table.players[next_index].chips.amount > 0:
    #         logger.debug(f"The next player is {table.players[next_index].name}.")
    #         table.dealer = table.players[next_index]
    #     next_index = (next_index + 1) % num_players
    
    # Get the next dealer
    table.dealer = get_next_player(starting_players=table.starting_players, active_players=table.players_game, current_player=table.dealer)
    if table.dealer.folded == True: AssertionError()

    # loop over a copy of the list and remove all the people without money
    for player in table.players[:]:
        logger.debug(f"{player.name} has {player.chips.amount} chips left")
        logger.info(f"{player.name}-chips-{player.chips.amount}")
        player.hand = []
        player.total_bet_betting_round = 0
        player.folded = False
        player.all_in = False
        if player.chips.amount == 0:
            table.players.remove(player)
            logger.debug(f"{player.name} has no chips left and leaves the table crying")
    # Create a new list that only includes the players you want to keep
    table.players_game = table.players
    table.community_cards = []
    table.pots = []
    # table.players = [player for player in table.players if player.chips.amount > 0]
    if len(table.players) == 1:
        return None
    # move dealer button --> needs to be refactored