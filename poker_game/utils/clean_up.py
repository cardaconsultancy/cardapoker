""" Get the next dealer, remove the players without money and determine if the game is ended """

import logging
from poker_game.utils.next_player import get_next_player

# Retrieve the already configured logger
logger = logging.getLogger("poker_game")


def clean_up(table) -> None:
    """Get the next dealer, remove the players without money and determine if the game is ended"""

    logger.debug(
        "cleaning time for players %s", [player.name for player in table.players]
    )

    # Get the next dealer
    table.dealer = get_next_player(
        starting_players_and_seats=table.starting_players_and_seats,
        active_players=table.players_game,
        current_player=table.dealer,
    )

    # loop over a copy of the list and remove all the people without money
    for player in table.players[:]:
        logger.debug("%s has %s chips left", player.name, player.chips.amount)
        logger.info("%s-chips-%s", player.name, player.chips.amount)
        player.hand = []
        player.total_bet_betting_round = 0
        player.folded = False
        player.all_in = False
        if player.chips.amount == 0:
            table.players.remove(player)
            logger.debug(
                "%s has no chips left and leaves the table crying", player.name
            )
    # Create a new list that only includes the players you want to keep
    table.players_game = table.players
    table.community_cards = []
    table.pots = []

    # if there is only one player left, the game is over
    if len(table.players) == 1:
        logger.debug("Only %s is left, the game is over.", table.players[0].name)
        return None
