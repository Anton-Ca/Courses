import gym
import random
import requests
import numpy as np
from gym_connect_four import ConnectFourEnv

env: ConnectFourEnv = gym.make("ConnectFour-v0")

#SERVER_ADRESS = "http://localhost:8000/"
SERVER_ADRESS = "https://vilde.cs.lth.se/edap01-4inarow/"
API_KEY = 'nyckel'
STIL_ID = ["mas14doh"] # TODO: fill this list with your stil-id's

test_board_1 = np.reshape([
    0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 1, 0, 0, 0,
    0, 0, -1, 1, 0, 0, 0,
    0, -1, -1, 1, -1, 0, 0,
], (6, 7))

test_board_2 = np.reshape([
    -1,  0, -1, -1,  0,  0, -1,
    -1, -1,  1,  1,  1,  0, -1,
    -1,  1,  1, -1,  1,  0,  1,
     1, -1,  1, -1, -1, -1,  1,
    -1, -1, -1,  1, -1,  1, -1,
    -1,  1, -1,  1, -1,  1, -1,
], (6, 7))

test_board_3 = np.reshape([
     0,  0,  0,  0,  0,  0,  0,
    -1,  1, -1,  1, -1,  1, -1,
     1, -1,  1, -1,  1,  1, -1,
     1, -1,  1, -1,  1, -1, -1,
    -1,  1, -1,  1, -1,  1,  1,
    -1,  1, -1,  1, -1,  1, -1,
], (6, 7))

test_board_4 = np.array([
    [ 1,  0,  0,  0,  0,  0,  0],
    [ 1,  0,  0,  0,  0,  0,  0],
    [-1,  0,  0, -1,  0,  0,  0],
    [ 1,  0,  1, -1,  0,  0, -1],
    [ 1,  0, -1,  1,  0,  0, -1],
    [ 1,  0, -1,  1,  0,  0, -1]]
)

def call_server(move):
   res = requests.post(SERVER_ADRESS + "move",
                       data={
                           "stil_id": STIL_ID,
                           "move": move, # -1 signals the system to start a new game. any running game is counted as a loss
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
   env.change_player() # change to oppoent
   avmoves = env.available_moves()
   if not avmoves:
      env.change_player() # change back to student before returning
      return -1

   # TODO: Optional? change this to select actions with your policy too
   # that way you get way more interesting games, and you can see if starting
   # is enough to guarrantee a win
   action = random.choice(list(avmoves))

   state, reward, done, _ = env.step(action)
   if done:
      if reward == 1: # reward is always in current players view
         reward = -1
   env.change_player() # change back to student before returning
   return state, reward, done

def move_is_valid(state, col):
    return state[0, col] == 0
    
def check_win(state, row, col):
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

place_values = np.reshape([
    3, 4,  5,  7,  5, 4, 3,
    4, 6,  8, 10,  8, 6, 4,
    5, 8, 11, 13, 11, 8, 5,
    5, 8, 11, 13, 11, 8, 5,
    4, 6,  8, 10,  8, 6, 4,
    3, 4,  5,  7,  5, 4, 3,
], (6, 7))

def heuristic_2(state):
    return np.sum(state * place_values)

def evaluate(state, row, col):    
    return heuristic_2(state)


    
def make_move(state, col, whom):
    for i in range(5, -1, -1):
        if state[i, col] == 0:
            state_copy = np.copy(state)
            state_copy[i, col] = whom
            return state_copy, i

indent = 0
def p(s):
    return
    print('%s%d. %s' % (indent * '    ', indent, s))
    
INF = 1000000    

def search(state, whom, col, alpha, beta, depth):
    global indent
    # I try to play the move given, can I? Do I win? Is it a draw?
    
    if not move_is_valid(state, col):
        return None
    p('Consider col=%d by player=%d (alpha=%d, beta=%d)' % (col, whom, alpha, beta))
    #for row in state: p(repr(row))
    new_state, row = make_move(state, col, whom)
    result = check_win(new_state, row, col)

    if result == whom:
        p('Win for player=%d' % whom)
        return whom * INF   
    elif is_draw(new_state):
        p('Draw')
        return 0
        
        
    # No win or draw, turn passes to other player. What can he do?
    if depth > 3:
        result = evaluate(state, row, col)
        p('Max depth')
        return result
    
    value = INF if whom == 1 else -INF
    
    for i in range(0, 7):
        indent += 1
        score = search(new_state, -whom, i, alpha, beta, depth + 1)
        indent -= 1

        if score is None:
            continue
            
        if whom == 1: # min
            value = min(value, score)
            beta = min(beta, value)
            if beta <= alpha:
                p('Beta-prune col=%d score=%g for player %d' % (col, score, whom))
                break
        else: # max
            value = max(value, score)
            alpha = max(alpha, value)
            if alpha >= beta:
                p('Alpha-prune col=%d score=%g for player %d' % (col, score, whom))
                break

    p('Result col=%d score=%g for player %d' % (col, value, whom))
    return value
        
def is_draw(state):
    for i in range(0, 7):
        if state[0, i] == 0:
            return False
    return True
        
  
def student_move(state): 
    """
    TODO: Implement your min-max alpha-beta pruning algorithm here.
    Give it whatever input arguments you think are necessary
    (and change where it is called).
    The function should return a move from 0-6
    """
    
    best_i = -1
    best_score = -INF
    for i in range(0, 7):      
        score = search(state, 1, i, -INF, INF, 0)
        if score is not None and score > best_score:
            best_score = score
            best_i = i
    return best_i
    

def play_game(vs_server = False):
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
      res = call_server(-1) # -1 signals the system to start a new game. any running game is counted as a loss

      # This should tell you if you or the bot starts
      print(res.json()['msg'])
      botmove = res.json()['botmove']
      state = np.array(res.json()['state'])
   else:
      # reset game to starting state
      env.reset(board=None)
      # determine first player
      student_gets_move = random.choice([True, False])
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
      stmove = student_move(state) # TODO: change input here

      # make both student and bot/server moves
      if vs_server:
         # Send your move to server and get response
         res = call_server(stmove)
         print(res.json()['msg'])

         # Extract response values
         result = res.json()['result']
         botmove = res.json()['botmove']
         state = np.array(res.json()['state'])
      else:
         if student_gets_move:
            # Execute your move
            avmoves = env.available_moves()
            if stmove not in avmoves:
               print("You tied to make an illegal move! Games ends.")
               break
            state, result, done, _ = env.step(stmove)

         student_gets_move = True # student only skips move first turn if bot starts

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
         print("Current state (1 are student discs, -1 are servers, 0 is empty): ")

      # Print current gamestate
      print(state)
      print()

def main():
   play_game(vs_server = False)
   # TODO: Change vs_server to True when you are ready to play against the server
   # the results of your games there will be logged

if __name__ == "__main__":
    main()
