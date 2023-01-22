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
SERVER_PIECE = -1
WINDOW_LENGTH = 4
DEPTH = 5



element_values = np.reshape([
    3, 4,  5,  7,  5, 4, 3,
    4, 6,  8, 10,  8, 6, 4,
    5, 8, 11, 13, 11, 8, 5,
    5, 8, 11, 13, 11, 8, 5,
    4, 6,  8, 10,  8, 6, 4,
    3, 4,  5,  7,  5, 4, 3,
], (6, 7))


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
    # initialize row and column for augmentation of which where to best place a piece
    row = 0
    column = 0
    best_move = 0
    best_move, score = minimax(
        board, DEPTH, -math.inf, math.inf, row, column, 1, student_starts)
    if best_move == None:
        print('No more moves')
    else:
        print('Best move is row: ' + str(best_move + 1) + '   With the score: {}'.format(score))

    return best_move


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



def is_terminal_node(board):
    return env.is_win_state() or winning_move(board, PLAYER_PIECE) or winning_move(board, SERVER_PIECE) 


def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r-1][c] == piece and board[r-2][c] == piece and board[r-3][c] == piece:
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

def check_win(state, row, col):
    state = state.copy()
    sym = state[row, col]
    # up/down, left/right, diag ru/ld, diag lu/rd
    count = [1, 1, 1, 1]
    vectors = [
        [(-1, 0), (1, 0)],
        [(0, -1), (0, 1)],
        [(-1, 1), (1, -1)],
        [(-1, -1), (1, 1)]
    ]
    for k in range(4):
        for dr, dc in vectors[k]:
            for i in range(1, 4):
                r = i * dr + row
                c = i * dc + col
                if r < 0 or r > 5:
                    break
                if c < 0 or c > 6:
                    break
                if sym == state[r, c]:
                    count[k] += 1
                else:
                    break
    for j in count:
        if j >= 4:
            return sym

def heuristic(board):
    return np.sum(board * element_values)


def evaluate(board, row, col):
    return heuristic(board)


def minimax(board, depth, a, b, row, column, piece, maximizingPlayer):

    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)  
    result = check_win(board, row, column)
    if depth == 0 or result == piece or result == -piece:
        if winning_move(board, PLAYER_PIECE):
            return (None, 999999999)
        elif winning_move(board, SERVER_PIECE):
            return (None, -999999999)
        elif result == 0:                
            return(column, 0)
        elif depth == 0:  # Depth is zero
            return (None, evaluate(board, row, column))

    if maximizingPlayer:
        value = -math.inf
        for col in valid_locations:
            row = get_next_open_row(board, col)
            board_copy = drop_piece(board, row, col, piece)
            new_score = minimax(board_copy, depth-1, a, b, row, col, -piece, False)[1]
            new_score = max(value, new_score)
            if new_score > value:
                value = new_score
                column = col
            a = max(a, value)
            if a >= b:
                break
        return column, value

    else:  # Minimizing player
        value = math.inf
        for col in valid_locations:
            row = get_next_open_row(board, col)
            board_copy = drop_piece(board, row, col, piece)
            new_score = minimax(board_copy, depth-1, a, b, row, col, -piece, True)[1]
            new_score = min(value, new_score)
            if new_score < value:
                value = new_score
                column = col
            b = min(b, value)
            if a >= b:
                break
        return column, value


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
