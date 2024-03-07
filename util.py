
def nextstates(state):
    ##state is a tuple like ([3,2],1)
    piles, player = state
    #we need to make it the opposite players turn
    player = 3 - player
    next_states= []
    for i in range(len(piles)):
        current = piles[i]
        for j in range(1, 4):
            if j < current:
                new_state = piles[:i] + [current - j] + piles[i+1:]
                new_state = sorted(new_state)
                if (new_state,player) not in next_states:
                    next_states.append((new_state,player))
            elif j == current:
                new_state = piles[:i] + piles[i+1:]
                new_state = sorted(new_state)
                if (new_state,player) not in next_states:
                    next_states.append((new_state,player))

    return next_states

def terminalTest(state):
    ##checks to see if we are in a terminal state, have just combined the utility function here as it's simple
    if state == ([], 1):
        return 1
    if state == ([], 2):
        return -1
    else:
        return 0