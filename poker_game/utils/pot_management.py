from .objects_on_table import Pot
from .clean_up import clean_up
import logging

logger = logging.getLogger(__name__)

def create_pots(table):
    logger.debug(f"Start to create pot(s)")

    # if there are no pots, create one.
    if len(table.pots) == 0:
        main_pot = Pot()
        main_pot.players = [player for player in table.players_game if player.folded == False]
        table.pots.append(main_pot)
        logger.debug(f"No pot yet, so created {len(table.pots)} main pot")
    check_for_side_pots(table)

    # reset the bets and raise/check/call status
    for player in table.players_game:
        # player.total_in_pots_this_game += player.total_bet_betting_round
        player.raised_called_or_checked_this_round = False
        player.total_bet_betting_round = 0
        logger.debug(f"Reset total bets {player.name} to {player.total_bet_betting_round}")



def check_if_rest_folded_and_pay(table):
    at_least_two_not_folded_or_out = []
    for player in table.players_game:
        
        # Questionable whether to use the 'folded' criteria here, as it does not create a necessary pot for 
        # the situation where there is a folded player that has betted more than one pot.
        # Alternative would be to change the payout system.
        
        if player.folded == False:
            at_least_two_not_folded_or_out.append(player)
    if len(at_least_two_not_folded_or_out) < 2:
        create_pots(table) # <-- why do this?
        # skip all
        for pot in table.pots:
            at_least_two_not_folded_or_out[0].chips.win(pot.amount)
            print('does this ever run now??????')
            AttributeError()
        clean_up()
        return 1

def check_if_only_one_player_left(table):
    if len([player for player in table.players_game if player.folded != True]) == 1:
        winner = table.players_game[0]
        logger.info(f"Only 1 left: {winner.name}, so immediately do payout")
        for pot in table.pots:
            logger.info(f"Empty pot {pot.players}")
            winner.chips.win(pot.amount)
            table.pots.remove(pot)
        for player in table.players_game:
            winner.chips.win(player.total_bet_betting_round)
            player.total_bet_betting_round = 0
        return True
        
def check_for_side_pots(table):
    # use total betting round as an indicator to get out of the loop. Keep reducing it untill every player has 0.

    logger.debug(f"checking for side pots")

    # check_for_side_pots = True
    sidepot_created = False
    counter = 1
    while any(player.total_bet_betting_round != 0 for player in table.players):

        # get the minimum bet from the people that did not fold:
        not_folded_or_out = []
        for player in table.players_game:
            # get all the minimum bet, need to check for 0 also as we reduce the total_betting_round
            if player.folded == False and player.total_bet_betting_round > 0:
                not_folded_or_out.append(player)

        # get the lowest bet in not-folded
        lowest_bet = min([player.total_bet_betting_round for player in not_folded_or_out])
        logger.debug(f"1. Lowest bet is {lowest_bet}")
        
        # if len(not_folded_or_out) > 2:
        #     AssertionError

        if len(not_folded_or_out) < 2:
            raise Exception("this should have been caught earlier on")

        # check if there is only 1 person not all in amongst the non-folders (and the other one is, reduce his/her bet by the difference with the max bidder).
        elif len([player for player in not_folded_or_out if not player.all_in]) == 1 and len([player for player in not_folded_or_out if player.all_in]) == 1:
            logger.debug(f"2. Only one player not all in")

            # Find the player who is not all-in: the folded 60
            non_all_in_player = next(player for player in not_folded_or_out if not player.all_in)
            # print(non_all_in_player.name)

            # Find the max bet among all-in players
            all_in_bet = max(player.total_bet_betting_round for player in not_folded_or_out if player.all_in)
            # print(all_in_bet, non_all_in_player.total_bet_betting_round)

            # This is the only case in which we give players back money in mid game as we cannot guarantee who joins:
            non_all_in_player.chips.give_back(non_all_in_player.total_bet_betting_round - all_in_bet)

            # Adjust the bet of the non all-in player
            logger.debug(f"As {non_all_in_player.name} was the only one not all in, his/her will be reduced by {non_all_in_player.total_bet_betting_round - all_in_bet}")
            non_all_in_player.total_bet_betting_round = all_in_bet

        # check if the players all betted the same amount, if so take shortcut (also necessary to prevent loop):
        if lowest_bet == max([player.total_bet_betting_round for player in not_folded_or_out]):
            logger.debug(f"99. Every player is in with the same amount")

            # get the first out of not_folded_or_out
            fill_current_pot(not_folded_or_out[0], table)
            return None
        
        counter += 1
        # check_for_side_pots = False

        # for every player that has not folded already:
        for player in not_folded_or_out[:]:
            logger.debug(f"check player:{player.name}")
            logger.debug(f"nr of players in not_folded_or_out: {len(not_folded_or_out)}")
            logger.debug(f"total bet (left) this round: {player.total_bet_betting_round}")
            logger.debug(f"lowest bet: {lowest_bet}")

            # check if they have the lowest bid
            if player.total_bet_betting_round == lowest_bet:
                logger.debug(f"player {player.name} has the lowest bet of {lowest_bet}")

                # check if there is at least one player that went all in (if multiple no problem)... 
                if player.all_in == True:
                    logger.debug(f"player {player.name} went all in, side pot is needed")
                    # fill up original pot & create side pot
                    fill_current_pot(player, table)
                    logger.debug(f"after filling the pot {player.total_bet_betting_round} is left")

                    side_pot = Pot()

                    # do this in the fill current pot
                    # side_pot.players = not_folded_or_out

                    table.pots.append(side_pot)
                    sidepot_created = True
                    # check_for_side_pots = True
                    # player.folded = True
                    # not_folded_or_out.remove(player)
                    # print(f'the rest of the list {not_folded_or_out}')
            # elif player.total_bet_betting_round == 0 and player.folded == False:
            #     logger.debug(f"{player.name} also went all in with the minimum bet")
            #     not_folded_or_out.remove(player)
            #     print(f'the rest of the list {not_folded_or_out}')
        if sidepot_created == False:
            logger.debug(f"No (more) sidepots created")
            # just get a person that did not fold, as there are no sidepots his/her bet will be the same as the others.
            fill_current_pot(not_folded_or_out[0], table)
            # for pot in table.pots:
            #     print(f'---------- pot {pot} is {pot.amount}')
            return None
                    # get the minimum bet fromt he people that did not fold:
        
        # check_for_side_pots = True
        logger.debug(f"A sidepot was created")


def fill_current_pot(lowest_player, table):
    logger.debug(f"-- Fill the current pot --")
    lowest_bet = lowest_player.total_bet_betting_round
    current_pot = table.pots[-1]
    # reset the participants
    current_pot.players = []
    # you HAVE TO use players here, as you can still get some of your big blind back if the person you beat has less chips than that.
    # and p1 can raise to 60, p2 goes all in with 10, p3 raises to 600, p4 calls, p1 folds. Then p1 fills pot 1 AND the main pot.
    for player in table.players:

        # if the player has folded or called with more than was required, save that for the next pot.
        if player.total_bet_betting_round >= lowest_bet:
            logger.debug(f"{player.name} has betted enough, check if it is more than was necessary for this pot")

            # fill the pot with the minimum bet
            current_pot.amount += lowest_bet
            logger.debug(f"the new pot holds {current_pot.amount} chips")
            
            # reduce the betting amount with the lowest bet
            player.total_bet_betting_round = player.total_bet_betting_round - lowest_bet

            # if player folded, he or she does not take part in any of the winnings
            if player.folded == False:
                logger.debug(f"Player {player.name} has not folded and will be part of the winnings.")
                current_pot.players.append(player)
        
        # if they have less betted than the lowest bet
        elif player.total_bet_betting_round < lowest_bet:
            logger.debug(f"{player.name} bet ({player.total_bet_betting_round}) is lower than {lowest_bet} and hence this person will always be folding because we checked for this before")
            logger.debug(f"Player {player.name} has folded or is out of chips and will not be part of the winnings.")

            # increase the amount in the pot
            current_pot.amount += player.total_bet_betting_round
            logger.debug(f"the new pot holds {current_pot.amount} chips")

            # reduce the betting amount to 0
            player.total_bet_betting_round = 0
            logger.debug(f"{player.name} bet is down to {player.total_bet_betting_round}")

            current_pot.amount += player.total_bet_betting_round
            logger.debug(f"{player.name} bet is {player.total_bet_betting_round}")
            
    # side_pot.players.append(player)
    # table.pots.append(side_pot)