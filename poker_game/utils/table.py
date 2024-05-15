import logging
from collections import deque
from .players import Player

class Table:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.community_cards = []
        self.players = []
        self.starting_players = []
        self.pots = []
        self.players_game = deque()
        # self.seats = {}
        self.blind_size = 1
        self.dealer = None # Initially, there is no dealer
        self.small_blind_seat = 1
        self.big_blind_seat = 2

    # def add_chair(self, nr_of_chairs):
    #     for chair in range(0,nr_of_chairs):
    #         self.seats[chair] = None
    #         #self.logger.debug(f"Seat added, current table has {len(self.seats)}")

    def add_player(self, player):

        self.starting_players.append(player)
        # I am not sure if we still need this one, but added starting players because we remove players and I need the reference
        self.players.append(player)
        self.players_game.append(player)
        # If this is the first player added, set them as the dealer
        if len(self.players) == 1:
            self.set_dealer(0)
    
    def set_dealer(self, index):
        if 0 <= index < len(self.players):
            self.dealer = self.players[index]
        else:
            self.logger.error("Invalid index for dealer")
        # for chair in self.seats:
        #     if self.seats[chair] == None:
        #         self.seats[chair] = player
        #         self.players.append(player)
        #         self.logger.info(f"{player} got added to table on seat {chair}")
        #         break
    
    # def change_dealer_and_blinds(self):
    #     # this produces problems if someone leaves, the blind doesn't get transferred.
    #     self.logger.info(f"The current dealer was seating on seat {self.dealer_seat}")
    #     # Loop over table using helper function to determine next dealer
    #     # self.dealer_seat = next_player(self.seats, self.dealer_seat)
    #     self.dealer_seat += 1
    #     self.small_blind_seat += 1
    #     self.big_blind_seat += 1
    #     self.logger.info(f"The new dealer nr is {self.dealer_seat}")
    #     # Next person is small blind
    #     # self.small_blind_seat = next_player(self.seats, self.dealer_seat)
    #     # Next person is big blind
    #     # self.big_blind_seat = next_player(self.seats, self.small_blind_seat)

    def increase_blinds(self):
        self.blind_size = self.blind_size * 2

    def remove_player(self, player):
        self.players.remove(player)

    def set_community_cards(self, community_cards_list):
        self.community_cards = community_cards_list

