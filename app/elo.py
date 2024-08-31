def calculate_elo(rating_a, rating_b, score_a, k_factor=32):
    """
    Calculate the new Elo ratings for two players.
    
    :param rating_a: Current rating of player A
    :param rating_b: Current rating of player B
    :param score_a: Score of player A (1 for win, 0.5 for draw, 0 for loss)
    :param k_factor: K-factor for Elo calculation (default: 32)
    :return: Tuple of (new_rating_a, new_rating_b)
    """
    expected_a = 1 / (1 + 10 ** ((rating_b - rating_a) / 400))
    expected_b = 1 - expected_a

    new_rating_a = rating_a + k_factor * (score_a - expected_a)
    new_rating_b = rating_b + k_factor * ((1 - score_a) - expected_b)

    return round(new_rating_a), round(new_rating_b)

def update_ratings(player1, player2, winner):
    """
    Update player ratings based on game result.
    
    :param player1: Player 1 object
    :param player2: Player 2 object
    :param winner: Winner object (None for draw)
    """
    if winner == player1:
        score_a = 1
    elif winner == player2:
        score_a = 0
    else:
        score_a = 0.5

    new_rating_1, new_rating_2 = calculate_elo(player1.rating, player2.rating, score_a)

    player1.rating = new_rating_1
    player2.rating = new_rating_2
    player1.games_played += 1
    player2.games_played += 1