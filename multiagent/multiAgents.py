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
        minFoodDistance = 999999
        for xy in newFood.asList():
            minFoodDistance = min(minFoodDistance, manhattanDistance(newPos, (xy[0], xy[1])))
        if newFood.asList() == []:
            minFoodDistance = 0
        minGhostDistance = 999999
        for i in range(len(newGhostStates)):
            if newScaredTimes[i] == 0:
                minGhostDistance = min(minGhostDistance,
                manhattanDistance(newPos, newGhostStates[i].getPosition()))
        return successorGameState.getScore() - minFoodDistance / 2 + minGhostDistance / 8

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
        return self.miniMaxSearch(gameState, self.index, self.depth)[1]
        util.raiseNotDefined()

    def miniMaxSearch(self, gameState: GameState, agentIndex, depth):
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), Directions.STOP
        if agentIndex == 0:
            resultValue = -9999999
            resultAction = Directions.STOP
            legalActions = gameState.getLegalActions(agentIndex)
            for action in legalActions:
                successorState = gameState.generateSuccessor(agentIndex, action)
                currentValue = self.miniMaxSearch(successorState,
                        (agentIndex + 1) % gameState.getNumAgents(),
                        depth - (agentIndex + 1) // gameState.getNumAgents())[0]
                if resultValue < currentValue:
                    resultValue = currentValue
                    resultAction = action
        else:
            resultValue = 9999999
            resultAction = Directions.STOP
            legalActions = gameState.getLegalActions(agentIndex)
            for action in legalActions:
                successorState = gameState.generateSuccessor(agentIndex, action)
                currentValue = self.miniMaxSearch(successorState,
                        (agentIndex + 1) % gameState.getNumAgents(),
                        depth - (agentIndex + 1) // gameState.getNumAgents())[0]
                if resultValue > currentValue:
                    resultValue = currentValue
                    resultAction = action
        return resultValue, resultAction

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.alphaBetaSearch(gameState, self.index, self.depth, -99999999, 99999999)[1]
        util.raiseNotDefined()

    def alphaBetaSearch(self, gameState: GameState, agentIndex, depth, alpha, beta):
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), Directions.STOP
        if agentIndex == 0:
            resultValue = -9999999
            resultAction = Directions.STOP
            legalActions = gameState.getLegalActions(agentIndex)
            for action in legalActions:
                successorState = gameState.generateSuccessor(agentIndex, action)
                currentValue = self.alphaBetaSearch(successorState,
                        (agentIndex + 1) % gameState.getNumAgents(),
                        depth - (agentIndex + 1) // gameState.getNumAgents(), alpha, beta)[0]
                if resultValue < currentValue:
                    resultValue = currentValue
                    resultAction = action
                if resultValue > beta:
                    return resultValue, resultAction
                alpha = max(alpha, resultValue) 
        else:
            resultValue = 9999999
            resultAction = Directions.STOP
            legalActions = gameState.getLegalActions(agentIndex)
            for action in legalActions:
                successorState = gameState.generateSuccessor(agentIndex, action)
                currentValue = self.alphaBetaSearch(successorState,
                        (agentIndex + 1) % gameState.getNumAgents(),
                        depth - (agentIndex + 1) // gameState.getNumAgents(), alpha, beta)[0]
                if resultValue > currentValue:
                    resultValue = currentValue
                    resultAction = action
                if resultValue < alpha:
                    return resultValue, resultAction
                beta = min(beta, resultValue)
        return resultValue, resultAction


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
        "*** YOUR CODE HERE ***"

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.expectiMaxSearch(gameState, self.index, self.depth)[1]
        util.raiseNotDefined()

    def expectiMaxSearch(self, gameState: GameState, agentIndex, depth):
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), Directions.STOP
        if agentIndex == 0:
            resultValue = -9999999
            resultAction = Directions.STOP
            legalActions = gameState.getLegalActions(agentIndex)
            for action in legalActions:
                successorState = gameState.generateSuccessor(agentIndex, action)
                currentValue = self.expectiMaxSearch(successorState,
                        (agentIndex + 1) % gameState.getNumAgents(),
                        depth - (agentIndex + 1) // gameState.getNumAgents())[0]
                if resultValue < currentValue:
                    resultValue = currentValue
                    resultAction = action
        else:
            resultValue = 0
            resultAction = Directions.STOP
            legalActions = gameState.getLegalActions(agentIndex)
            for action in legalActions:
                successorState = gameState.generateSuccessor(agentIndex, action)
                currentValue = self.expectiMaxSearch(successorState,
                        (agentIndex + 1) % gameState.getNumAgents(),
                        depth - (agentIndex + 1) // gameState.getNumAgents())[0]
                resultValue += currentValue
            resultValue /= len(legalActions)
        return resultValue, resultAction

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]

    minFoodDistance = 999999
    for xy in food.asList():
        minFoodDistance = min(minFoodDistance, manhattanDistance(pos, (xy[0], xy[1])))
    if food.asList() == []:
        minFoodDistance = 0
    minGhostDistance = 999999
    for i in range(len(ghostStates)):
        if scaredTimes[i] == 0:
            minGhostDistance = min(minGhostDistance,
            manhattanDistance(pos, ghostStates[i].getPosition()))
    return currentGameState.getScore() - minFoodDistance / 2 + minGhostDistance / 8
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
