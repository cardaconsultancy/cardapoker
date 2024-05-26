import logging

# Retrieve the already configured logger
logger = logging.getLogger("poker_game")


def get_next_player(starting_players, active_players, current_player):
    """
    Find the next player in the list of starting players, who is also an active player.
    """

    # Log the current player and active and starting players
    logger.debug("Current player: %s", current_player.name)
    active_player_names = [player.name for player in active_players]
    logger.debug("Active players: %s", active_player_names)
    starting_player_names = [player.name for player in starting_players]
    logger.debug("Starting players: %s", starting_player_names)

    if not active_players or not starting_players:
        logger.error("No active players or starting players found")
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
            logger.debug("-- Next player: %s", next_player.name)
            return next_player
