import pygame
import sys
import image_detector
import game
import player
import min_max

COLOR_PROTOTYPES = {
    1: (60, 60, 60),  # black
    2: (250, 220, 70),  # yellow
    3: (175, 215, 95),  # green
    4: (90, 165, 235),  # blue
    5: (130, 100, 170),  # purple
    6: (235, 80, 95),  # red
}

GRID_COLOR = (40, 40, 45)
BG_COLOR = (25, 25, 30)
TEXT_COLOR = (220, 220, 220)
HIGHLIGHT_COLOR = (255, 255, 100)


grid = image_detector.detect_image("IMG.jpg")
me = player.Player(grid[6][0], {(6, 0)})
opponent = player.Player(grid[0][7], {(0, 7)})
game_instance = game.Game(grid, 0, me, opponent)


pygame.init()
cell_size = 70
width = game_instance.cols * cell_size + 350
height = game_instance.rows * cell_size + 120
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Filler Solver")
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 28)
clock = pygame.time.Clock()

best_move_printed = False

def draw_game():
    screen.fill(BG_COLOR)

    title = font.render("FILLER", True, TEXT_COLOR)
    screen.blit(title, (20, 20))

    grid_start_y = 80
    for row in range(game_instance.rows):
        for col in range(game_instance.cols):
            x = col * cell_size + 20
            y = row * cell_size + grid_start_y

            pos = (row, col)


            if pos in me.captured:
                cell_color = COLOR_PROTOTYPES.get(me.color, (255, 255, 255))
            elif pos in opponent.captured:
                cell_color = COLOR_PROTOTYPES.get(opponent.color, (255, 255, 255))
            else:
                color_value = game_instance.grid[row][col]
                cell_color = COLOR_PROTOTYPES.get(color_value, (100, 100, 100))

            pygame.draw.rect(screen, cell_color, (x + 2, y + 2, cell_size - 4, cell_size - 4), border_radius=8)

    ui_x = game_instance.cols * cell_size + 60
    ui_start_y = 100

    turn_text = "YOUR TURN" if game_instance.turn == 0 else "OPPONENT"
    turn_color = (100, 200, 100) if game_instance.turn == 0 else (200, 100, 100)
    turn_surface = font.render(turn_text, True, turn_color)
    screen.blit(turn_surface, (ui_x, ui_start_y))

    y_offset = ui_start_y + 60
    screen.blit(small_font.render("YOU", True, TEXT_COLOR), (ui_x, y_offset))
    pygame.draw.rect(screen, COLOR_PROTOTYPES.get(me.color, (255, 255, 255)),
                     (ui_x + 80, y_offset - 5, 40, 40), border_radius=6)
    score_text = small_font.render(f"Score: {me.score}", True, TEXT_COLOR)
    screen.blit(score_text, (ui_x + 130, y_offset + 5))

    y_offset += 70
    screen.blit(small_font.render("OPP", True, TEXT_COLOR), (ui_x, y_offset))
    pygame.draw.rect(screen, COLOR_PROTOTYPES.get(opponent.color, (255, 255, 255)),
                     (ui_x + 80, y_offset - 5, 40, 40), border_radius=6)
    score_text = small_font.render(f"Score: {opponent.score}", True, TEXT_COLOR)
    screen.blit(score_text, (ui_x + 130, y_offset + 5))

    y_offset += 90
    screen.blit(small_font.render("MOVES:", True, TEXT_COLOR), (ui_x, y_offset))

    available_moves = game_instance.get_available_moves()
    y_offset += 40
    for i, move in enumerate(available_moves):
        move_y = y_offset + i * 55

        pygame.draw.rect(screen, COLOR_PROTOTYPES[move],
                         (ui_x, move_y, 50, 50), border_radius=8)
        pygame.draw.rect(screen, TEXT_COLOR,
                         (ui_x, move_y, 50, 50), 2, border_radius=8)

        num_surface = font.render(str(move), True, TEXT_COLOR)
        screen.blit(num_surface, (ui_x + 65, move_y + 10))

    pygame.display.flip()


running = True
game_over = False

while running:
    draw_game()

    if game_instance.turn == 0 and not game_over and not best_move_printed:
        best_move = min_max.get_best_move(game_instance, 10)
        print(f"Best move: {best_move}")
        best_move_printed = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False

            elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6]:
                if not game_over:
                    move = event.key - pygame.K_0

                    if move in game_instance.get_available_moves():
                        game_instance.make_move(move)
                        best_move_printed = False

                        total_score = game_instance.check_total_score()
                        if total_score >= 56:
                            game_over = True
                            print("\n" + "=" * 30)
                            print("GAME OVER!")
                            print("=" * 30)
                            if me.score > opponent.score:
                                print(f"YOU WIN! ({me.score} vs {opponent.score})")
                            elif opponent.score > me.score:
                                print(f"OPPONENT WINS! ({opponent.score} vs {me.score})")
                            else:
                                print(f"TIE GAME! ({me.score} vs {opponent.score})")
                            print("=" * 30 + "\n")

    clock.tick(60)

pygame.quit()
sys.exit()