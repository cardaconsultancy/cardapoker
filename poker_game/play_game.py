import logging
import datetime
from poker_game.utils.set_up_database import log_game
from poker_game.utils.play_round import play_round

logger = logging.getLogger(__name__)


def play_game(table, rounds_before_raise_blinds=20, seed=None):
    total_chips = sum(player.chips.amount for player in table.players)
    table.dealer = table.players_game[0]
    logger.debug(f"Player {table.dealer.name} gets the dealer button")
    game_on = True
    number_of_rounds = 1
    blinds_raised = 0
    logger.debug("game on")
    while game_on:
        for raising_time in range(0, rounds_before_raise_blinds):
            number_of_rounds += 1
            logger.debug(f"")
            logger.debug(f"")
            logger.debug(f"")
            for player in table.players_game:
                logger.debug(
                    f" Player {player.name} has {player.chips.amount}"
                )
                if player.chips.amount == total_chips:
                    logger.debug(
                        f"player {player.name} has won after {number_of_rounds} rounds!!!!"
                    )

                    # log the results in the database
                    log_game(
                        game_id=str(datetime.datetime.now()),
                        game_seed=seed,
                        winner=player.name,
                        seat_winner=table.starting_players_and_seats.index(player),
                        strategy_winner=player.__class__.__name__,
                        number_of_rounds=number_of_rounds,
                        player_1=table.starting_players_and_seats[0].name,
                        player_2=table.starting_players_and_seats[1].name,
                        player_3=table.starting_players_and_seats[2].name,
                        player_4=table.starting_players_and_seats[3].name,
                        player_5=table.starting_players_and_seats[4].name,
                        player_6=table.starting_players_and_seats[5].name
                    )

                    return player.name, number_of_rounds
            logger.debug(f"next round: {number_of_rounds}")

            # to create some quick variance over rounds while testing multiple rounds
            if seed != None:
                play_round(table=table, seed=seed * seed * number_of_rounds)
            else:
                play_round(table=table)

        table.increase_blinds()
        blinds_raised += 1
        logger.debug(f"Blinds raised {blinds_raised} times")
    return table, number_of_rounds
