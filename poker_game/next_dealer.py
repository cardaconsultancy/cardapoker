import logging

# Retrieve the already configured logger
logger = logging.getLogger('poker_game')

def find_next_dealer(starting_players, active_players, current_dealer):
    
    """
    Find the next dealer in the list of starting players, who is also an active player.
    """

    # Log the current dealer and active and starting players
    logging.debug(f"Current dealer: {current_dealer.name}")
    active_player_names = [player.name for player in active_players]
    logging.debug(f"Active players: {active_player_names}")
    starting_player_names = [player.name for player in starting_players]
    logging.debug(f"Starting players: {starting_player_names}")

    if not active_players or not starting_players:
        AssertionError('No active players or starting players found')
        return None  # Return None if either list is empty

    # Finding the index of the current dealer in the starting players
    try:
        current_index = starting_players.index(current_dealer)
    except ValueError:
        # If current dealer is not in starting players, start from the beginning
        current_index = -1

    # Start searching for the next active dealer
    total_players = len(starting_players)
    for i in range(total_players):
        next_index = (current_index + 1 + i) % total_players
        next_dealer = starting_players[next_index]
        if next_dealer in active_players:
            logging.debug(f"Next dealer: {next_dealer}")
            return next_dealer

    return None  # In case no active players are found in starting players, though this should ideally never happen
