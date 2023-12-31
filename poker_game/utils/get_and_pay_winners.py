from .evaluate_hand import get_hand_rank, card_rank_value
import logging

logger = logging.getLogger(__name__)

def pay_winners(table):
    for pot in table.pots:
        last_pot = table.pots[-1]
        winner_list = determine_winners(last_pot.players, table)
        bounty = last_pot.amount / len(winner_list)
        for winner in winner_list:
            logger.debug(f"{winner.name} gets {bounty} chips")
            winner.chips.win(bounty)
        logger.debug(f"Removing {table.pots.pop()}, so {len(table.pots)} pots left")

def determine_winners(pot_players, table):
    # Determine the best hand for each player
    # dict_example = {}
    winner_list = []
    for player in pot_players:
        player.set_best_hand(get_hand_rank(player, table))
        logger.debug(f"{player.name} highest hand is {player.best_hand}")
        logger.debug(f"- {player.name} has hand {player.best_hand}")
        # create a list of players
        winner_list.append(player)

    for metric in range(0,5):
        logger.debug(f"1. Metric nr {metric}")
        # get the max metric in hand rank
        metric_list = []
        # print('-----------', metric_list)
        for player in winner_list:
            logger.debug(f"  2a. Player {player.name} with {player.best_hand}")
            if metric == 0:
                metric_list.append(player.best_hand[metric])
            else:
                metric_list.append(card_rank_value(player.best_hand[metric]))
            # print('-----------', metric_list)
        max_metric = max(metric_list)
        mask = []
        for metric in metric_list:
            # logger.debug(f"  2b. Metric score {metric}")
            if metric == max_metric:
                mask.append(True)
            else:
                mask.append(False)
        # use the mask to select True candidates from winner_list
        relevant_winners = []
        for i in range(len(winner_list)):
            # logger.debug(f"  2c. {i} of {len(winner_list)}")
            if mask[i]:
                relevant_winners.append(winner_list[i])
                logger.debug(f"{winner_list[i].name} is in winner list")
        winner_list = relevant_winners
        if len(winner_list) == 1:
            logger.debug(f"0. The winner is {winner_list[0].name}")
            break
    if len(winner_list) != 1:
        logger.debug(f"0. There is a tie between winners:")
        for winner in winner_list:
            logger.debug(f"- {winner.name}")
    return winner_list