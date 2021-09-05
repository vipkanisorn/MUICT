"""This module contains classes and function to solve a pathfinding problem.

Author:
    - Kanisorn Sa-nguansook
    - 
Student ID:
    - 6288161
    - 
"""

# %%

from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple, List, Callable, Union
from hw1.envutil import render_maze, find_agent

import numpy as np

@dataclass(frozen=True, unsafe_hash=False)
class MazeState:

    # TODO 1: Add other state information here.
    grid: np.ndarray
    # If you need anything more than `grid`, please add here
    

    # TODO 2 Create a list of all possible actions.
    # Please replace it with your own actions
    # Note that an agent can only rotate and move forward.
    actions: Tuple[str] = ('rotate', 'move_forward')

    def __eq__(self, o: object) -> bool:
        if isinstance(o, MazeState):
            return np.all(self.grid == o.grid)
        return False

    def __hash__(self) -> int:
        return render_maze(self.grid).__hash__()

    # TODO 3: Create a transition function
    @classmethod
    def transition(cls, state: MazeState, action: str) -> MazeState:
        """Return a new state after performing `action`.

        If the action is not possible, it should return None.

        The mud disappears as soon as the agent walk onto it.

        Note
        ---------------------
        Keep in mind that you should not modify the previous state
        If you need to clone a numpy's array, you can do so like this:
        >>> y = np.array(x)
        >>> y.flags.writeable = False
        This will create an array y as a copy of array x and then make
        array y immutable (cannot be changed, for safty).
        """
        if(action == 'rotate'):
            y = np.array(state.grid)
            agent_index_y, agent_index_x = find_agent(y)

            if(y[agent_index_x][agent_index_y] == 2):
                y[agent_index_x][agent_index_y] = 3

            elif(y[agent_index_x][agent_index_y] == 3):
                y[agent_index_x][agent_index_y] = 4

            elif(y[agent_index_x][agent_index_y] == 4):
                y[agent_index_x][agent_index_y] = 5
            
            elif(y[agent_index_x][agent_index_y] == 5):
                y[agent_index_x][agent_index_y] = 2

            next_state = MazeState(y)
            return next_state

        
        elif(action == 'move_forward'):
            y = np.array(state.grid)
            agent_index_y, agent_index_x = find_agent(y)
   
            if(
                (y[agent_index_x][agent_index_y] == 2 and y[agent_index_x - 1][agent_index_y] == 1) or 
                (y[agent_index_x][agent_index_y] == 3 and y[agent_index_x][agent_index_y + 1] == 1) or 
                (y[agent_index_x][agent_index_y] == 4 and y[agent_index_x + 1][agent_index_y] == 1) or 
                (y[agent_index_x][agent_index_y] == 5 and y[agent_index_x][agent_index_y - 1] == 1)):
                return None

            else:
                if(y[agent_index_x][agent_index_y] == 2):
                    y[agent_index_x - 1][agent_index_y] = y[agent_index_x][agent_index_y]
                    y[agent_index_x][agent_index_y] = 0

                elif(y[agent_index_x][agent_index_y] == 3):
                    y[agent_index_x][agent_index_y + 1] = y[agent_index_x][agent_index_y]
                    y[agent_index_x][agent_index_y] = 0

                elif(y[agent_index_x][agent_index_y] == 4):
                    y[agent_index_x + 1][agent_index_y] = y[agent_index_x][agent_index_y]
                    y[agent_index_x][agent_index_y] = 0
                
                elif(y[agent_index_x][agent_index_y] == 5):
                    y[agent_index_x][agent_index_y - 1] = y[agent_index_x][agent_index_y]
                    y[agent_index_x][agent_index_y] = 0

                next_state = MazeState(y)
                return next_state

        return None

    # TODO 4: Create a cost function
    @classmethod
    def cost(cls, state: MazeState, action: str) -> float:
        """Return the cost of `action` for a given `state`.

        If the action is not possible, the cost should be infinite.

        Note
        ------------------
        You may come up with your own cost for each action, but keep in mind
        that the cost must be positive and any walking into
        a mod position should cost more than walking into an empty position.
        """
        y = np.array(state.grid)
        agent_index_y, agent_index_x = find_agent(y)
        sum_cost = 0  #total cost
        if (action == 'move_forward'):
            if(
                (y[agent_index_x][agent_index_y] == 2 and y[agent_index_x - 1][agent_index_y] == 7) or 
                (y[agent_index_x][agent_index_y] == 3 and y[agent_index_x][agent_index_y + 1] == 7) or 
                (y[agent_index_x][agent_index_y] == 4 and y[agent_index_x + 1][agent_index_y] == 7) or 
                (y[agent_index_x][agent_index_y] == 5 and y[agent_index_x][agent_index_y - 1] == 7)):
                sum_cost = sum_cost + 2
                print("shit it's a mud !!!!")

            elif(
                (y[agent_index_x][agent_index_y] == 2 and y[agent_index_x - 1][agent_index_y] == 1) or 
                (y[agent_index_x][agent_index_y] == 3 and y[agent_index_x][agent_index_y + 1] == 1) or 
                (y[agent_index_x][agent_index_y] == 4 and y[agent_index_x + 1][agent_index_y] == 1) or 
                (y[agent_index_x][agent_index_y] == 5 and y[agent_index_x][agent_index_y - 1] == 1)):
                print("shit it's a wall !!!!")
                return float('inf')

            else:
                sum_cost = sum_cost + 1
        elif(action == 'rotate'):
                sum_cost = sum_cost + 1
        
        return float(sum_cost)

    # TODO 5: Create a goal test function
    @classmethod
    def is_goal(cls, state: MazeState) -> bool:
        """Return True if `state` is the goal."""
        y = np.array(state.grid)
        if(find_agent(y) == (len(y) - 2,len(y) - 2)):
            return True
        return False

    # TODO 6: Create a heuristic function
    @classmethod
    def heuristic(cls, state: MazeState) -> float:
        """Return a heuristic value for the state.

        Note
        ---------------
        You may come up with your own heuristic function.
        """
        #Manhatthan Distance
        y = np.array(state.grid)
        agent_index_y, agent_index_x = find_agent(y)
        hs = abs(agent_index_x - (len(y) -2)) + abs(agent_index_y - (len(y) - 2))
        return hs
# %%

@dataclass
class TreeNode:
    path_cost: float
    state: MazeState
    action: str
    depth: int
    parent: TreeNode = None


def dfs_priority(node: TreeNode) -> float:
    return -1.0 * node.depth


def bfs_priority(node: TreeNode) -> float:
    return 1.0 * node.depth


# TODO: 7 Create a priority function for the greedy search
def greedy_priority(node: TreeNode) -> float:
    open_set = []
    return 0.0


# TODO: 8 Create a priority function for the A* search
def a_star_priority(node: TreeNode) -> float:
    return 0.0


# TODO: 9 Implement the graph search algorithm.
def graph_search(
        init_state: MazeState,
        priority_func: Callable[[TreeNode], float]) -> Tuple[List[str], float]:
    """Perform graph search on the initial state and return a list of actions.

    If the solution cannot be found, return None and infinite cost.
    """
    return None, float('inf')
