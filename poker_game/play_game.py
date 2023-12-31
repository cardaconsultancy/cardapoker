import logging

from poker_game.utils.start_round import start_round

logger = logging.getLogger(__name__)

def play_game(table, rounds_before_raise_blinds=20, seed=None):
    table.dealer = table.players_game[0]
    game_on = True
    number_of_rounds = 1
    while game_on == True:
        for raising_time in range(0, rounds_before_raise_blinds):
            
            for player in table.players_game:
                logger.debug(f'Player {player.name} has {player.chips.amount} chips') 
            game_on = start_round(table=table, seed=seed)
            logger.debug(f'Blinds raised {raising_time} times')
        table.increase_blinds()
        number_of_rounds += 1
        if number_of_rounds > 10:
            break
    return False