"""The logic of the poker round is here."""

import logging
from poker_game.Timer import timeout
from poker_game.utils.at_most_one_not_all_in_or_folded import (
    all_but_one_folded_or_all_in,
)
from poker_game.utils.betting_round import betting_round_completed
from poker_game.utils.clean_up import clean_up
from poker_game.utils.get_and_pay_winners import pay_winners
from poker_game.utils.objects_on_table import Deck
from poker_game.utils.pot_management import check_if_rest_folded_and_pay

# Retrieve the already configured logger
logger = logging.getLogger("poker_game")


@timeout(5)  # Set timeout to 5 seconds
def play_round(table, test_cards=None, seed=None):
    """Play 1 round of poker."""

    # log new Round
    logger.info("--- New Round ---")
    logger.info("table = Table()")
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

        # TODO: remove this lines when the game is stable
        # for the ease of debugging
        strategy_mapping = {
            "AggressivePlayer": "aggressive",
            "SuperAggressivePlayer": "super_aggressive",
            "ConservativePlayer": "conservative",
            "AlwaysFoldPlayer": "always_fold",
            "Raises_with_aces_reduces_with_12345Player": "raises_with_aces_reduces_with_12345",
            "careful_calculator_Player": "careful_calculator",
            "ActualPlayerTemplate": "default",
            "CompletelyRandomPlayer": "completely_random",
        }
        # create logger info in the form of A = create_player("A", "raises_with_aces_reduces_with_12345", Chips(15))
        logger.info(
            '{player.name} = create_player("%s", "%s", Chips(%s))',
            player.name,
            strategy_mapping[player.__class__.__name__],
            player.chips.amount,
        )

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
    for player in table.players_game:

        # I will separate logging and dashboarding in the future
        # logger.info(f'{player.name}-{player.hand[0].rank}{player.hand[0].suit}{player.hand[1].rank}{player.hand[1].suit}')
        # logger.info(
        #     '%s.hand = [Card("%s", "%s"), Card("%s", "%s")]' % (
        #         player.name, 
        #         player.hand[0].rank, player.hand[0].suit, 
        #         player.hand[1].rank, player.hand[1].suit
        #     )
        # ) 


        logger.debug(f"Player {player.name} has {player.hand}")

    # Betting Round 1, note that preflop_round is set to True
    logger.debug("Players can make their first bet.")
    if not betting_round_completed(table, preflop_round=True):
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

        if not betting_round_completed(table):
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
        if not betting_round_completed(table):
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

    # log river
    # logger.info(f'{table.community_cards[4].rank}{table.community_cards[4].suit}')

    # for debugging purposes while running random simulations, this made life easier to copy paste
    # logger.info(
    #     f'test_cards = [Card("{table.community_cards[0].rank}", "{table.community_cards[0].suit}"), Card("{table.community_cards[1].rank}", "{table.community_cards[1].suit}"), Card("{table.community_cards[2].rank}", "{table.community_cards[2].suit}"), Card("{table.community_cards[3].rank}", "{table.community_cards[3].suit}"), Card("{table.community_cards[4].rank}", "{table.community_cards[4].suit}")]'
    # )

    logger.debug(
        "On the table comes %s of %s.",
        table.community_cards[4].rank,
        table.community_cards[4].suit,
    )

    # Betting Round 4, the river
    if not all_but_one_folded_or_all_in:
        logger.debug("Players can bet on the river, final bet!")
        if not betting_round_completed(table):
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
    pay_winners(table)

    # debugger to identify errors in long simulations
    # if sum(player.chips.amount for player in table.players) != 600:
    #     AttributeError("The total amount of chips is not 600")
    #     logger.debug(sum(player.chips.amount for player in table.players))

    # Clean up
    clean_up(table)

    return table
