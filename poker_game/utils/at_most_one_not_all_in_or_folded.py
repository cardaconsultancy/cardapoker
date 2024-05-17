import logging

# Retrieve the already configured logger
logger = logging.getLogger('poker_game')

def all_but_one_folded_or_all_in(table) -> bool:
    # Count players who are neither all-in nor folded
    count_not_all_in_or_folded = sum(not (player.all_in or player.folded) for player in table.players_game)
    logger.debug(f"There are {count_not_all_in_or_folded} persons that are still able to bet.")

    # Check if at most one player is not all-in or folded
    if count_not_all_in_or_folded <= 1:
        logger.debug(f"We should skip the rest.")
        return True
    else:
        return False