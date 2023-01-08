import sys, pygame, game_board, graphics, time, alphago, CNN_player, output
import numpy as np

WHITE = (255,255,255)
GOLD = (255,225,0)

SIZE = (620, 620)

pygame.init()
screen = pygame.display.set_mode(SIZE)

white_win_image = pygame.image.load("white_win_image.png")
black_win_image = pygame.image.load("black_win_image.png")
tie_image = pygame.image.load("tie_image.png")
icon = pygame.image.load("icon.png")

pygame.display.set_caption("Gomoku")
pygame.display.set_icon(icon)

graph = graphics.Graphics()
alphago = alphago.AlphaGo()
CNN_model_1 = CNN_player.CNNPlayer('model3.h5')
CNN_model_2 = CNN_player.CNNPlayer('model_2.0.h5')
game_counter = 0

p1_wins = 0
p2_wins = 0

while True:
    print(f"Games played: {game_counter}, p1 wins: {100 * p1_wins / (max(1, game_counter))}%, p2 wins: {100 * p2_wins / (max(1, game_counter))}%")
    game_counter += 1
    screen.fill(WHITE)
    pygame.display.update()
    
    start_game = True
    dim = 15
    gametype = 1

    while not start_game:
        screen.fill(GOLD)
        graph.draw_menu(screen, dim, gametype)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                start_game, dim, gametype = graph.menu_click(event.pos, dim, gametype)
        pygame.display.update()

    screen.fill(WHITE)
    board = game_board.GameBoard(dim, dim)
    graph.draw_grid(screen, board)
    pygame.display.update()

    game_board_states = np.zeros((225, 15, 15))
    moves = np.zeros((2, 225))
    players = np.zeros(225)

    winner = 0
    player = 1
    move_coords = None

    p2 = CNN_model_1
    p1 = alphago

    turn_counter = 0

    while winner == 0:

        game_board_states[turn_counter] = np.array(board.get_board())
        players[turn_counter] = player
        if gametype == player:
            move_coords = p1.move(board.get_board(), player)
            moves[0, turn_counter], moves[1, turn_counter] = move_coords
            move = board.move(move_coords, player)
            if move:
                player *= -1
            winner = board.check_winner()
            graph.draw_pieces(screen, board)
            pygame.display.update()

            turn_counter += 1

        if winner != 0:
            if winner == 1:
                p1_wins += 1
            if winner == -1:
                p2_wins += 1
            break

        screen.fill(WHITE)
        graph.draw_grid(screen, board)

        game_board_states[turn_counter] = np.array(board.get_board())
        players[turn_counter] = player

        if gametype != 0:
            graph.highlight_last_move(screen, move_coords)

        if gametype * -1 == player:
            move_coords = p2.move(board.get_board(), player)
            moves[0, turn_counter], moves[1, turn_counter] = move_coords
            move = board.move(move_coords, player)
            if move:
                player *= -1
            winner = board.check_winner()
            graph.draw_pieces(screen, board)
            pygame.display.update()

            turn_counter += 1

        if winner != 0:
            if winner == 1:
                p1_wins += 1
            if winner == -1:
                p2_wins += 1
            break

        #graph.hover_square(screen, board, player)
        graph.draw_pieces(screen, board)
        pygame.display.update()

    output.output_file(game_board_states, moves, players, winner, turn_counter)

    if winner != 2:
        graph.highlight_winner(screen, board.get_winning_line(move_coords))
        pygame.display.update()

    if winner == -1:
        screen.blit(black_win_image,(0,0))
    elif winner == 1:
        screen.blit(white_win_image,(0,0))
    else:
        screen.blit(tie_image, (0,0))

    pygame.display.update()

    new_game = True

    while not new_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == 32:
                    new_game = True
