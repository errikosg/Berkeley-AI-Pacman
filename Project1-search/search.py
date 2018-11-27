# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    
	#implementing graph search with explored set (from lecture slides), with stack as the data structure
    frontier = util.Stack()
    explored_set = []
    frontier.push((problem.getStartState(), [], 0))             #here the cost is 0 because dfs is a blind algorithm

    while not frontier.isEmpty():
        current = frontier.pop()
        if problem.isGoalState(current[0]):
            return current[1]
        if current[0] not in explored_set:                      #expanding successors
            explored_set.append(current[0])
            for successor in problem.getSuccessors(current[0]):
                if successor[0] not in explored_set:
                    new_path = current[1]+[successor[1]]        #new_path = total path path from beginning till current state
                    #if problem.isGoalState(successor[0]):      #doing isGoalState check here instead of where is written results in the expansion of less ->
                        #return new_path						#-> nodes, but autograder doesn't recognise solution (old version).
                    frontier.push((successor[0], new_path, 0))
    if frontier.isEmpty():
        return []                                                   #returns "error" if frontier is empty

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    
	#same implementation as before, data structure = queue for bfs.

    frontier = util.Queue()
    explored_set = []
    frontier.push((problem.getStartState(), [], 0))

    while not frontier.isEmpty():
        current = frontier.pop()
        if problem.isGoalState(current[0]):
            return current[1]
        if current[0] not in explored_set:
            explored_set.append(current[0])
            for successor in problem.getSuccessors(current[0]):
                if successor[0] not in explored_set:
                    new_path = current[1]+[successor[1]]
                    #if problem.isGoalState(successor[0]):
                        #return new_path
                    frontier.push((successor[0], new_path, 0))
    if frontier.isEmpty():
        return []

def uniformCostSearch(problem):
    """Search the node of least total cost first."""

	#ucs algorithm follows the same pattern but is implemented with a priority queue. Here, we are actually interested in the cost of the step in every move.
	#Therefore, cost=problem.getCostOfAction(...). Finally, we call frontier.update() instead of frontier.push!

    frontier = util.PriorityQueue()
    explored_set = []
    frontier.push((problem.getStartState(), []), 0)

    while not frontier.isEmpty():
        current = frontier.pop()               
        if problem.isGoalState(current[0]):
            return current[1]
        if current[0] not in explored_set:
            explored_set.append(current[0])
            for successor in problem.getSuccessors(current[0]):
                if successor[0] not in explored_set:
                    new_path = current[1]+[successor[1]]
                    #if problem.isGoalState(successor[0]):
                        #return new_path
                    frontier.update((successor[0], new_path), problem.getCostOfActions(new_path))   #where item=(successor_state, path), priority=path_cost
    if frontier.isEmpty():
        return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    
	#A* algorithm is similar to ucs, with the only difference being not calculating the cost of action the same.
	#Here, cost = problem.getCostOfActions(...) + heuristic(...)

    frontier = util.PriorityQueue()
    explored_set = []
    frontier.push((problem.getStartState(), []), 0)

    while not frontier.isEmpty():
        current = frontier.pop()               
        if problem.isGoalState(current[0]):
            return current[1]
        if current[0] not in explored_set:
            explored_set.append(current[0])
            for successor in problem.getSuccessors(current[0]):
                if successor[0] not in explored_set:
                    new_path = current[1]+[successor[1]]
                    #if problem.isGoalState(successor[0]):
                        #return new_path
                    frontier.update((successor[0], new_path), problem.getCostOfActions(new_path) + heuristic(successor[0],problem))
    if frontier.isEmpty():
        return []

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
