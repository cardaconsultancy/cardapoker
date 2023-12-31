from .objects_on_table import Pot
from .clean_up import clean_up
import logging

logger = logging.getLogger(__name__)

def create_pots(table):
    logger.debug(f"Start to create pot(s)")
    if len(table.pots) == 0:
        main_pot = Pot()
        main_pot.players = table.players_game
        table.pots.append(main_pot)
        logger.debug(f"No pot yet, so created {len(table.pots)} main pot")
    check_for_side_pots(table)
    required_action = 100

    # reset the bets and raise/check/call status
    for player in table.players_game:
        player.total_in_pots_this_game += player.total_bet_betting_round
        player.raised_called_or_checked_this_round = False
        player.total_bet_betting_round = 0
        logger.debug(f"Reset total bets {player.name} to {player.total_bet_betting_round}")

def check_if_rest_folded_and_pay(table):
    at_least_two_not_folded = []
    for player in table.players_game:
        if player.folded == False:
            at_least_two_not_folded.append(player)
    if len(at_least_two_not_folded) < 2:
        # skipp_all
        for pot in table.pots:
            at_least_two_not_folded[0].chips.win(pot.amount)
        clean_up()
        return 1

def check_for_side_pots(table):
    # use total betting round as an indicator to get out of the loop. Keep reducing it untill every player has 0.

    logger.debug(f"checking for side pots")

    # get the minimum bet fromt he people that did not fold:
    not_folded = []
    for player in table.players_game:
        # get all the minimum bet
        if player.folded == False:
            not_folded.append(player)
    # check_for_side_pots = True
    sidepot_created = False
    counter = 1
    while any(player.total_bet_betting_round != 0 for player in table.players):
        
        # get the lowest bet in folded, need to check for 0 also as we reduce the total_betting_round
        lowest_bet = min([player.total_bet_betting_round for player in not_folded if player.total_bet_betting_round != 0])
        logger.debug(f"1. Lowest bet is {lowest_bet}")
        
        # throw error if len not folded > 2
        if len(not_folded) > 2:
            AssertionError

        # check if there is only 1 person not all in amongst the non-folders, reduce his/her bet by the difference with the max bidder.
        if len([player for player in not_folded if not player.all_in]) == 1:
            logger.debug(f"2. Only one player not all in")

            # Find the player who is not all-in: the folded 60
            non_all_in_player = next(player for player in not_folded if not player.all_in)
            # print(non_all_in_player.name)

            # Find the max bet among all-in players: 600
            all_in_bet = max(player.total_bet_betting_round for player in not_folded if player.all_in)
            # print(all_in_bet, non_all_in_player.total_bet_betting_round)

            # This is the only case in which we give players back money in mid game as we cannot guarantee who joins:
            non_all_in_player.chips.give_back(non_all_in_player.total_bet_betting_round - all_in_bet)

            # Adjust the bet of the non all-in player
            non_all_in_player.total_bet_betting_round = all_in_bet
            logger.debug(f"As {non_all_in_player.name} was the only one not all in, his/her bet got reduced by {non_all_in_player.total_bet_betting_round - all_in_bet}")

        # check if the players all betted the same amount, if so take shortcut (also necessary to prevent loop):
        if lowest_bet == max([player.total_bet_betting_round for player in not_folded]):
            logger.debug(f"99. Every player is in with the same amount")
            # check_for_side_pots = False
            fill_current_pot(not_folded[0], table)
            return None
        
        counter += 1
        print('Looping for more side pots')
        # check_for_side_pots = False

        # for every player that has not folded already:
        for player in not_folded[:]:
            print('check player:', player.name)
            print('nr of players in not_folded:', len(not_folded))
            print(player.total_bet_betting_round)
            print('lowest bet: ', lowest_bet)

            # check if they have the lowest bid
            if player.total_bet_betting_round == lowest_bet:
                logger.debug(f"player {player.name} has the lowest bet of {lowest_bet}")

                # check if the lowest gambling player went all in
                if player.all_in == True:
                    logger.debug(f"player {player.name} went all in, side pot is needed")
                    # fill up original pot & create side pot
                    fill_current_pot(player, table)
                    side_pot = Pot()

                    # do this in the fill current pot
                    # side_pot.players = not_folded

                    table.pots.append(side_pot)
                    sidepot_created = True
                    # check_for_side_pots = True
                    # player.folded = True
                    # not_folded.remove(player)
                    # print(f'the rest of the list {not_folded}')
            # elif player.total_bet_betting_round == 0 and player.folded == False:
            #     logger.debug(f"{player.name} also went all in with the minimum bet")
            #     not_folded.remove(player)
            #     print(f'the rest of the list {not_folded}')
        if sidepot_created == False:
            logger.debug(f"No (more) sidepots created")
            # just get a person that did not fold, as there are no sidepots his/her bet will be the same as the others.
            fill_current_pot(not_folded[0], table)
            for pot in table.pots:
                print(f'---------- pot {pot} is {pot.amount}')
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

            # increase the amount in the pot
            current_pot.amount += player.total_bet_betting_round
            logger.debug(f"the new pot holds {current_pot.amount} chips")

            # reduce the betting amount to 0
            player.total_bet_betting_round = 0
            logger.debug(f"{player.name} bet is down to {player.total_bet_betting_round}")

            current_pot.amount += player.total_bet_betting_round
            logger.debug(f"{player.name} bet is {player.total_bet_betting_round}")
            # add them to the list if they call
            current_pot.players.append(player)
            
    # side_pot.players.append(player)
    # table.pots.append(side_pot)