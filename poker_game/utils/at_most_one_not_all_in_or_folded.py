def check_at_most_one_not_all_in_or_folded(table):
    # Count players who are neither all-in nor folded
    count_not_all_in_or_folded = sum(not (player.all_in or player.folded) for player in table.players_game)

    # Check if at most one player is not all-in or folded
    if count_not_all_in_or_folded <= 1:
        # print("At most one player is not all-in or folded.")
        return True
    else:
        # print("More than one player is still active.")
        return False