from math import sqrt
from math import log
from collections import deque
import random
from util import nextstates
from util import terminalTest

class MonteCarloNode():
    def __init__(self,state,parent = None):
        self.state = state
        self.parent = parent
        self.num_visits = 0
        self.avg_val = 0
        self.value = 0
        self.ucb1_dict = {}
        self.children = []
        

    def get_avg_val(self):
        self.avg_val = self.value/self.num_visits
        return self.avg_val
    
    def get_parent(self):
        return self.parent
    
    def get_visits(self):
        return self.num_visits
    
    def get_state(self):
        return self.state
    

    def pick_best_node(self):
        queue = deque([self])
        best_val = -100
        best_child = None
        visited = set()
        while queue:
            current_node = queue.popleft()
            if current_node in visited:
                continue
            visited.add(current_node)
            curr_val = self.ucb1_dict.get(current_node,UCB1(current_node))
            if curr_val > best_val:
                best_val = curr_val
                best_child = current_node
            queue.extend(current_node.children)
      
        return best_child
        
    
    def rollout(self, num_rollouts = 10):
        total_utility = 0
        for _ in range(num_rollouts):
            curr_state = self.state
            while(terminalTest(curr_state) == 0):
                sucessors = nextstates(curr_state)
                if not sucessors:
                    break
                curr_state = random.choice(sucessors)
            total_utility += terminalTest(curr_state)
        average_utility = total_utility / num_rollouts
        return average_utility
    
    def expand(self):
        if self.num_visits > 0:
            new_nodes = []
            for c_state in nextstates(self.state):
                new_node = MonteCarloNode(c_state, parent=self)
                self.children.append(new_node)
                new_nodes.append(new_node)
            if new_nodes:
                return new_nodes
            else:
                return [self]
        else:
            return [self]

            
    def backpropagate(self, terminal_result):
          self.num_visits += 1
          self.value += terminal_result
          if self.parent:
              self.parent.backpropagate(terminal_result)

    def mcts(self, num_iterations = 10):
        for _ in range (num_iterations):
            curr_node = self.pick_best_node()
            if curr_node.get_visits() >0:
                expanded_node = curr_node.expand()
                result = expanded_node[0].rollout()
                expanded_node[0].backpropagate(result)
            else:
                result = curr_node.rollout()
                curr_node.backpropagate(result)

        


def UCB1(node):

    if node.get_visits() == 0:
        return 1000
    
    avg_val = node.get_avg_val()
    if node.get_parent() == None:
        return 0
    parent_visits = node.get_parent().get_visits()
    num_visits = node.get_visits()
    
    UCB1_val = avg_val + 2 * sqrt(log(parent_visits)/num_visits)
    return UCB1_val

