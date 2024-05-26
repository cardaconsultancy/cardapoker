""" Check if there is only one (or 0) person left who can do a bet """

import logging

# Retrieve the already configured logger
logger = logging.getLogger("poker_game")

def all_but_one_folded_or_all_in(table) -> bool:
    """Count players who are neither all-in nor folded."""
    count_not_all_in_or_folded = sum(
        not (player.all_in or player.folded) for player in table.players_game
    )
    logger.debug(
        "There are %s persons that are still able to bet.", count_not_all_in_or_folded
    )

    # Check if at most one player is not all-in or folded
    if count_not_all_in_or_folded <= 1:
        logger.debug("We should skip the rest.")
        return True

    return False
