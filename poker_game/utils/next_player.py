import logging

logger = logging.getLogger(__name__)

def get_next_player(current_player, table):
    """
    Gets the next player in the list who hasn't folded or gone all-in.
    """
    num_players = len(table.players_game)
    print('getting next player')
    # Find the index of the current player by name if no index given
    if type(current_player) == int:
        print('an index is given')
        current_index = current_player
    else:
        current_index = next((i for i, player in enumerate(table.players_game) if player == current_player), None)
    if current_index is None:
        logger.debug(f"The current player is not found, probably he/she just left crying!")
        return None

    next_index = (current_index + 1) % num_players
    logger.debug(f"current index: ({current_index} + 1) % {num_players} = {next_index}")
    # logger.debug(f"next index: {next_index}")

    while next_index != current_index:
        logger.debug(f"1. try next index: {next_index} is not {current_index}")
        logger.debug(f"1b. but folded: {table.players_game[next_index].folded} - or all in {table.players_game[next_index].all_in}")
        if not table.players_game[next_index].folded and not table.players_game[next_index].all_in:
            logger.debug(f"2a. The next player is {table.players_game[next_index].name}.")
            return table.players_game[next_index]
        next_index = (next_index + 1) % num_players
        logger.debug(f"2b.. try next index: {next_index}")
        if next_index == current_index: print(f'IT SHOULD STOP HERE RETURN {current_player.name}')

    # return the last raiser if it turns out to be the only one, to end the loop
    return current_player