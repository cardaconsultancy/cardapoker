from poker_game.utils.next_player import get_next_player
from poker_game.utils.pot_management import check_if_only_one_player_left, create_pots
from poker_game.utils.logging_config import setup_logging

# Obtain the logger configured in logging_config.py
logger = setup_logging()

# A full round of Texas Holdem
def betting_round_completed(table, preflop_round = False):
    
    # make sure that this logs    
    logger.info(f"TEST")
    
    logger.debug(f" ------------- Start betting round ------------- ")
    all_are_done = False

    # do we have to initialise it here or is there a smarter way to make this while loop work?
    last_raiser = table.dealer
    player = get_next_player(last_raiser, table)

    # create a second indicator that helps with letting the BB have another turn
    SB_is_last_raiser_so_that_BB_can_have_another_go = False

    # create another variable for if it is the first_bet
    first_bet = True
    
    if preflop_round == True:
        SB_is_last_raiser_so_that_BB_can_have_another_go = True
        first_bet = False

    # start the betting round
    while player != last_raiser:

        # if this is the first bet and we are not in the preflop round, the last raiser is the one that sets the limit
        if first_bet == True and preflop_round == False:
            last_raiser = player
            logger.debug(f"this is the first bet and so {last_raiser.name} automatically is last raiser")
            first_bet = False
        logger.debug(f" the current last raiser is {last_raiser.name} with {last_raiser.total_bet_betting_round} chips")
        logger.debug(f"{player.name} is up and currently has {player.total_bet_betting_round} in the betting round pot")

        if preflop_round == True:
            player.total_bet_betting_round += table.blind_size
            logger.debug(f"Player {player.name} has the small blind of {player.total_bet_betting_round}")
            
            # log turn
            logger.info(f'SB-{player.name}-{player.total_bet_betting_round}')
            
            # check for all in
            if table.blind_size >= player.chips.amount:
                logger.debug(f"Player {player.name} is all in")
                player.all_in = True
                player.total_bet_betting_round = player.chips.amount
                player.total_in_pots_this_game = player.chips.amount
                player.chips.lose(player.chips.amount)
            else:
                player.total_bet_betting_round = (table.blind_size)
                player.total_in_pots_this_game = (table.blind_size)
                player.chips.lose(table.blind_size)

            player = get_next_player(player, table)
            player.total_bet_betting_round += table.blind_size*2
            logger.debug(f"Player {player.name} has the Big blind of {player.total_bet_betting_round}")
            
            # log turn
            logger.info(f'BB-{player.name}-{player.total_bet_betting_round}')

            if table.blind_size*2 >= player.chips.amount:
                logger.debug(f"Player {player.name} is all in")
                player.all_in = True
                player.total_bet_betting_round = player.chips.amount
                player.total_in_pots_this_game = player.chips.amount
                player.chips.lose(player.chips.amount)
            else:
                player.total_bet_betting_round = (table.blind_size*2)
                player.total_in_pots_this_game = (table.blind_size*2)
                player.chips.lose(table.blind_size*2)

            preflop_round = False
            
            player = get_next_player(player, table)

            last_raiser = player
            logger.debug(f"The last raiser is now {player.name} with {player.total_bet_betting_round}")

            

        # for pl in table.players_game:
            
        logger.debug(f"{player.name} is up.")
        bet_sizes = [player.total_bet_betting_round for player in table.players_game]
        max_bet = max(bet_sizes)

        # logger.debug(f'bet sizes {bet_sizes}')

        
        # check if all in or folded
        if not player.all_in or player.folded:
            # add the 'first' rule to account for the time when a person has a big blind and is the last raiser.

            # This is a very confusing part of poker, where the last raiser can have another go when he/she is the big blind.
            # I Have entered a section here that keeps logs 
            # if player == last_raiser and SB_is_last_raiser_so_that_BB_can_have_another_go == True:
                # I keep switching between these options, but for now, it is more convenient to have the last raiser logic
                # separate from the highest bid due to big blinds being able to raise again.
                # max_bet = last_raiser.total_bet_betting_round

            # else:
                # logger.debug(f"{player.name} has to match {max_bet} from last raiser {last_raiser.name}")

                # check if max_bet is lower than theirs 
                # (this can happen if the SB or is higher than the chipsstack and player is the BB), if so make current player lastraiser
                # if max_bet < player.total_bet_betting_round:
                #     logger.debug(f"Because {last_raiser.name}'s {max_bet} chips is less than {player.name}'s {player.total_bet_betting_round}, make this the last bet")
                #     last_raiser = player

                # for gambler in table.players_game:
                    

            # ugly but this prevents the users from making mistakes (or cheating) by this functionality in their standard function.
            ################## user call #####################
            player_bet = player.response(max_bet, player.hand, table)
            # 
            ##################################################

            # for gambler in table.players_game:
                

            # logger.debug(f"total bet was {player.total_bet_betting_round}")
            # new_bet = player.total_bet_betting_round + player_bet
            # logger.debug(f"total bet is {player.total_bet_betting_round + player_bet}")

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
                
                # you are not losing any more chips
                # player.chips.lose(player.chips.amount)
                logger.debug(f"Player {player.name} folds as {player.total_bet_betting_round + player_bet} is smaller than {max_bet} and NO all in. He/she loses his/her chips")
                # add to total_bet as this must be added to the pot (don't remove yet from player_list)
                
                # you are not losing any more chips
                # player.total_bet_betting_round += (player_bet)
                # player.total_in_pots_this_game += (player_bet)
                
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
            elif player.total_bet_betting_round + player_bet == max_bet and player_bet == 0:
            
                # player.chips.lose(player.total_bet_betting_round)
                # player.total_bet_betting_round += player_bet
                # player.total_in_pot_this_game += player.total_bet_betting_round
                player.raised_called_or_checked_this_round = True
                logger.debug(f"Player {player.name} checks with {player_bet} and has {player.chips.amount} chips left")

            # Calling
            elif player.total_bet_betting_round + player_bet == max_bet:
                
                # must do it here as we take away chips with the blinds
                player.chips.lose(player_bet)
                
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
            if player == last_raiser and SB_is_last_raiser_so_that_BB_can_have_another_go == True:
                SB_is_last_raiser_so_that_BB_can_have_another_go = False

            # required_action += 1

            # set first to False to make sure that we select the last raiser next time.
            # first = False
                    
            # Extra logging for confusing situations
            # if max_bet > last_raiser.total_bet_betting_round: logger.debug(f"The max Bet is higher than the amount betted by the last raiser, due to him/her being the SB and not having enough. We let the other player do a call and solve this in the pot distribution (give the money back).")


            # else:
            #     logger.debug(f"Player {player.name} was the last raiser")
            #     all_are_done = True
            # update the all_are_done
        
        logger.debug(f'total bet: {player.total_bet_betting_round}')
        logger.debug(f'NR of players in game = {len(table.players_game)}')
        logger.debug(f"-- The player was {player.name}")
        # The player who has the small blind makes the first bet in poker, which is why we can get the next one directly
        player = get_next_player(player, table)

        if player == None:
            player = last_raiser
            

    # for player in table.players_game:
                   

    # for player in table.players_game:
        
        

    # all players are either all in or folded or have called/checked/raised
    logger.debug(f"Betting round over")

    # create pots
    create_pots(table)

    # remove all players that have folded
    table.players_game = [player for player in table.players_game if player.folded == False]
    logger.debug(f"Players left in the game {[player.name for player in table.players_game]}")

    # completed betting round
    return True