from .evaluate_hand import get_hand_rank, card_rank_value
import logging

# Retrieve the already configured logger
logger = logging.getLogger('poker_game')

# Determine the winners of the round
def determine_winners(pot_players, table):
    # Determine the best hand for each player
    # dict_example = {}
    winner_list = []
    for player in pot_players:
        player.set_best_hand(get_hand_rank(player, table))
        logger.debug(f"{player.name} highest hand is {player.best_hand}")
        # create a list of players
        winner_list.append(player)

    for metric in range(0,5):
        logger.debug(f"1. Metric nr {metric}")
        # get the max metric in hand rank
        metric_list = []
        for player in winner_list:
            logger.debug(f"  2a. Player {player.name} with {player.best_hand}")
            logger.info(f"{player.name}-{player.best_hand}")
            if metric == 0:
                metric_list.append(player.best_hand[metric])
            else:
                metric_list.append(card_rank_value(player.best_hand[metric]))
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
            logger.debug(f"The winner is {winner_list[0].name}")
            break
    if len(winner_list) != 1: logger.debug(f"There is a tie between winners:")
    return winner_list

def pay_winners(table):
    while table.pots:
        logger.debug(f"There are {len(table.pots)} pots left")

        last_pot = table.pots.pop()  # Remove and get the last pot
        logger.debug(f"There are {len(table.pots)} pots left after popping--------------------")
        logger.debug(f"The current pot has {last_pot.amount}")
        # for player in last_pot.players:
        #     print(player.name)

        winner_list = determine_winners(last_pot.players, table)
        
        # Calculate the main bounty for each winner
        bounty = last_pot.amount // len(winner_list)
        remainder = last_pot.amount % len(winner_list)
        
        for winner in winner_list:
            logger.debug(f"{winner.name} gets {bounty} chips")
            winner.chips.win(bounty)
        
        # Distribute remainder chips
        index = 0  # Start from the first winner
        while remainder > 0:
            logger.debug(f"There is a remainder of {remainder} chips")
            # Prioritize last raiser if they are a winner
            recipient = winner_list[index % len(winner_list)]
            index += 1
            logger.debug(f"{recipient.name} gets an extra chip")
            recipient.chips.win(1)
            remainder -= 1

        logger.debug(f"Removing {last_pot}, so {len(table.pots)} pots left")

    # debugger
    if sum(player.chips.amount for player in table.players) != 600:
        print(sum(player.chips.amount for player in table.players))