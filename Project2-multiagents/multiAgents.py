# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        actions = currentGameState.getLegalActions(0)


        #simple reflex agent that usually follows food using getFoodScore ->
        #but when ghost comes too close (radius=3) it tries to avoid

        currentScore = successorGameState.getScore()
        lowValue = -1000000.0
        radius = 3

        def getGhostScore(newGhostStates, newPos, radius):
            for ghost in newGhostStates:
                gpos = ghost.getPosition()
                distance = manhattanDistance(newPos, gpos)
                if distance != 0 and distance < radius:
                    return lowValue                                 #lowValue is declared outside
            return 0

        def getFoodScore(newFood, newPos):
            foodList = newFood.asList()
            score=0
            for food in foodList:
                distance = manhattanDistance(newPos, food)
                score += (1/float(distance))                        #float is wanted here as specified by exercise!
            return score

        ret = currentScore + getFoodScore(newFood, newPos) + getGhostScore(newGhostStates, newPos, radius)
        #print ret
        return ret

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """

        #function that checks if we are in terminal state - the actual value of the leaf must be returned.
        def terminalTest(gameState, depth, actions):
            if gameState.isWin() or gameState.isLose():
                return True
            elif len(actions)==0 or depth == self.depth:
                return True
            return False

        #functions that manages the many layers of ghost-agents.
        def fixCall(currState, newState, depth, agent):
            numAgents = currState.getNumAgents()
            if agent + 1 == numAgents:
                return maxValue(newState, depth+1, 0)
            else:
                return minValue(newState, depth, agent+1)


        def maxValue(currState, depth, agent):
            actions = currState.getLegalActions(agent)                  #pacman is always agent 0
            if terminalTest(currState, depth, actions) == True:         #if TERMINAL-TEST(state), then return UTILITY(state)
                return (self.evaluationFunction(currState), None)

            v = -10000000.0
            vAction = None                                              #successor and action

            for a in actions:
                newState = currState.generateSuccessor(agent, a)
                newValue, temp = minValue(newState, depth, agent+1)
                if newValue > v:
                    v = newValue
                    vAction = a
            return (v, vAction)


        def minValue(currState, depth, agent):
            actions = currState.getLegalActions(agent)                  #ghosts will have linear increment in their ids
            if terminalTest(currState, depth, actions) == True:         #if TERMINAL-TEST(state), then return UTILITY(state)
                return (self.evaluationFunction(currState), None)

            v = 10000000.0
            vAction = None

            for a in actions:
                newState = currState.generateSuccessor(agent, a)
                newValue, temp = fixCall(currState, newState, depth, agent)     #fixCall: manages the multiple "layers" of ghosts / explained in README
                if newValue < v:
                    v = newValue
                    vAction = a
            return (v, vAction)

        v, action = maxValue(gameState, 0, 0)
        return action
        

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """

        #similar algorithm to minimax, but we have the a-b values that can stop the process earlier
        #thus resulting to quicker responses (from pseudocode of lectures).

        def terminalTest(gameState, depth, actions):
            if gameState.isWin() or gameState.isLose():
                return True
            elif len(actions)==0 or depth == self.depth:
                return True
            return False

        def fixCall(currState, newState, depth, agent, a, b):
            numAgents = currState.getNumAgents()
            if agent + 1 == numAgents:
                return maxValue(newState, depth+1, 0, a, b)
            else:
                return minValue(newState, depth, agent+1, a, b)


        def maxValue(currState, depth, agent, a, b):
            actions = currState.getLegalActions(agent)                  #pacman is always agent 0
            if terminalTest(currState, depth, actions) == True:         #if TERMINAL-TEST(state), then return UTILITY(state)
                return (self.evaluationFunction(currState), None)

            v = -10000000.0
            vAction = None                                              #successor and action

            for action in actions:
                newState = currState.generateSuccessor(agent, action)
                newValue, temp = minValue(newState, depth, 1, a, b)
                if newValue > v:
                    v = newValue
                    vAction = action

                #check and fix alpha
                if v > b:
                    return (v, vAction)
                a = max(a,v)

            return (v, vAction)


        def minValue(currState, depth, agent, a, b):
            actions = currState.getLegalActions(agent)
            if terminalTest(currState, depth, actions) == True:         #if TERMINAL-TEST(state), then return UTILITY(state)
                return (self.evaluationFunction(currState), None)

            v = 10000000.0
            vAction = None

            for action in actions:
                newState = currState.generateSuccessor(agent, action)
                newValue, temp = fixCall(currState, newState, depth, agent, a, b)     #fixCall: same function as before(in minimax above)
                if newValue < v:
                    v = newValue
                    vAction = action
                
                #check and fix beta
                if v < a:
                    return (v, vAction)
                b = min(b, v)

            return (v, vAction)


        #initialize a, b with the corresponding values
        a = -10000000.0
        b = 10000000.0
        v, action = maxValue(gameState, 0, 0, a, b)
        return action

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """

        def terminalTest(gameState, depth, actions):
            if gameState.isWin() or gameState.isLose():
                return True
            elif len(actions)==0 or depth == self.depth:
                return True
            return False

        def fixCall(currState, newState, depth, agent):
            numAgents = currState.getNumAgents()
            if agent + 1 == numAgents:
                return maxValue(newState, depth+1, 0)
            else:
                return chanceValue(newState, depth, agent+1)


        def maxValue(currState, depth, agent):
            actions = currState.getLegalActions(agent)                  #pacman is always agent 0
            if terminalTest(currState, depth, actions) == True:         #if TERMINAL-TEST(state), then return UTILITY(state)
                return (self.evaluationFunction(currState), None)

            v = -10000000.0
            vAction = None                                              #successor and action

            for a in actions:
                newState = currState.generateSuccessor(agent, a)
                newValue, temp = chanceValue(newState, depth, agent+1)
                if newValue > v:
                    v = newValue
                    vAction = a
            return (v, vAction)


        #instead of minValue, chanceValue is implemented.
        def chanceValue(currState, depth, agent):
            actions = currState.getLegalActions(agent)
            if terminalTest(currState, depth, actions) == True:            #if TERMINAL-TEST(state), then return UTILITY(state)
                return (self.evaluationFunction(currState), None)

            #here we dont have v or vAction / v will be the average because we are in a chance node
            add=0
            for a in actions:
                newState = currState.generateSuccessor(agent, a)
                newValue, temp = fixCall(currState, newState, depth, agent)
                add += newValue                                                 #addition of all the returned values

            v = add/len(actions)
            return (v, None)

        v, action = maxValue(gameState, 0, 0)
        return action

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    #usefull data, similar to those we had in previous evaluation function
    currentPos = currentGameState.getPacmanPosition()
    currFood = currentGameState.getFood()
    flist = currFood.asList()
    ghostStates = currentGameState.getGhostStates()
    lowValue = -10000000.0
    
    #get current score, will be modified later by the values calculated
    currScore = currentGameState.getScore()

    #food
    for food in flist:
        distance = manhattanDistance(currentPos, food)
        currScore += (1/float(distance))

    #get ghost score, this time do not return low value immediately
    for ghost in ghostStates:
        gPos = ghost.getPosition()
        distance = manhattanDistance(currentPos, gPos)
        if distance == 0:
            continue
        if(distance < 3):
            currScore += 5*(1/float(distance))  
        else:
            currScore += (1/float(distance)) 

    return currScore


# Abbreviation
better = betterEvaluationFunction
