def find_next_dealer(starting_players, active_players, current_dealer):
    if not active_players or not starting_players:
        return None  # Return None if either list is empty

    # Finding the index of the current dealer in the starting players
    try:
        current_index = starting_players.index(current_dealer)
    except ValueError:
        # If current dealer is not in starting players, start from the beginning
        current_index = -1

    # Start searching for the next active dealer
    total_players = len(starting_players)
    for i in range(total_players):
        next_index = (current_index + 1 + i) % total_players
        next_dealer = starting_players[next_index]
        if next_dealer in active_players:
            return next_dealer

    return None  # In case no active players are found in starting players, though this should ideally never happen


# Example usage:
active_players = ["Alice", "jaja"]
starting_players = ["Alice", "jaja", "Bob", "Dana", "Charlie", "Diana"]
current_dealer = "Bob"

next_dealer = find_next_dealer(starting_players, active_players, current_dealer)
print(f"The next dealer is {next_dealer}")
