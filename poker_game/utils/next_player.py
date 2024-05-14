import logging

logger = logging.getLogger(__name__)

def get_next_player(current_player, table):
    """
    Don't select on all in as this might be the last_raiser, ending the loop
    """

    # get the number of original players
    num_players = len(table.players_game)


    # search for the current player in the original list of players
    current_index_in_original_list = next((i for i, player in enumerate(table.players) if player == current_player), None)


    if current_index_in_original_list is None:
        logger.debug(f"The current player is not found in the original list of players... error")
    
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

    # logger.debug(f"current index: ({current_index} + 1) % {num_players} = {next_index}")
    # logger.debug(f"next index: {next_index}")

    # while next_index != current_index:
        
    #     # if the next player is the last raiser, return None
    #     if next_index == current_index: 
    #         print(f'IT SHOULD STOP HERE RETURN {current_player.name}')
    #         return None
    #     logger.debug(f"1. try next index: {next_index} is not {current_index}")

    #     # if the next player is not folded, return this player, else keep looping
    #     if not table.players_game[next_index].folded:
    #         logger.debug(f"2a. The next player is {table.players_game[next_index].name}.")
    #     else:
    #         next_index = (next_index + 1) % num_players
    #         logger.debug(f"2b.. try next index: {next_index}")
    #         return table.players_game[next_index]

    # return the last raiser if it turns out to be the only one, to end the loop










"""
def get_next_player(current_player, table):
    

    # get the number of original players
    num_players = len(table.players_game)

    # Find the index of the current player by name if no index given
    if type(current_player) == int:
        print('an index is given')
        current_index = current_player
    else:
        # search for the current player in the original list of players
        current_index_in_original_list = next((i for i, player in enumerate(table.players) if player == current_player), None)
        
    if current_index is None:
        logger.debug(f"The current player is not found in the original list of players... error")
        AssertionError

    next_index = (current_index + 1) % num_players
    logger.debug(f"current index: ({current_index} + 1) % {num_players} = {next_index}")
    # logger.debug(f"next index: {next_index}")

    while next_index != current_index:
        
        # if the next player is the last raiser, return None
        if next_index == current_index: 
            print(f'IT SHOULD STOP HERE RETURN {current_player.name}')
            return None
        logger.debug(f"1. try next index: {next_index} is not {current_index}")

        # if the next player is not folded, return this player, else keep looping
        if not table.players_game[next_index].folded:
            logger.debug(f"2a. The next player is {table.players_game[next_index].name}.")
        else:
            next_index = (next_index + 1) % num_players
            logger.debug(f"2b.. try next index: {next_index}")
            return table.players_game[next_index]

    # return the last raiser if it turns out to be the only one, to end the loop
    """