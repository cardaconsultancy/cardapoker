import logging

from poker_game.utils.start_round import start_round

logger = logging.getLogger(__name__)

def play_game(table, rounds_before_raise_blinds=20, seed=None):
    total_chips = sum(player.chips.amount for player in table.players)
    table.dealer = table.players_game[0]
    logger.debug(f'Player {table.dealer.name} gets the dealer button')
    game_on = True
    number_of_rounds = 1
    blinds_raised = 0
    print('game on')
    while game_on:
        for raising_time in range(0, rounds_before_raise_blinds):            
            number_of_rounds += 1
            logger.debug(f'')
            logger.debug(f'')
            logger.debug(f'')
            for player in table.players_game:
                logger.debug(f'------- Player {player.name} has {player.chips.amount} ------') 
                if player.chips.amount == total_chips:
                    logger.debug(f"player {player.name} has won after {number_of_rounds} rounds!!!!")
                    return player.name, number_of_rounds
            print(f'next round: {number_of_rounds}')

            # to create some quick variance over rounds while testing multiple rounds
            if seed != None:
                start_round(table=table, seed=seed*seed*number_of_rounds)
            else:
                start_round(table=table)
        
        table.increase_blinds()
        blinds_raised += 1
        logger.debug(f'Blinds raised {blinds_raised} times')
    return table, number_of_rounds