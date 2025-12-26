import image_detector
import game
import player
import min_max

grid = image_detector.detect_image("IMG.jpg")
# assumptions:
# if score 56 we can end the game
# player with higher score wins

# current color and opponent color are not available only 4 options

me = player.Player(grid[6][0], {(6,0)})
opponent = player.Player(grid[0][7], {(0,7)})

# turn 0 me go first, 1 opponent goes first
game = game.Game(grid, 0, me, opponent)

game.draw()


while True:
    print('-' * 10)
    if game.turn == 0:
        print('captured', me.captured)
        print("psssstt, best move is ", min_max.get_best_move(game, 10))
    else:
        print('opponent', opponent.captured)
    print("available moves", game.get_available_moves())

    user_input = input("Enter something ")

    if user_input == "q":
        break


    game.make_move(int(user_input))


    print("You entered:", user_input)
    if game.turn == 1:
        print('now captured', me.captured)
        print('my score:', me.score)
    else:
        print('opponent now has', opponent.captured)
        print('opponent score:', opponent.score)
    print('-' * 10)





