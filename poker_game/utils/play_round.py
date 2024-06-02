"""The logic of the poker round is here."""

import logging
import datetime
from poker_game.Timer import timeout
from poker_game.utils.at_most_one_not_all_in_or_folded import (
    all_but_one_folded_or_all_in,
)
from poker_game.utils.betting_round import betting_round_completed
from poker_game.utils.clean_up import clean_up
from poker_game.utils.get_and_pay_winners import pay_winners
from poker_game.utils.objects_on_table import Card, Chips, Deck
from poker_game.utils.players import create_player
from poker_game.utils.pot_management import check_if_rest_folded_and_pay
from poker_game.utils.set_up_database import (
    log_active_players,
    log_round_players_chips_cards,
)
from poker_game.utils.set_up_database import log_betting_activity
from poker_game.utils.set_up_database import log_cards_player


# Retrieve the already configured logger
logger = logging.getLogger("poker_game")


@timeout(5)  # Set timeout to 5 seconds
def play_round(table, test_cards=None, seed=None):
    """Play 1 round of poker."""

    # log new Round
    logger.info("--- New Round ---")
    logger.info("table = Table()")
    round_id = str(datetime.datetime.now())
    # round_id = log_new_round(timing)  # Log the new round and get its ID

    # reset the deck
    deck = Deck(seed=seed)

    # Reset community cards at the beginning of each round
    table.community_cards = []

    # print the dealer button
    logger.debug("the dealer is %s", table.dealer.name)

    # copy the player list to easily keep track of players
    table.players_game = table.players

    # log the blind size
    logger.info("table.blind_size = %s", table.blind_size)

    # Deal the first private card to each player
    # (Chosen to stay the closest to the real game, by not dealing two at once)
    for player in table.players_game:

        # log the amount of chips each player has
        # logger.info(f"{player.name}-chips-{player.chips.amount}")

        # # TODO: remove this lines when the game is stable
        # # for the ease of debugging
        # strategy_mapping = {
        #     "AggressivePlayer": "aggressive",
        #     "SuperAggressivePlayer": "super_aggressive",
        #     "ConservativePlayer": "conservative",
        #     "AlwaysFoldPlayer": "always_fold",
        #     "Raises_with_aces_reduces_with_12345Player": "raises_with_aces_reduces_with_12345",
        #     "careful_calculator_Player": "careful_calculator",
        #     "ActualPlayerTemplate": "default",
        #     "CompletelyRandomPlayer": "completely_random",
        # }
        # # create logger info in the form of A = create_player("A", "raises_with_aces_reduces_with_12345", Chips(15))
        # logger.info(
        #     '{player.name} = create_player("%s", "%s", Chips(%s))',
        #     player.name,
        #     strategy_mapping[player.__class__.__name__],
        #     player.chips.amount,
        # )

        # in case of a test with predefined cards, we don't want to give
        # the player any cards
        if len(player.hand) == 0:
            player.receive_card(deck.deal())
        else:
            logger.debug(
                "Player %s already has cards ---- TEST ROUND -----", player.name
            )

    # Deal the second private card to each player
    for player in table.players_game:
        if len(player.hand) == 1:
            player.receive_card(deck.deal())

    # Log each player's hand
    for gambler in table.players_game:
        log_active_players(
            round_id=round_id,
            player_name=gambler.name,
            player_strategy=player.__class__.__name__,
            player_card_1_rank=gambler.hand[0].rank,
            player_card_1_suit=gambler.hand[0].suit,
            player_card_2_rank=gambler.hand[1].rank,
            player_card_2_suit=gambler.hand[1].suit,
        )

        # I will separate logging and dashboarding in the future
        # logger.info(f'{player.name}-{player.hand[0].rank}{player.hand[0].suit}{player.hand[1].rank}{player.hand[1].suit}')
        # logger.info(
        #     '%s.hand = [Card("%s", "%s"), Card("%s", "%s")]' % (
        #         player.name,
        #         player.hand[0].rank, player.hand[0].suit,
        #         player.hand[1].rank, player.hand[1].suit
        #     )
        # )

        # log_cards_player(round_id=round_id, card_1_rank=gambler.hand[0].rank, card_1_suit=gambler.hand[0].suit, card_2_rank=gambler.hand[1].rank, card_2_suit=gambler.hand[1].suit)
        # logger.debug(f"Player {gambler.name} has {gambler.hand}")

    # Betting Round 1, note that preflop_round is set to True
    logger.debug("Players can make their first bet.")
    if not betting_round_completed(table, preflop_round=True, round_id=round_id):
        logger.debug("!!!!!!!!!!!!!!everybody folded!!!!!!!!!!!!!!!")
        clean_up(table)
        return table
    if check_if_rest_folded_and_pay(table):
        print("obsolete")
        return table

    logger.debug("Bets are made")
    logger.debug(
        f"Total betted {sum(player.total_in_pots_this_game for player in table.players)}."
    )

    # Deal the flop (three community cards) if no test cards are provided
    if test_cards is None:
        table.community_cards.append(deck.deal())
        table.community_cards.append(deck.deal())
        table.community_cards.append(deck.deal())
    else:
        table.community_cards.extend(test_cards[0:3])

    # log flop
    logger.info(
        f'[Card("{table.community_cards[0].rank}", "{table.community_cards[0].suit}"), Card("{table.community_cards[1].rank}", "{table.community_cards[1].suit}"), Card("{table.community_cards[2].rank}", "{table.community_cards[2].suit}"),'
    )

    # Betting Round 2: flop
    if not all_but_one_folded_or_all_in(table):
        logger.debug("Players can bet on the flop.")

        # Start the betting round and check if the betting round is completed
        # If not completed, the table is cleaned up

        if not betting_round_completed(table, round_id=round_id):
            logger.debug("!!!!!!!!!!!!!!everybody folded!!!!!!!!!!!!!!!")
            clean_up(table)
            return table
        logger.debug(
            f"Total is {sum(player.total_in_pots_this_game for player in table.players)}."
        )
    else:
        logger.debug("All but one are all in, so no more bets!")
    # TODO delete this line if not needed
    if check_if_rest_folded_and_pay(table):
        print("obsolete")
        return True

    # Deal the turn (one additional community card) if no test cards are provided
    if test_cards is None:
        table.community_cards.append(deck.deal())
    else:
        logger.debug("TEST")
        table.community_cards.append(test_cards[3])

    # log turn
    # logger.info(f'{table.community_cards[3].rank}{table.community_cards[3].suit}')
    logger.info(
        f'[Card("{table.community_cards[0].rank}", "{table.community_cards[0].suit}"), Card("{table.community_cards[1].rank}", "{table.community_cards[1].suit}"), Card("{table.community_cards[2].rank}", "{table.community_cards[2].suit}"), Card("{table.community_cards[3].rank}", "{table.community_cards[3].suit}"),'
    )
    logger.debug(
        f"On the table comes {table.community_cards[3].rank} of {table.community_cards[3].suit}."
    )

    # Betting Round 3, the turn

    # Check if all players are all-in or folded
    if not all_but_one_folded_or_all_in:
        logger.debug("Players can bet on the turn.")
        if not betting_round_completed(table, round_id=round_id):
            logger.debug("!!!!!!!!!!!!!!everybody folded!!!!!!!!!!!!!!!")
            clean_up(table)
            return table
        logger.debug(
            f"Total is %s{sum(player.total_in_pots_this_game for player in table.players)}."
        )
    else:
        logger.debug("All but one are all in, so no more bets!")

    # TODO delete this line if not needed
    if check_if_rest_folded_and_pay(table):
        print("obsolete")
        return True

    # Deal the river (one final community card)
    if test_cards is None:
        table.community_cards.append(deck.deal())
    else:
        logger.debug("TEST")
        table.community_cards.append(test_cards[4])

    # log the cards...
    # but what happens if everybody folds? Did that never happen... do we still show cards?
    # TODO

    # BACKUP METHOD IF ANALYSIS IS MORE TROUBLESOME THAN EXPECTED:
    # Instead of logging only the players that are still in the game, we log all seats
    # Log each player's hand by creating another seatlist
    # seat_counter = 0
    # seat_list = []
    # for seat in table.starting_players_and_seats:
    #     if seat not in table.players:
    #         logger.debug("Player %s is out of the game", seat.name)
    #         empty_seat = create_player(f"Empty_seat_of {seat.name}", "conservative", Chips(0))
    #         empty_seat.hand = [Card(None, None), Card(None, None)]
    #         seat_list.append(empty_seat)
    #     else:
    #         seat_list.append(seat)
    #     seat_counter += 1

    # # this should happen at the game level, not at the round level so we only need to loop once.
    # # I will do it here now to prevent my next functions to crash
    # if seat_counter < 6:
    #     logger.debug("We need to add empty seats")
    #     for i in range(6 - seat_counter):
    #         empty_seat = create_player(f"Empty_seat{i}", "conservative", Chips(0))
    #         empty_seat.hand = [Card(None, None), Card(None, None)]
    #         seat_list.append(empty_seat)

    # for seat in seat_list:
    #     print(seat.name, seat.hand)

    logger.debug(
        "On the table comes %s of %s.",
        table.community_cards[4].rank,
        table.community_cards[4].suit,
    )

    # Betting Round 4, the river
    if not all_but_one_folded_or_all_in:
        logger.debug("Players can bet on the river, final bet!")
        if not betting_round_completed(table, round_id=round_id):
            logger.debug("!!!!!!!!!!!!!!everybody folded!!!!!!!!!!!!!!!")
            clean_up(table)
            return table
        logger.debug(
            "Total is %s",
            sum(player.total_in_pots_this_game for player in table.players),
        )
    else:
        logger.debug("All but one are all in, so no more bets!")

    # TODO delete this line if not needed
    if check_if_rest_folded_and_pay(table):
        print("obsolete")
        return True

    # Determine the winner(s)
    logger.debug("Pay_the_winner(s)")
    pay_winners(table=table, round_id=round_id)

    # log the cards and the chips
    log_round_players_chips_cards(
        round_id=round_id,
        card_1_rank=table.community_cards[0].rank,
        card_1_suit=table.community_cards[0].suit,
        card_2_rank=table.community_cards[1].rank,
        card_2_suit=table.community_cards[1].suit,
        card_3_rank=table.community_cards[2].rank,
        card_3_suit=table.community_cards[2].suit,
        card_4_rank=table.community_cards[3].rank,
        card_4_suit=table.community_cards[3].suit,
        card_5_rank=table.community_cards[4].rank,
        card_5_suit=table.community_cards[4].suit,  # ,
        # player1=seat_list[0].name,
        # player2=seat_list[1].name,
        # player3=seat_list[2].name,
        # player4=seat_list[3].name,
        # player5=seat_list[4].name,
        # player6=seat_list[5].name,
        # player1_card_1_rank=seat_list[0].hand[0].rank,
        # player1_card_1_suit=seat_list[0].hand[0].suit,
        # player1_card_2_rank=seat_list[0].hand[1].rank,
        # player1_card_2_suit=seat_list[0].hand[1].suit,
        # player2_card_1_rank=seat_list[1].hand[0].rank,
        # player2_card_1_suit=seat_list[1].hand[0].suit,
        # player2_card_2_rank=seat_list[1].hand[1].rank,
        # player2_card_2_suit=seat_list[1].hand[1].suit,
        # player3_card_1_rank=seat_list[2].hand[0].rank,
        # player3_card_1_suit=seat_list[2].hand[0].suit,
        # player3_card_2_rank=seat_list[2].hand[1].rank,
        # player3_card_2_suit=seat_list[2].hand[1].suit,
        # player4_card_1_rank=seat_list[3].hand[0].rank,
        # player4_card_1_suit=seat_list[3].hand[0].suit,
        # player4_card_2_rank=seat_list[3].hand[1].rank,
        # player4_card_2_suit=seat_list[3].hand[1].suit,
        # player5_card_1_rank=seat_list[4].hand[0].rank,
        # player5_card_1_suit=seat_list[4].hand[0].suit,
        # player5_card_2_rank=seat_list[4].hand[1].rank,
        # player5_card_2_suit=seat_list[4].hand[1].suit,
        # player6_card_1_rank=seat_list[5].hand[0].rank,
        # player6_card_1_suit=seat_list[5].hand[0].suit,
        # player6_card_2_rank=seat_list[5].hand[1].rank,
        # player6_card_2_suit=seat_list[5].hand[1].suit,
        # player1_chips_end=seat_list[0].chips.amount,
        # player2_chips_end=seat_list[1].chips.amount,
        # player3_chips_end=seat_list[2].chips.amount,
        # player4_chips_end=seat_list[3].chips.amount,
        # player5_chips_end=seat_list[4].chips.amount,
        # player6_chips_end=seat_list[5].chips.amount,
    )

    # debugger to identify errors in long simulations
    # if sum(player.chips.amount for player in table.players) != 600:
    #     AttributeError("The total amount of chips is not 600")
    #     logger.debug(sum(player.chips.amount for player in table.players))

    # Clean up
    clean_up(table)

    return table
