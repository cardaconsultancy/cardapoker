import logging

# Retrieve the already configured logger
logger = logging.getLogger('poker_game')

def get_next_player(starting_players, active_players, current_player):
    
    """
    Find the next player in the list of starting players, who is also an active player.
    """

    # Log the current player and active and starting players
    logger.debug(f"Current player: {current_player.name}")
    active_player_names = [player.name for player in active_players]
    logger.debug(f"Active players: {active_player_names}")
    starting_player_names = [player.name for player in starting_players]
    logger.debug(f"Starting players: {starting_player_names}")

    if not active_players or not starting_players:
        AssertionError('No active players or starting players found')
        return None  # Return None if either list is empty

    # Finding the index of the current player in the starting players
    try:
        current_index = starting_players.index(current_player)
    except ValueError:
        # If current player is not in starting players, start from the beginning
        current_index = -1

    # Start searching for the next active player
    total_players = len(starting_players)
    for i in range(total_players):
        next_index = (current_index + 1 + i) % total_players
        next_player = starting_players[next_index]
        if next_player in active_players:
            logger.debug(f"Next player: {next_player.name}")
            return next_player





# def get_next_player(current_player, table):
#     """
#     Don't select on all in as this might be the last_raiser, ending the loop
#     """

#     # get the number of original players
#     num_players = len(table.players_game)


#     # search for the current player in the original list of players
#     current_index_in_original_list = next((i for i, player in enumerate(table.starting_players) if player == current_player), None)

#     namelist = [player.name for player in table.starting_players]
#     if current_index_in_original_list is None:
#         logger.debug(f'The current player{current_player.name} is not found in the original list of players...{namelist} error!')
    
#     # get the next index in the original list of players
#     next_index = (current_index_in_original_list + 1) % num_players
    
#     # get the next player from the original list of players
#     next_player = table.players[next_index]

#     while current_player != next_player:
        
#         if current_player == next_player: 
#             print(f'IT SHOULD STOP HERE RETURN {current_player.name}')
#             return None
        
#         else:
#             # double check if this player is still in the game
#             if next_player in table.players_game and not next_player.folded:

#                 # return the next player in the new list of players
#                 return next_player

#             next_index = (next_index + 1) % num_players
#             next_player = table.players_game[next_index]
#             if next_player in table.players_game:
#                 logger.debug(f"_________________The next player is {next_player.name}.")
#                 return next_player


