from poker_game.utils.next_player import get_next_player
from poker_game.utils.pot_management import create_pots
import logging

logger = logging.getLogger(__name__)

def betting_round(table, preflop_round = False):
    
    logger.debug(f"The dealer is {table.dealer.name}.")

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

    # for pl in table.players_game:
        

    counter = 0
    while player != last_raiser and counter <10:
        # for pl in table.players_game:
            
        if first_bet == True and preflop_round == False:
            last_raiser = player
            logger.debug(f"this is the first round and so {last_raiser.name} is the last raiser")
            first_bet = False
        logger.debug(f" the current last raiser is {last_raiser.name} with {last_raiser.total_bet_betting_round} chips")

        counter += 1
        
        logger.debug(f"{player.name} is up and currently has {player.total_bet_betting_round} in the betting round pot")

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
            
            player = get_next_player(player, table)
            

        # for pl in table.players_game:
            
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
                
                # for gambler in table.players_game:
                    

                # ugly but this prevents the users from making mistakes (or cheating) by this functionality in their standard function.
                ################## user call #####################
                player_bet = player.response(max_bet, player.hand, table.community_cards)
                # 
                ##################################################

                # for gambler in table.players_game:
                    

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
                    # 
                    # player.chips.lose(player.total_bet_betting_round)
                    # player.total_bet_betting_round += player_bet
                    # player.total_in_pot_this_game += player.total_bet_betting_round
                    player.raised_called_or_checked_this_round = True
                    logger.debug(f"Player {player.name} checks with {player_bet} and has {player.chips.amount} chips left")

                # Calling
                elif player.total_bet_betting_round + player_bet == max_bet:
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

        # if player == last_raiser:
            

    # for player in table.players_game:
                   

    # for player in table.players_game:
        
        

    # all players are either all in or folded or have called/checked/raised
    logger.debug(f"Betting round over")

    # create pots
    create_pots(table)