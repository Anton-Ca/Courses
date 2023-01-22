import gym
import random
import requests
import numpy as np
import math
from gym_connect_four import ConnectFourEnv

env: ConnectFourEnv = gym.make("ConnectFour-v0")

# SERVER_ADRESS = "http://localhost:8000/"
SERVER_ADRESS = "https://vilde.cs.lth.se/edap01-4inarow/"
API_KEY = 'nyckel'
STIL_ID = ["bas15aca"]

# Initialized variables
ROW_COUNT = 6
COLUMN_COUNT = 7
PLAYER = 0
AI = 1
EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = -1
WINDOW_LENGTH = 4
DEPTH = 5


def call_server(move):
    res = requests.post(SERVER_ADRESS + "move",
                        data={
                            "stil_id": STIL_ID,
                            "move": move,  # -1 signals the system to start a new game. any running game is counted as a loss
                            "api_key": API_KEY,
                        })
    # For safety some respose checking is done here
    if res.status_code != 200:
        print("Server gave a bad response, error code={}".format(res.status_code))
        exit()
    if not res.json()['status']:
        print("Server returned a bad status. Return message: ")
        print(res.json()['msg'])
        exit()
    return res


def drop_piece(board, row, col, piece):
    board = board.copy()
    board[row][col] = piece
    return board


def is_valid_location(board, col):
    return board[0][col] == 0


def get_next_open_row(board, col):
    for row in range(ROW_COUNT):
        r = ROW_COUNT - row - 1
        if board[r][col] == 0:
            return r


def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


"""
You can make your code work against this simple random agent
before playing against the server.
It returns a move 0-6 or -1 if it could not make a move.
To check your code for better performance, change this code to
use your own algorithm for selecting actions too
"""


def opponents_move(env):
    env.change_player()  # change to oppoent
    avmoves = env.available_moves()

    if not avmoves:
        env.change_player()  # change back to student before returning
        return -1

    # TODO: Optional? change this to select actions with your policy too
    # that way you get way more interesting games, and you can see if starting
    # is enough to guarrantee a win
    action = random.choice(list(avmoves))

    state, reward, done, _ = env.step(action)
    if done:
        if reward == 1:  # reward is always in current players view
            reward = -1
    env.change_player()  # change back to student before returning
    return state, reward, done


'''

    valid_move = env.available_moves()
    best_move = random.choice(valid_move)
    best_score = -math.inf
    for col in valid_move:
         
'''


def student_move(board, student_starts):
    #best_move = random.choice([0, 1, 2, 3, 4, 5, 6])

    # initialize column for augmentation of which column corresponds to the best score
    column = 0  # random.choice(get_valid_locations(board))
    best_move = 0
    best_move, score = minimax(
        board, DEPTH, -math.inf, math.inf, column, -1, student_starts)
    if best_move == None:
        print('No more moves')
    else:
        print('Best move is: ' + str(best_move + 1))

    return best_move


def is_terminal_node(board):
    return env.is_win_state() or len(get_valid_locations(board)) == 0


def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True


def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE

    if window.count(piece) == 4:
        score += 999
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 6
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 3

    if window.count(opp_piece) == 4:
        score += 99
    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(opp_piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    return score


def quick_score(sum_pieces, piece):
    score = 0

    if sum_pieces == 2 * piece:
        score += 2 * piece
    if sum_pieces == 3 * piece:
        score += 5 * piece 
    return score

def score_position(piece, board):
    score = 0
    for r in range(ROW_COUNT - 1):
        for c in range(COLUMN_COUNT - 1):

            if c < COLUMN_COUNT - 3:
                # Horizontal 
                row = []
                sum_row = 0
                for n in range(4):
                    if board[r][c+n] != -piece:
                        row.append(board[r][c+n])
                        sum_row = sum(row)
                        score += quick_score(sum_row, piece)

                if r < ROW_COUNT - 3:
                    # Diagonal right
                    row = []
                    for n in range(4):
                        if board[r+n][r+n] != -piece:
                            row.append(board[r+n][c+n])
                            sum_row = sum(row)
                            score += quick_score(sum_row, piece)

            if c >= 3:
                # Horizontal left
                row = []
                for n in range(4):
                    if board[r][c-n] != -piece:
                        row.append(board[r][c-n])
                        sum_row = sum(row)
                        score += quick_score(sum_row, piece)
                        
                if r < ROW_COUNT - 3:
                    # Diagonal left
                    row = []
                    for n in range(4):
                        if board[r+n][r-n] != -piece:
                            row.append(board[r][c-n])
                            sum_row = sum(row)
                            score += quick_score(sum_row, piece)
                

            if c < ROW_COUNT - 3:
                # vertical 
                row = []
                for n in range(4):
                    if board[r-n][c] != -piece:
                        row.append(board[r-n][c])
                        sum_row = sum(row)
    return score

'''
def score_position(piece, board):
    score = 0

    # Score center column
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 4  # * piece

    # Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT-3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_window(window, piece)  # * piece

    # Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)  # * piece

    # Score  positive sloped diagonal
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r-3+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)  # * piece

    # Score negative sloped diagonal
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)  # * piece

    return score
'''

def minimax(board, depth, a, b, column, piece, maximizingPlayer):
    # For alternation of placing down a piece
    piece *= -1  # is positive our first turn
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)  # Översätt här
    if depth == 0 or is_terminal:
        if is_terminal:
            if env.is_win_state() and winning_move(board, PLAYER_PIECE):
                return (column, 9999)
            elif env.is_win_state() and winning_move(board, AI_PIECE):
                return (column, -9999)
            else:
                return(column, 0)
        else:  # Depth is zero
            return (column, score_position(PLAYER_PIECE, board))

    if maximizingPlayer:
        value = -math.inf
        for col in valid_locations:
            row = get_next_open_row(board, col)
            board_copy = drop_piece(board, row, col, piece)
            c, new_score = minimax(board_copy, depth-1,
                                   a, b, col, piece, False)
            new_score = max(value, new_score)
            if new_score > value:
                value = new_score
                column = c
            a = max(a, new_score)
            if a >= b:
                break
        return column, new_score

    else:  # Minimizing player
        value = math.inf
        for col in valid_locations:
            row = get_next_open_row(board, col)
            board_copy = drop_piece(board, row, col, piece)
            c, new_score = minimax(board_copy, depth-1, a, b, col, piece, True)
            new_score = min(value, new_score)
            if new_score < value:
                value = new_score
                column = c
            b = min(b, new_score)
            if a >= b:
                break
        return column, new_score


def play_game(vs_server=True):
    """
    The reward for a game is as follows. You get a
    botaction = random.choice(list(avmoves)) reward from the
    server after each move, but it is 0 while the game is running
    loss = -1
    win = +1
    draw = +0.5
    error = -10 (you get this if you try to play in a full column)
    Currently the player always makes the first move
    """

    # default state
    state = np.zeros((6, 7), dtype=int)

    # setup new game
    if vs_server:
        # Start a new game
        # -1 signals the system to start a new game. any running game is counted as a loss
        res = call_server(-1)

        # This should tell you if you or the bot starts
        print(res.json()['msg'])
        botmove = res.json()['botmove']
        state = np.array(res.json()['state'])
        if botmove == -1:
            student_starts = True
        else:
            student_starts = False
    else:
        # reset game to starting state
        env.reset(board=None)
        # determine first player
        student_gets_move = random.choice([True, False])
        student_starts = student_gets_move
        if student_gets_move:
            print('You start!')
            print()
        else:
            print('Bot starts!')
            print()

    # Print current gamestate
    print("Current state (1 are student discs, -1 are servers, 0 is empty): ")
    print(state)
    print()

    done = False
    while not done:
        # Select your move
        stmove = student_move(state, student_starts)  # TODO: change input here

        # if env.is_win_state():
        # env.StepResult.get_reward(PLAYER)
        # make both student and bot/server moves
        if vs_server:
            # Send your move to server and get response
            res = call_server(stmove)
            print(res.json()['msg'])

            # Extract response values
            result = res.json()['result']
            botmove = res.json()['botmove']
            state = np.array(res.json()['state'])
            print('New state: \n')
        else:
            if student_gets_move:
                # Execute your move
                avmoves = env.available_moves()
                if stmove not in avmoves:
                    print("You tried to make an illegal move! Game ends.")
                    break
                state, result, done, _ = env.step(stmove)

            student_gets_move = True  # student only skips move first turn if bot starts

            # print or render state here if you like

            # select and make a move for the opponent, returned reward from students view
            if not done:
                state, result, done = opponents_move(env)

        # Check if the game is over
        if result != 0:
            done = True
            if not vs_server:
                print("Game over. ", end="")
            if result == 1:
                print("You won!")
            elif result == 0.5:
                print("It's a draw!")
            elif result == -1:
                print("You lost!")
            elif result == -10:
                print("You made an illegal move and have lost!")
            else:
                print("Unexpected result result={}".format(result))
            if not vs_server:
                print("Final state (1 are student discs, -1 are servers, 0 is empty): ")
        else:
            # print("Current state (1 are student discs, -1 are servers, 0 is empty): ")
            pass

        # Print current gamestate
        print(state)
        print()
    return result


def main():
    nbr_of_games = 1
    result = 0.0
    for round in range(nbr_of_games):
        result += play_game(vs_server=True)
    print('Result: {}'.format(result))
    # TODO: Change vs_server to True when you are ready to play against the server
    # the results of your games there will be logged


if __name__ == "__main__":
    main()
