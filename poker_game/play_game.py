import logging

from poker_game.utils.start_round import start_round

logger = logging.getLogger(__name__)

def play_game(table, rounds_before_raise_blinds=20, seed=None):
    total_chips = sum(player.chips.amount for player in table.players)
    table.dealer = table.players_game[0]
    logger.debug(f'Player {table.dealer.name} gets the dealer button')
    game_on = True
    number_of_rounds = 1
    while game_on == True:
        for raising_time in range(0, rounds_before_raise_blinds):            
            logger.debug('')
            logger.debug('')
            logger.debug('')
            for player in table.players_game:
                logger.debug(f'------- Player {player.name} has {player.chips.amount} ------') 
                number_of_rounds += 1
                if player.chips.amount == total_chips:
                    logger.debug(f"player {player.name} has won after {number_of_rounds} rounds!!!!")
                    return True
            game_on = start_round(table=table, seed=seed)
        table.increase_blinds()
        logger.debug(f'Blinds raised {raising_time} times')
    return table