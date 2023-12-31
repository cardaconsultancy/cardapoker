import logging

from poker_game.utils.next_player import get_next_player
from poker_game.utils.pot_management import create_pots

logger = logging.getLogger(__name__)

def betting_round(table, preflop_round = False):
    print()
    logger.debug(f"The dealer is {table.dealer.name}.")
    # print()
    # required_action = 0

    # if first == True:
    #     # table.players_game[0].bet(table.blind_size)
    #     table.players_game[table.dealer+1].total_bet_betting_round += table.blind_size
    #     logger.debug(f"Player {table.players_game[table.dealer+1].name} has the small blind of {table.players_game[table.dealer+1].total_bet_betting_round}")
    #     logger.debug(f"Player {table.players_game[table.dealer+1].name} has the small blind of {table.players_game[table.dealer+1].total_bet_betting_round}")
    #     table.players_game[table.dealer+1].chips.lose(table.blind_size)
    #     table.players_game[table.dealer+1].total_bet_betting_round = (table.blind_size)
    #     table.players_game[table.dealer+1].total_in_pots_this_game = (table.blind_size)

    #     # table.players_game[1].bet(table.blind_size*2)
    #     table.players_game[table.dealer+2].total_bet_betting_round += table.blind_size*2
    #     logger.debug(f"Player {table.players_game[table.dealer+2].name} has the big blind of {table.players_game[table.dealer+2].total_bet_betting_round}")
    #     table.players_game[table.dealer+2].chips.lose(table.blind_size*2)
    #     table.players_game[table.dealer+2].total_bet_betting_round = (table.blind_size*2)
    #     table.players_game[table.dealer+2].total_in_pots_this_game = (table.blind_size*2)
    #     required_action = -2
    # else:
    #     full_round_player = table.players_game[table.dealer]
    #     logger.debug(f"The game ends when {full_round_player.name} is about to get his turn again")


    logger.debug(f" ------------- Start betting round ------------- ")
    # max 100 
    all_are_done = False

    # do we have to initialise it here or is there a smarter way to make this while loop work?
    last_raiser = table.dealer
    player = get_next_player(last_raiser, table)

    # create a second indicator that helps with letting the BB have another turn
    # create another variable for if it is the first_bet
    BB_can_have_another_go = False
    first_bet = True
    if preflop_round == True:
        BB_can_have_another_go = True
        first_bet = False

    for pl in table.players_game:
        print('check: ', pl.name)

    counter = 0
    while player != last_raiser and counter <10:
        for pl in table.players_game:
            print('check: ', pl.name)
        if first_bet == True and preflop_round == False:
            last_raiser = player
            logger.debug(f"this is the first round and so {last_raiser.name} is the last raiser")
            first_bet = False
        logger.debug(f" the current last raiser is {last_raiser.name} with {last_raiser.total_bet_betting_round} chips")

        counter += 1
        
        logger.debug(f"{player.name} is up and currently has {player.total_bet_betting_round} in the betting round pot")
        # logger.debug(f'required_action {required_action}')

        # check if player has the big or small blind
        # for player in table.players_game:
        #     logger.debug(f"{player.name} is up and currently has {player.total_bet_betting_round} in the betting round pot")
        #     logger.debug(f'required_action {required_action}')
        #     for playerprint in table.players_game:
        #         print('-------', playerprint.total_bet_betting_round)

        # if required_action == -2:
        #     logger.debug(f'skipping {player.name} as he/she has the small blind')
        #     required_action += 1
        #     continue
        # if required_action == -1:
        #     logger.debug(f'skipping {player.name} as he/she has the big blind')
        #     required_action += 1
        #     full_round_player = table.players_game[0]
        #     last_raiser = player 
        #     continue

        # This takes care of the exception: this is the player on which the bet has to end in the first round, regardless of what he/she does
        # if no one else raises, this is where it ends.
        # last_raiser = player

        if preflop_round == True:
            player.total_bet_betting_round += table.blind_size
            logger.debug(f"Player {player.name} has the small blind of {player.total_bet_betting_round}")
            if player.chips.lose(table.blind_size) == False:
                logger.debug(f"Player {player.name} is all in")
                player.all_in = True
                player.total_bet_betting_round = player.chips.amount
                player.total_in_pots_this_game = player.chips.amount
                player.chips.lose(player.chips.amount)
            else:
                player.total_bet_betting_round = (table.blind_size)
                player.total_in_pots_this_game = (table.blind_size)

            player = get_next_player(player, table)
            player.total_bet_betting_round += table.blind_size*2
            logger.debug(f"Player {player.name} has the big blind of {player.total_bet_betting_round}")

            if player.chips.lose(table.blind_size*2) == False:
                logger.debug(f"Player {player.name} is all in")
                player.all_in = True
                player.total_bet_betting_round = player.chips.amount
                player.total_in_pots_this_game = player.chips.amount
                player.chips.lose(player.chips.amount)
            else:
                player.total_bet_betting_round = (table.blind_size*2)
                player.total_in_pots_this_game = (table.blind_size*2)

            # to get the max bet? Can also be changed.
            last_raiser = player
            logger.debug(f"The last raiser is now {player.name} with {player.total_bet_betting_round}")

            preflop_round = False
            print('1. checking??', player.name)
            player = get_next_player(player, table)
            print('2. checking??', player.name)

        for pl in table.players_game:
            print('check: ', pl.name)
        logger.debug(f"{player.name} is up.")
        # bet_sizes = [player.total_bet_betting_round for player in table.players_game]
        # logger.debug(f'bet sizes {bet_sizes}')
        # check if all in or folded
        if not player.all_in or player.folded:
            # add the 'first' rule to account for the time when a person has a big blind and is the last raiser.
            if player != last_raiser or (player == last_raiser and BB_can_have_another_go == True):
                logger.debug(f"{player.name} is not the last raiser (or had the BB)")
                # get info for response
                # max_bet = max(bet_sizes)
                max_bet = last_raiser.total_bet_betting_round

                # check if betsize of lastraiser is lower than theirs 
                # (this can happen if the SB or is higher than the chipsstack and player is the BB), if so make current player lastraiser
                if max_bet < player.total_bet_betting_round:
                    logger.debug(f"Because {last_raiser.name}'s {max_bet} chips is less than {player.name}'s {player.total_bet_betting_round}, make this the last bet")
                    last_raiser = player

                logger.debug(f"-------- {player.name} has to match {max_bet} from last raiser {last_raiser.name}")
                
                for gambler in table.players_game:
                    print(gambler.name, gambler.total_bet_betting_round)

                # ugly but this prevents the users from making mistakes (or cheating) by this functionality in their standard function.
                ################## user call #####################
                player_bet = player.response(max_bet, player.hand, table.community_cards)
                # print(f'the player bet is {player_bet}')
                ##################################################

                for gambler in table.players_game:
                    print(gambler.name, gambler.total_bet_betting_round)

                logger.debug(f"total bet was {player.total_bet_betting_round}")
                # new_bet = player.total_bet_betting_round + player_bet
                logger.debug(f"total bet is {player.total_bet_betting_round + player_bet}")

                # check if the betsize is bigger than the chips, if so correct by making it the max bet 
                if player.total_bet_betting_round + player_bet >= player.total_bet_betting_round + player.chips.amount:
                    logger.debug(f"{player.name} goes all in because {player.total_bet_betting_round + player_bet} >= {player.total_bet_betting_round + player.chips.amount}, so automatically the player is all in!!")
                    player_bet = player.chips.amount
                    # what is left and what is bet is the all in
                    player.chips.lose(player.chips.amount)
                    player.total_bet_betting_round += (player_bet)
                    player.total_in_pots_this_game += (player_bet)
                    logger.debug(f"{player.name} new bet is {player.total_bet_betting_round}.")
                    player.all_in = True

                    # check if the all in player is raising (seems better than to check for all options if player is all in)
                    if player.total_bet_betting_round > max_bet:
                        last_raiser = player
                        logger.debug(f"----{player.name} is the last raiser")

                # Folding
                elif player.total_bet_betting_round + player_bet < max_bet:
                    player.chips.lose(player.chips.amount)
                    logger.debug(f"Player {player.name} folds as {player.total_bet_betting_round + player_bet} is smaller than {max_bet} and NO all in. He/she loses his/her chips")
                    # add to total_bet as this must be added to the pot (don't remove yet from player_list)
                    player.total_bet_betting_round += (player_bet)
                    player.total_in_pots_this_game += (player_bet)
                    player.folded = True

                # Checking
                elif player.total_bet_betting_round + player_bet == max_bet and player_bet == 0:
                    # print(player.name, player.chips.amount, '????????????????????????')
                    # player.chips.lose(player.total_bet_betting_round)
                    # player.total_bet_betting_round += player_bet
                    # player.total_in_pot_this_game += player.total_bet_betting_round
                    player.raised_called_or_checked_this_round = True
                    logger.debug(f"Player {player.name} checks with {player_bet} and has {player.chips.amount} chips left")

                # Calling
                elif player.total_bet_betting_round + player_bet == max_bet:
                    player.chips.lose(player_bet)
                    print(player_bet)
                    print(player.total_bet_betting_round)
                    player.total_in_pots_this_game += player_bet
                    player.total_bet_betting_round += player_bet
                    player.raised_called_or_checked_this_round = True
                    logger.debug(f"Player {player.name} calls with {player_bet}, making the total {player.total_bet_betting_round} this round. He/she has {player.chips.amount} chips left")

                # Raising
                elif player.total_bet_betting_round + player_bet > max_bet:
                    player.chips.lose(player_bet)
                    player.total_bet_betting_round += player_bet
                    player.total_in_pots_this_game += player_bet
                    player.raised_called_or_checked_this_round = True
                    logger.debug(f"Player {player.name} throws in {player_bet}, raising to {player.total_bet_betting_round} and has {player.chips.amount} chips left")
                    last_raiser = player
                    logger.debug(f"----{player.name} is the last raiser")
                
                # remove the special status of Big Blind is removed if we continue
                if player == last_raiser and BB_can_have_another_go == True:
                    BB_can_have_another_go = False

                player.total_bet += player.total_in_pots_this_game
                # required_action += 1

                # set first to False to make sure that we select the last raiser next time.
                # first = False
            # else:
            #     logger.debug(f"Player {player.name} was the last raiser")
            #     all_are_done = True
            # update the all_are_done
        else:
            logger.debug(f"Player {player.name} has folded or is all in")

        logger.debug(f'total bet: {player.total_bet_betting_round}')
        logger.debug(f'NR of players in game = {len(table.players_game)}')
        logger.debug(f"-- The player was {player.name}")
        # The player who has the small blind makes the first bet in poker, which is why we can get the next one directly
        player = get_next_player(player, table)

        if player == last_raiser:
            print("IT SHOULD END HERE")

            # sugg
            # playernr = 0
            # while not all_are_done:
            #     player = playerlist[playernr]
            #     if not folded or all in:
            #         # works in two man heads up
            #         if not last_raiser:
            #             do action
            #             if raise:
            #                 update last_raiser = player
            #         else:
            #             all_are_done = True
            #     playernr += 1
            #     
            # 
            
            # this is incorrect, someone could check and then someone raises
            # rather than making a complex average, just check whether someone has raised (a seperate attribute) and the rest hasn't folded
            # if so continue

        # all_are_done = all(player.folded == True or player.raised_called_or_checked_this_round == True or player.all_in == True for player in table.players_game)

        # bet_sizes = [player.total_bet_betting_round for player in table.players_game]
        # avg_bet = sum(bet_sizes) / len(table.players_game)
        # max_bet = max(bet_sizes)

    for player in table.players_game:
        print('1', player.total_bet_betting_round, player.chips.amount)           

    for player in table.players_game:
        print(player.name)
        print(player.folded, player.raised_called_or_checked_this_round, player.all_in)

    # all players are either all in or folded or have called/checked/raised
    logger.debug(f"Betting round over")

    # create pots
    create_pots(table)