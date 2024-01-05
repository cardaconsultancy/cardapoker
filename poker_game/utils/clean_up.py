import logging
logger = logging.getLogger(__name__)

def clean_up(table):
    logger.debug(f'cleaning time for players {[player.name for player in table.players]}')
    
    """
    Gets the next player in the list who has more than 0 chips.
    """
    # remove losers and pass on dealer button
    # get the dealer location, this has to happen here because:
    # dealer could be the one left
    # but also the next could

    num_players = len(table.players)
    
    current_index_dealer = next((i for i, player in enumerate(table.players) if player == table.dealer), None)
    if current_index_dealer is None:
        AssertionError()

    next_index = (current_index_dealer + 1) % num_players

    while next_index != current_index_dealer:
        if table.players_game[next_index].chips.amount > 0:
            logger.debug(f"The next player is {table.players[next_index].name}.")
            table.dealer = table.players[next_index]
        next_index = (next_index + 1) % num_players
    
    # loop over a copy of the list and remove all the people without money
    for player in table.players[:]:
        logger.debug(f"{player.name} has {player.chips.amount} chips left")
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