from .objects_on_table import Card
import logging
logger = logging.getLogger(__name__)


def card_rank_value(rank):
    if rank == None:
        return 0
    return '123456789TJQKA'.index(rank) + 1

def is_royal_or_straight_flush(sorted_hand):
   #logger.debug("Checking for Royal and/or Straight Flush...")
    for the_suit in ['♠','♥','♦','♣']:
        # omdat als ie nou een niet suited eentje naar beneden gaat? Dat sluit nu nog niks uit...
        suited_list = []
        for hand in sorted_hand:
            if hand.suit == the_suit:
                suited_list.append(hand)
        # 
        straight_suited_counter = 0
        if len(suited_list) != 0:
            if suited_list[0].rank == 'A':
                ##logger.debug(f'Found an ace')
                # USE + instead of .append as this doesn't mutate the original list.
                suited_list + [Card(rank='1', suit=the_suit)]
        ##logger.debug(f'New list: {suited_list}')
        for i in range(len(suited_list)-1):
            if card_rank_value(suited_list[i].rank) == card_rank_value(suited_list[i+1].rank) + 1:
                straight_suited_counter += 1
                if straight_suited_counter == 4:
                   #logger.debug(f"Straight Flush was Found with suit {the_suit}!!")
                    handscore = [8, suited_list[i - 3].rank, None, None, None, None]
                    return handscore
            elif card_rank_value(suited_list[i].rank) - card_rank_value(suited_list[i+1].rank) > 2:
                # 
                straight_suited_counter = 0 
                
       #logger.debug("No straight flush was Found.")
        return False           

def is_four_of_a_kind(sorted_hand):
   #logger.debug("Checking for Four of a Kind...")
    for i in range(len(sorted_hand) - 3):
        if sorted_hand[i].rank == sorted_hand[i + 1].rank == sorted_hand[i + 2].rank == sorted_hand[i + 3].rank:
           #logger.debug("Four of a Kind found!")
            quads_rank = sorted_hand[i].rank
            # it is OK to change this list as we are sure that it is four of a kind at this point
            sorted_hand.remove(sorted_hand[i])
            sorted_hand.remove(sorted_hand[i])
            sorted_hand.remove(sorted_hand[i])
            sorted_hand.remove(sorted_hand[i])
           #logger.debug(f"rest is now {sorted_hand}")
            return [7, quads_rank, sorted_hand[0].rank, None, None, None]
   #logger.debug("No Four of a Kind.")
    return False


def is_full_house(sorted_hand):
   #logger.debug("Checking for Full House...")
    first_handscore = is_three_of_a_kind(sorted_hand)
    if first_handscore != False:
       #logger.debug("Checking for another Pair...")
        for i in range(len(sorted_hand) - 1):
            if sorted_hand[i].rank == sorted_hand[i + 1].rank and sorted_hand[i].rank != first_handscore[1]:
               #logger.debug("Found a full house!")
                return [6, first_handscore[1], sorted_hand[i].rank, None, None, None]
   #logger.debug(f"No Full House")
    return False


def is_flush(sorted_hand):
   #logger.debug("Checking for Flush...")
    handscore = [5]
    for suit in ['♠','♥','♦','♣']:
        for card in sorted_hand:
            if card.suit == suit:
                handscore.append(card.rank)
                if len(handscore) == 6:
                   #logger.debug("Flush was Found!")
                    return handscore
        handscore = [5]
    return False


def is_straight(sorted_hand):
   #logger.debug("Checking for Straight...")
    
    # as there are nog 8 cards with the extra Ace possibility, needs different solving for straight flush
    straight_counter = 0
    if sorted_hand[0].rank == 'A':
        ##logger.debug(f'Found an ace')
        ace_suit = sorted_hand[0].suit
        ##logger.debug(f'old list: {sorted_hand}')
        sorted_hand.append(Card(rank='1', suit=ace_suit))
        ##logger.debug(f'New list: {sorted_hand}')
    for i in range(len(sorted_hand)-1):
        # just an extra card for each ace
        # )
        if card_rank_value(sorted_hand[i].rank) == card_rank_value(sorted_hand[i+1].rank) + 1:
            #  + 1, straight_counter)
            straight_counter += 1
            if straight_counter == 4:
               #logger.debug("Straight was Found!")
                handscore = [4, sorted_hand[i-3].rank, None, None, None, None]
                return handscore

        else: #card_rank_value(sorted_hand[i].rank) - card_rank_value(sorted_hand[i+1].rank) > 2:
            # } too big')
            straight_counter = 0

   #logger.debug("No straight found!")
    return False

def is_three_of_a_kind(sorted_hand):
    # 
   #logger.debug("Checking for Three of a Kind...")
    for i in range(len(sorted_hand) - 2):
        if sorted_hand[i].rank == sorted_hand[i + 1].rank == sorted_hand[i + 2].rank:
           #logger.debug("Three of a Kind found!")
            trips_rank = sorted_hand[i].rank
            # we need to make sure this is mutable as this gets called by is_full_house
            sorted_hand = sorted_hand.copy()
            sorted_hand.remove(sorted_hand[i])
            sorted_hand.remove(sorted_hand[i])
            sorted_hand.remove(sorted_hand[i])
           #logger.debug(f"rest is now {sorted_hand}")
            return [3, trips_rank, sorted_hand[0].rank, sorted_hand[1].rank, None, None]
   #logger.debug("No Three of a Kind.")
    return False

def is_two_pair(sorted_hand):
    # we need to make sure this is mutable as this gets called by is_full_house
    sorted_hand = sorted_hand.copy()
   #logger.debug("Checking for Two Pair...")
    pairs = 0
    for i in range(len(sorted_hand) - 3):
        if sorted_hand[i].rank == sorted_hand[i + 1].rank and pairs == 0:
           #logger.debug("First pair found...")

            # remove the two cards to easily access the kickers                
            first_pair_rank = sorted_hand[i].rank
            sorted_hand.remove(sorted_hand[i])
            sorted_hand.remove(sorted_hand[i])
           #logger.debug(f"rest is now {sorted_hand}")

            pairs += 1
        if sorted_hand[i].rank == sorted_hand[i + 1].rank and pairs == 1:
           #logger.debug("Two pair found!")
            second_pair_rank = sorted_hand[i].rank
            sorted_hand.remove(sorted_hand[i])
            sorted_hand.remove(sorted_hand[i])
            ##logger.debug(f"rest is now {sorted_hand}")
            handscore = [2, first_pair_rank, second_pair_rank, sorted_hand[0].rank, None, None]
            return handscore
        # fill the rest with first, second and third kicker
   #logger.debug(f"No two Pair!")
    return False

def is_one_pair(sorted_hand):
   #logger.debug("Checking for One Pair...")
    for i in range(len(sorted_hand) - 1):
        if sorted_hand[i].rank == sorted_hand[i + 1].rank:
           #logger.debug("One Pair found!")

            # remove the two cards to easily access the kickers
            pair_rank = sorted_hand[i].rank
            sorted_hand.remove(sorted_hand[i])
            sorted_hand.remove(sorted_hand[i])
            ##logger.debug(f"7-2={sorted_hand}")
            
            # fill the rest with first, second and third kicker
            handscore = [1, pair_rank, sorted_hand[0].rank, sorted_hand[1].rank, sorted_hand[2].rank, None]
            ##logger.debug(f"Handscore = {handscore}")
            return handscore
   #logger.debug("No One Pair.")
    return False

def evaluate_hand(all_cards):
    sorted_hand = sorted(all_cards, key=lambda card: card_rank_value(card.rank), reverse=True)
   #logger.debug(f"...Checking for different hand Ranks.. for {sorted_hand}")

    sorted_hand = sorted_hand.copy()
    hand_rank = is_royal_or_straight_flush(sorted_hand)
    if hand_rank == False:
        hand_rank = is_four_of_a_kind(sorted_hand)
    if hand_rank == False:
        hand_rank = is_full_house(sorted_hand)
    if hand_rank == False:
        hand_rank = is_flush(sorted_hand)
    if hand_rank == False:
        hand_rank = is_straight(sorted_hand)
    if hand_rank == False:
        hand_rank = is_three_of_a_kind(sorted_hand)
    if hand_rank == False:
        hand_rank = is_two_pair(sorted_hand)
    if hand_rank == False:
        hand_rank = is_one_pair(sorted_hand)
    if hand_rank == False:
       #logger.debug("Return high card...")
        hand_rank = [0, sorted_hand[0].rank, sorted_hand[1].rank, sorted_hand[2].rank, sorted_hand[3].rank, sorted_hand[4].rank]
    return hand_rank


def get_hand_rank(player, table):
   #logger.debug(f"...Checking for different hand Ranks for {player.name }")
    all_cards = player.hand + [Card(card[0], card[1]) for card in table.community_cards]
    hand_rank = evaluate_hand(all_cards)
    ##logger.debug(f"The best hand is {hand_rank}")
    return hand_rank