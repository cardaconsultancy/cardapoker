import logging

# Retrieve the already configured logger
logger = logging.getLogger('poker_game')

def get_next_player(current_player, table):
    """
    Don't select on all in as this might be the last_raiser, ending the loop
    """

    # get the number of original players
    num_players = len(table.players_game)


    # search for the current player in the original list of players
    current_index_in_original_list = next((i for i, player in enumerate(table.starting_players) if player == current_player), None)

    namelist = [player.name for player in table.starting_players]
    if current_index_in_original_list is None:
        logger.debug(f'The current player{current_player.name} is not found in the original list of players...{namelist} error!')
    
    # get the next index in the original list of players
    next_index = (current_index_in_original_list + 1) % num_players
    
    # get the next player from the original list of players
    next_player = table.players[next_index]

    while current_player != next_player:
        
        if current_player == next_player: 
            print(f'IT SHOULD STOP HERE RETURN {current_player.name}')
            return None
        
        else:
            # double check if this player is still in the game
            if next_player in table.players_game and not next_player.folded:

                # return the next player in the new list of players
                return next_player

            next_index = (next_index + 1) % num_players
            next_player = table.players_game[next_index]
            if next_player in table.players_game:
                logger.debug(f"_________________The next player is {next_player.name}.")
                return next_player
