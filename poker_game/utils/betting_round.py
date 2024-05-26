"""This module contains the code for a full betting round in Texas Holdem"""

import logging
from poker_game.utils.next_player import get_next_player
from poker_game.utils.pot_management import check_if_only_one_player_left, create_pots
from poker_game.Timer import timeout

# Retrieve the already configured logger
logger = logging.getLogger("poker_game")


# A full round of Texas Holdem
@timeout(5)  # Set timeout to 5 seconds
def betting_round_completed(table, preflop_round=False) -> bool:
    """This code starts the betting round until we reach the last raiser"""

    logger.debug(" ------------- Start betting round ------------- ")
    # do we have to initialise it here or is there a smarter way to make this while loop work?
    last_raiser = table.dealer

    # create logger info in the form of:
    # A = create_player("A", "raises_with_aces_reduces_with_12345", Chips(15))
    # create a copy to be safe:
    print_player = table.dealer

    for _ in table.players_game:
        logger.info("table.add_player(%s)", print_player.name)
        print_player = get_next_player(
            starting_players=table.starting_players,
            active_players=table.players_game,
            current_player=print_player,
        )

    # for ease of debugging:
    logger.info("start_round(table=table, test_cards = test_cards)")

    player = get_next_player(
        starting_players=table.starting_players,
        active_players=table.players_game,
        current_player=last_raiser,
    )

    # create a second indicator that helps with letting the BB have another turn
    # SB_is_last_raiser_so_that_BB_can_have_another_go = False

    # create another variable for if it is the first_bet
    first_bet = True

    if preflop_round:
        # SB_is_last_raiser_so_that_BB_can_have_another_go = True
        first_bet = False

    # start the betting round

    # this poses a problem when the last raiser has folded and is automatically the last 
    # raiser after the BB
    big_blind_player = None

    while player != last_raiser:

        # if this is the first bet and we are not in the preflop round, the first raiser 
        # is the one that sets the limit
        if first_bet and preflop_round is False:
            last_raiser = player
            logger.debug(
                "this is the first bet and so %s automatically is last raiser",
                last_raiser.name
            )
            first_bet = False
        logger.debug(
            "the current last raiser is %s with %s chips",
            last_raiser.name,
            last_raiser.total_bet_betting_round
        )
        logger.debug(
            "%s is up and currently has %s in the betting round pot",
            player.name,
            player.total_bet_betting_round
        )

        if preflop_round:
            player.total_bet_betting_round += table.blind_size
            logger.debug(
                f"Player {player.name} has the small blind of {player.total_bet_betting_round}"
            )

            # check for all in
            if table.blind_size >= player.chips.amount:
                logger.debug(f"Player {player.name} is all in")
                player.all_in = True
                player.total_bet_betting_round = player.chips.amount
                player.total_in_pots_this_game = player.chips.amount
                player.chips.lose(player.chips.amount)
            else:
                player.total_bet_betting_round = table.blind_size
                player.total_in_pots_this_game = table.blind_size
                player.chips.lose(table.blind_size)

            # log SB if all in or not
            logger.info(f"SB-{player.name}-{player.total_bet_betting_round}")

            player = get_next_player(
                starting_players=table.starting_players,
                active_players=table.players_game,
                current_player=player,
            )
            player.total_bet_betting_round += table.blind_size * 2
            logger.debug(
                "Player %s has the Big blind of %s",
                player.name,
                player.total_bet_betting_round,
            )

            # create a variable that keeps track of the big blind player. We do this so that we can name the next player automatically the last raiser without worrying about creating an indefinite loop.
            big_blind_player = player

            if table.blind_size * 2 >= player.chips.amount:
                logger.debug("Player %s is all in", {player.name})
                player.all_in = True
                player.total_bet_betting_round = player.chips.amount
                player.total_in_pots_this_game = player.chips.amount
                player.chips.lose(player.chips.amount)
            else:
                player.total_bet_betting_round = table.blind_size * 2
                player.total_in_pots_this_game = table.blind_size * 2
                player.chips.lose(table.blind_size * 2)

            # log BB if all in or not
            logger.info(f"BB-{player.name}-{player.total_bet_betting_round}")

            preflop_round = False

            player = get_next_player(
                starting_players=table.starting_players,
                active_players=table.players_game,
                current_player=player,
            )

            last_raiser = player
            logger.debug(
                f"The last raiser is now {player.name} with {player.total_bet_betting_round}"
            )

        logger.debug(f"{player.name} is up.")
        bet_sizes = [gambler.total_bet_betting_round for gambler in table.players_game]
        max_bet = max(bet_sizes)

        # if the BB player cannot afford the BB, the max_bet is the BB
        # UNLESS... the SB player has the highest bet because all the other players cannot afford the SB... Ugh...
        # UNLESS... the round is not the preflop round
        logger.debug(f"the max bet is {max_bet}")
        if (
            max_bet < table.blind_size * 2
            and player.total_bet_betting_round != max_bet
            and preflop_round == True
        ):
            logger.debug(
                f"the max bet is lower than the BB, so we set it to the BB of {table.blind_size*2}"
            )
            max_bet = table.blind_size * 2

        # check if all in or folded
        if not player.all_in and not player.folded:

            # ugly but this prevents the users from making mistakes (or cheating) by this functionality in their standard function.
            ################## user call #####################
            player_bet = player.response(max_bet, player.hand, table)
            ##################################################

            # All in
            # Also check if the betsize is bigger than the chips, if so correct by making it the max bet
            if (
                player.total_bet_betting_round + player_bet
                >= player.total_bet_betting_round + player.chips.amount
            ):

                # Log this event
                logger.debug(
                    f"{player.name} goes all in because {player.total_bet_betting_round + player_bet} >= {player.total_bet_betting_round + player.chips.amount}, so automatically the player is all in!!"
                )
                # don't put this before the log
                player_bet = player.chips.amount

                # what is left and what is bet is the all in
                player.chips.lose(player.chips.amount)

                player.total_bet_betting_round += player_bet
                logger.info(f"{player.name}-{player_bet}-AI")

                player.total_in_pots_this_game += player_bet
                logger.debug(
                    f"{player.name} new bet is {player.total_bet_betting_round}."
                )
                player.all_in = True

                # check if the all in player is raising (seems better than to check for all options if player is all in)
                if player.total_bet_betting_round > max_bet:
                    last_raiser = player
                    logger.debug(f"----{player.name} is the last raiser")

            # Folding
            # Note that this automatically prevents a player from folding when he/she can check, as it should

            elif player.total_bet_betting_round + player_bet < max_bet:

                # you are not losing any more chips
                logger.debug(
                    f"Player {player.name} folds as {player.total_bet_betting_round + player_bet} is smaller than {max_bet} and NO all in. He/she loses his/her chips"
                )
                logger.info(f"{player.name}-F")

                player.folded = True

                # exception on the exception: if a SB player folds and there are only two left, the next should not be BB,
                # because this is not how it works (it should end there) and we do not take into account this possibility
                # we can solve this by just checking if there is only one other player (and possibly save some calc time for the rest)
                # if len([player for player in table.players_game if player.folded != True]) == 1:
                #     logger.debug(f"return True and let get and check_if_rest_folded_and_pay pay the winner")
                #     return True
                if check_if_only_one_player_left(table):
                    return False

                # we don't want to remove the player from the game yet, as we need to put his/her chips in the pot

            # Checking
            elif (
                player.total_bet_betting_round + player_bet == max_bet
                and player_bet == 0
            ):
                player.raised_called_or_checked_this_round = True
                logger.debug(
                    f"Player {player.name} checks with {player_bet} and has {player.chips.amount} chips left"
                )
                logger.info(f"{player.name}-{player_bet}-Check")

            # Calling
            elif player.total_bet_betting_round + player_bet == max_bet:

                # must do it here as we take away chips with the blinds
                player.chips.lose(player_bet)
                player.total_in_pots_this_game += player_bet
                player.total_bet_betting_round += player_bet
                player.raised_called_or_checked_this_round = True
                logger.debug(
                    f"Player {player.name} calls with {player_bet}, making the total {player.total_bet_betting_round} this round. He/she has {player.chips.amount} chips left"
                )
                logger.info(f"{player.name}-{player_bet}-Call")

            # Raising
            elif player.total_bet_betting_round + player_bet > max_bet:
                player.chips.lose(player_bet)
                player.total_bet_betting_round += player_bet
                player.total_in_pots_this_game += player_bet
                player.raised_called_or_checked_this_round = True
                logger.debug(
                    f"Player {player.name} throws in {player_bet}, raising to {player.total_bet_betting_round} and has {player.chips.amount} chips left"
                )
                last_raiser = player
                logger.debug(f"----{player.name} is the last raiser")
                logger.info(f"{player.name}-{player_bet}-Raise")

            else:
                logger.debug(
                    f"Something went wrong with the betting round, the player {player.name} has not called, checked, raised or folded."
                )
                return False

        logger.debug(f"total bet {player.name}: {player.total_bet_betting_round}")

        # to prevent a future issue with the player after the big blind being automatically being the last raiser and folding:
        # but this leads to the issue that the player after the BB might still need to call to a raise from the next player.
        if player == big_blind_player:

            # this is the first time so remove this special status
            big_blind_player = None
            # get a new list of bet sizes from players that have not folded:
            for gambler in table.players_game:
                logger.debug(
                    f"------- {gambler.name} {gambler.total_bet_betting_round} {gambler.folded}"
                )
            bet_sizes = [
                gambler.total_bet_betting_round
                for gambler in table.players_game
                if gambler.folded == False
            ]
            logger.debug(f"the non folded bet sizes are {bet_sizes}")
            min_bet = min(bet_sizes)
            logger.debug(f"the min bet which is not folded is {min_bet}")

            if (
                max_bet == player.total_bet_betting_round
                and min_bet == player.total_bet_betting_round
            ):
                logger.debug(
                    f"Because this (1) is the Big Blind, (2) the {last_raiser.name}'s {max_bet} chips is less than or equal to {player.name}'s {player.total_bet_betting_round} and (3) the lowest bet is also {min_bet}, make this the last bet"
                )
                player = last_raiser
            else:
                logger.debug(
                    f"Because {player.name} (1) is the Big Blind, but (2) the {last_raiser.name}'s {max_bet} chips is less than or equal to {player.name}'s {player.total_bet_betting_round} and/or (3) there are other lower bets, continue as normal"
                )
                # The player who has the small blind makes the first bet in poker, which is why we can get the next one directly
                logger.debug(f"The player was {player.name}")
                player = get_next_player(
                    starting_players=table.starting_players,
                    active_players=table.players_game,
                    current_player=player,
                )

                if player is None:
                    player = last_raiser
        else:
            # The player who has the small blind makes the first bet in poker, which is why we can get the next one directly
            logger.debug(f"The player was {player.name}")
            player = get_next_player(
                starting_players=table.starting_players,
                active_players=table.players_game,
                current_player=player,
            )

            if player is None:
                player = last_raiser

    # all players are either all in or folded or have called/checked/raised
    logger.debug(
        f"Betting round over, because {player.name} is the last raiser {last_raiser.name} and all players have called/checked/raised or folded."
    )

    # create pots
    create_pots(table)

    # remove all players that have folded
    table.players_game = [
        player for player in table.players_game if player.folded == False
    ]
    logger.debug(
        f"Players left in the game {[player.name for player in table.players_game]}"
    )

    # completed betting round
    return True