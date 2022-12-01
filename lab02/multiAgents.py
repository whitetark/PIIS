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
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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

    def evaluationFunction(self, currentGameState: GameState, action):
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

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState: GameState):
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
    def minimax(self, gameState, agent, depth):
        # If pacman won/lost or max depth reached, we stop recursion
        if depth == 0 or gameState.isLose() or gameState.isWin():
            return [self.evaluationFunction(gameState)]

        # If it's pacman (agent zero)
        if agent == 0:
            maxValue = -float("inf")
            pacmanActions = gameState.getLegalActions(agent)

            # For all its possible movements
            for action in pacmanActions:
                successorState = gameState.generateSuccessor(agent, action)

                # After pacman, the first ghost moves, we go into recursion
                max = self.minimax(successorState, agent + 1, depth)[0]

                # Pakman maximizer, so we look for the highest value of movement among potential ones
                if max > maxValue:
                    maxValue = max
                    bestAction = action

            return (maxValue, bestAction)

        # Queue of one of the ghosts (minimizer). Executed when the agent is not equal to zero. Also, if it's the last ghost's turn, the agent's number will reset to 0
        else:
            minValue = float("inf")
            ghostsNum = gameState.getNumAgents() - 1
            
            # Determine for whom to process movements in recursion next
            if agent == ghostsNum:
                depth -= 1
                next = 0
            else:
                next = agent + 1
            ghostActions = gameState.getLegalActions(agent)

            # For all possible ghost moves
            for action in ghostActions:
                successorState = gameState.generateSuccessor(agent, action)
                # Recursively, we call the function for the next agent
                min = self.minimax(successorState, next, depth)[0]
                # Update minimum value. Ghosts are minimizers interested in the lowest value
                if min < minValue:
                    minValue = min
                    bestAction = action

            return [minValue, bestAction]

    def getAction(self, gameState: GameState):
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        return self.minimax(gameState, self.index, self.depth)[1]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def alphabeta(self, gameState, agent, depth, alpha, beta):
        # If pacman won / programs or max depth reached, stop recursion
        if depth == 0 or gameState.isLose() or gameState.isWin():
            return [self.evaluationFunction(gameState)]

        # If this is pacman (agent zero)
        if agent == 0:
            maxValue = -float("inf")
            pacmanActions = gameState.getLegalActions(agent)

            # For all its possible moves
            for action in pacmanActions:
                successorState = gameState.generateSuccessor(agent, action)
                # After pacman, the first ghost moves, we go into recursion
                newMax = self.alphabeta(successorState, agent + 1, depth, alpha, beta)[0]
                # Pacman is maximizer, so we look for the highest value of movement among potential ones
                if newMax > maxValue:
                    maxValue = newMax
                    bestAction = action
                # If max > beta => cut off
                if maxValue > beta:
                    return [maxValue]
                # Update alpha
                alpha = max(alpha, maxValue)
            return [maxValue, bestAction]

        # Queue of one of the ghosts (minimizer). Executed when the agent is not equal to zero. Also, if it's the last ghost's turn, the agent's number will reset to 0
        else:
            minValue = float("inf")
            ghostsNum = gameState.getNumAgents() - 1

            # Determine for whom to process movements in recursion next
            if agent == ghostsNum:
                depth -= 1
                next_agent = 0
            else:
                next_agent = agent + 1
            ghostActions = gameState.getLegalActions(agent)

            # For all possible ghost moves
            for action in ghostActions:
                successorState = gameState.generateSuccessor(agent, action)
                # Recursively, we call the function for the next agent
                new_min = self.alphabeta(successorState, next_agent, depth, alpha, beta)[0]
                
                # Update minimum value. Ghosts are minimizers interested in the lowest value
                if new_min < minValue:
                    minValue = new_min
                    bestAction = action
                # If minimum < alpha => cut off
                if minValue < alpha:
                    return [minValue]
                # Update beta
                beta = min(beta, minValue)

            return [minValue, bestAction]

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.alphabeta(gameState, self.index, self.depth, -float("inf"), float("inf"))[1]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def expectimax(self, gameState, agent, depth):
        # If pacman won / programs or max depth reached, stop recursion
        if depth == 0 or gameState.isLose() or gameState.isWin():
            return [self.evaluationFunction(gameState)]

        # If this is pacman (agent zero)
        if agent == 0:
           maxValue = -float("inf")
           pacmanActions = gameState.getLegalActions(agent)

            # For all its possible moves
           for action in pacmanActions:
               successorState = gameState.generateSuccessor(agent, action)
               # After pacman, the first ghost moves
               newMax = self.expectimax(successorState, agent + 1, depth)[0]

               # Pacman is maximizer, so we look for the highest value of movement among potential ones
               if newMax > maxValue:
                   maxValue = newMax
                   bestAction = action
           return [maxValue, bestAction]

        # Queue of one of the ghosts (minimizer). Executed when the agent is not equal to zero. Also, if it's the last ghost's turn, the agent's number will reset to 0
        else:
            minValue = 0
            ghostsNum = gameState.getNumAgents() - 1
            
            # Determine for whom to process movements in recursion next
            if agent == ghostsNum:
                depth -= 1
                next = 0
            else:
                next = agent + 1
            ghostActions = gameState.getLegalActions(agent)

            # For all possible ghost moves
            for action in ghostActions:
                successorState = gameState.generateSuccessor(agent, action)
                # Recursively, we call the function for the next agent and sum all the values ​​of the ghost's movements
                minValue += self.expectimax(successorState, next, depth)[0]
            
            
            # All moves are equal, so we multiply the minimum value by (1 / number of ghosts)
            minValue = minValue * (1.0 / len(ghostActions))
            return [minValue, action]

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"

        return self.expectimax(gameState, self.index, self.depth)[1]

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
