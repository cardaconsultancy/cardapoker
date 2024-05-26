from .evaluate_hand import get_hand_rank, card_rank_value
import logging

# Retrieve the already configured logger
logger = logging.getLogger("poker_game")


# Determine the winners of the round
def determine_winners(pot_players, table):
    # Determine the best hand for each player
    # dict_example = {}
    winner_list = []
    for player in pot_players:
        player.set_best_hand(get_hand_rank(player, table))
        logger.debug("%s highest hand is %s", player.name, player.best_hand)
        # create a list of players
        winner_list.append(player)

    for metric in range(0, 5):
        logger.debug("1. Metric nr %s", metric)
        # get the max metric in hand rank
        metric_list = []
        for player in winner_list:
            logger.debug("  2a. Player %s with %s", player.name, player.best_hand)
            logger.debug("%s-%s", player.name, player.best_hand)
            if metric == 0:
                metric_list.append(player.best_hand[metric])
            else:
                metric_list.append(card_rank_value(player.best_hand[metric]))
        max_metric = max(metric_list)
        mask = []
        for metric in metric_list:
            # logger.debug("  2b. Metric score %s", metric)
            if metric == max_metric:
                mask.append(True)
            else:
                mask.append(False)
        # use the mask to select True candidates from winner_list
        relevant_winners = []
        for i in range(len(winner_list)):
            # logger.debug("  2c. %s of %s", i, len(winner_list))
            if mask[i]:
                relevant_winners.append(winner_list[i])
                logger.debug("%s is in winner list", winner_list[i].name)
        winner_list = relevant_winners
        if len(winner_list) == 1:
            logger.debug("The winner is %s", winner_list[0].name)
            break
    if len(winner_list) != 1:
        logger.debug("There is a tie between winners:")
    return winner_list


def pay_winners(table):
    logger.debug("1. There are %s pots left", len(table.pots))
    while table.pots:
        logger.debug("2. There are %s pots left", len(table.pots))

        last_pot = table.pots.pop()  # Remove and get the last pot
        logger.debug(
            "There are %s pots left after popping--------------------", len(table.pots)
        )
        logger.debug("The current pot has %s", last_pot.amount)
        # for player in last_pot.players:
        #     print(player.name)

        winner_list = determine_winners(last_pot.players, table)

        # Calculate the main bounty for each winner
        bounty = last_pot.amount // len(winner_list)
        remainder = last_pot.amount % len(winner_list)

        for winner in winner_list:
            logger.debug("%s gets %s chips", winner.name, bounty)
            logger.info("%s-wins-%s", winner.name, bounty)
            winner.chips.win(bounty)

        # Distribute remainder chips
        index = 0  # Start from the first winner
        while remainder > 0:
            logger.debug("There is a remainder of %s chips", remainder)
            # Prioritize last raiser if they are a winner
            recipient = winner_list[index % len(winner_list)]
            index += 1
            logger.debug("%s gets an extra chip", recipient.name)
            logger.info("%s gets and extra chip", recipient.name)
            recipient.chips.win(1)
            remainder -= 1

        logger.debug("Removing %s, so %s pots left", last_pot, len(table.pots))
    # debugger to identify errors in long simulations
    # if sum(player.chips.amount for player in table.players) != 600:
    #     logger.debug("ERROR, this %s should be equal to 600", (sum(player.chips.amount for player in table.players)))
    #     AttributeError("The total amount of chips is not 600")
    #     1/0
