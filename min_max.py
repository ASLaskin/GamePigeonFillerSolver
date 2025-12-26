def get_best_move(game, depth):
    best_score = float('-inf')
    best_move = None

    for move in game.get_available_moves():
        game_copy = game.clone()
        game_copy.make_move(move)
        score = minimax(game_copy, depth - 1, float('-inf'), float('inf'), False)

        if score > best_score:
            best_score = score
            best_move = move

    return best_move


def minimax(game, depth, alpha, beta, maximizing_player):
    if depth == 0 or is_over(game) or not game.get_available_moves():
        return evaluate(game)

    if maximizing_player:
        best_score = float('-inf')
        for move in game.get_available_moves():
            game_copy = game.clone()
            game_copy.make_move(move)
            score = minimax(game_copy, depth - 1, alpha, beta, False)
            best_score = max(best_score, score)
            alpha = max(alpha, best_score)
            if alpha >= beta:
                break
        return best_score
    else:
        best_score = float('inf')
        for move in game.get_available_moves():
            game_copy = game.clone()
            game_copy.make_move(move)
            score = minimax(game_copy, depth - 1, alpha, beta, True)
            best_score = min(best_score, score)
            beta = min(beta, best_score)
            if alpha >= beta:
                break
        return best_score


def evaluate(game) -> int:
    return game.player.score - game.opponent.score

def is_over(game) -> bool:
    return game.check_total_score() == 56




