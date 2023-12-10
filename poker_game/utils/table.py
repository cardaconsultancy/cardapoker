import logging
from collections import deque

class Table:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.community_cards = []
        self.players = []
        self.players_game = deque()
        # self.seats = {}
        self.blind_size = 1
        self.dealer_seat = 0
        self.small_blind_seat = 1
        self.big_blind_seat = 2

    # def add_chair(self, nr_of_chairs):
    #     for chair in range(0,nr_of_chairs):
    #         self.seats[chair] = None
    #         self.logger.debug(f"Seat added, current table has {len(self.seats)}")

    def add_player(self, player):
        self.players.append(player)
        self.players_game.append(player)
        # for chair in self.seats:
        #     if self.seats[chair] == None:
        #         self.seats[chair] = player
        #         self.players.append(player)
        #         self.logger.info(f"{player} got added to table on seat {chair}")
        #         break
    
    def change_dealer_and_blinds(self):
        # this produces problems if someone leaves, the blind doesn't get transferred.
        self.logger.info(f"The current dealer was seating on seat {self.dealer_seat}")
        # Loop over table using helper function to determine next dealer
        # self.dealer_seat = next_player(self.seats, self.dealer_seat)
        self.dealer_seat += 1
        self.small_blind_seat += 1
        self.big_blind_seat += 1
        self.logger.info(f"The new dealer nr is {self.dealer_seat}")
        # Next person is small blind
        # self.small_blind_seat = next_player(self.seats, self.dealer_seat)
        # Next person is big blind
        # self.big_blind_seat = next_player(self.seats, self.small_blind_seat)

    def increase_blinds(self):
        self.blind_size = self.blind_size * 2

    def remove_player(self, player):
        self.players.remove(player)

    def set_community_cards(self, community_cards_list):
        self.community_cards = community_cards_list

