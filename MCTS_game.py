import random
import time
import math
from montetreesearch import MonteCarloNode
from util import nextstates
from util import terminalTest

# Main function to run game
def Nim():
    # initial variables
    initialState = []
    state = ()

    print("Let's play Nim")

    # Add try catch to ensure only valid values are accepted
    valid = False;
    while valid==False:
        try:
            # Get piles and sticks
            numPiles = input("How many piles initially? ")
            maxSticks = input("Maximum number of sticks? ")

            # Create initial state
            for i in range(int(numPiles)):
                # Use random numbers to generate random number of sticks
                sticks = random.randint(1,int(maxSticks))
                initialState.append(sticks)

            # set first or second go and create state
            print("The intial state is " + str(initialState))
            print("Do you want to play a) first or b) second")
            turn = input("Enter a or b")
            if(str(turn).lower() ==  "a"):
                state = (initialState,1) #user is always MAX player
                valid = True

            elif(str(turn).lower() == "b"):
                state = (initialState,2) #AI is always MIN player
                valid = True

            else:
                raise ValueError("Invalid Input")
        except ValueError:
            print("invalid input, please re-enter")

    # Return state so we can start game
    return state


# THe user turn, let them choose
def userturn(state):
    # Next states called here (import from your own code)
    succ = nextstates(state)

    # if only an empty state left, pick the stick and return
    if(len(succ)==1 and succ[0][0] ==[1]):    
        print("Only one stick left, and you picked it up")
        return succ[0]
    if(len(succ)==1 and succ[0][0] ==[]):    
        print("You picked up the last stick!")
        return succ[0]
    # Print list of moves
    print("Next move options:")
    for i in range(len(succ)):
        print(str(i) + ".    " + str(succ[i][0]))
    moveIndex = input("Enter next move option number ")
    print("You moved to state " + str(succ[int(moveIndex)][0]))

    # Set new state and return
    state = succ[int(moveIndex)]
    return state



# Given a state, start the game
def game_begin(state):

    game_state = state

    print("game start ", game_state)
    # while no winner, keep alternating
    while game_state[0] != []:

        # You will need to create your own AI function
        if(game_state[1]==1):
             game_state = userturn(game_state)
             #game_state = AI_player_basic(game_state)
        else:
            game_state = AI_player_MCTS(game_state)
        print("state is", game_state)

    # if final state is 1, 2 wins
    if(game_state[1] == 2):
        print("win for player 2")
    else:
        print("You win!")


def AI_player_MCTS(game_state):
    succ = nextstates(game_state)
    if(len(succ)==1 and succ[0][0] ==[1]):    
        print("Only one stick left, and you picked it up")
        return succ[0]
    if(len(succ)==1 and succ[0][0] ==[]):    
        print("You picked up the last stick!")
        return succ[0]
    nodes = []
    for state in succ:
        new_node = MonteCarloNode(state, parent = None)
        nodes.append(new_node)
    for node in nodes:
        node.mcts(10)
    best_node = min(nodes, key=MonteCarloNode.get_avg_val)
    move = best_node.get_state()
    value = succ.index(move)
    state = succ[int(value)]
    return state

    
# Game, get state
init_state = Nim()
game_begin(init_state)