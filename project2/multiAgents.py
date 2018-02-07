# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util
import sys

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

    "*** YOUR CODE HERE ***"
    initialScore = successorGameState.getScore()
    mindistanceToFood = sys.maxint
    mindistanceToGhost = sys.maxint
    capsules = successorGameState.getCapsules()
    for food in newFood.asList():
      distanceToFood = abs(newPos[0] - food[0]) + abs(newPos[1] - food[1])
      if distanceToFood < mindistanceToFood:
        mindistanceToFood = distanceToFood

    for ghost in newGhostStates:
      distanceToGhost = abs(newPos[0] - ghost.getPosition()[0]) + abs(newPos[1] - ghost.getPosition()[1])
      if distanceToGhost < mindistanceToGhost:
        mindistanceToGhost = distanceToGhost

    if mindistanceToGhost > 5:
      mindistanceToGhost = 100

    return  initialScore + 10/mindistanceToFood + mindistanceToGhost

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

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"
    def max_value(state, d):
      if state.isWin() or state.isLose() or d == 0:
        return self.evaluationFunction(state)
      val = -sys.maxint-1
      for action in state.getLegalActions(0):
        if action == Directions.STOP:
          continue
        suc = state.generateSuccessor(0, action)
        val = max(val, min_value(suc, d - 1, state.getNumAgents()-1))
      return val

    def min_value(state, d, num):
      index = num
      if state.isWin() or state.isLose() or d == 0:
        return self.evaluationFunction(state)
      val = sys.maxint
      for action in state.getLegalActions(index):
        if action == Directions.STOP:
          continue
        suc = state.generateSuccessor(index, action)
        if num == 1:
          val = min(val, max_value(suc, d - 1))
        else:
          val = min(val, min_value(suc, d, num - 1))
      return val

    a = Directions.STOP
    v = -sys.maxint-1
    for actions in gameState.getLegalActions():
      successor = gameState.generateSuccessor(0, actions)
      temp = v
      v = max(v, min_value(successor, self.depth, gameState.getNumAgents()-1))
      if v > temp:
        a = actions
    return a
    util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    def max_value(state, a, b, d):
      if state.isWin() or state.isLose() or d == 0:
        return self.evaluationFunction(state)
      val = -sys.maxint-1
      for action in state.getLegalActions(0):
        if action == Directions.STOP:
          continue
        suc = state.generateSuccessor(0, action)
        val = max(val, min_value(suc, a, b, d-1, state.getNumAgents()-1))
        if val > b:
          return val
        a = max(val, a)
      return val

    def min_value(state, a, b, d, num):
      index = num
      if state.isWin() or state.isLose() or d == 0:
        return self.evaluationFunction(state)
      val = sys.maxint
      for action in state.getLegalActions(index):
        if action == Directions.STOP:
          continue
        suc = state.generateSuccessor(index, action)
        if num == 1:
          val = min(val, max_value(suc, a, b, d - 1))
        else:
          val = min(val, min_value(suc, a, b, d, num - 1))
        if val < a:
          return val
        b = min(val, b)
      return val

    act = Directions.STOP
    v = -sys.maxint-1
    alp = -sys.maxint-1
    bet = sys.maxint
    for action in gameState.getLegalActions(0):
      t = v
      v = max(v, min_value(gameState.generateSuccessor(0, action), alp, bet, self.depth, gameState.getNumAgents()-1))
      if v > t:
        act = action
      if v >= bet:
        return act
      alp = max(alp, v)
    return act

    util.raiseNotDefined()

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
    def max_value(state, d):
      if state.isWin() or state.isLose() or d == 0:
        return self.evaluationFunction(state)
      val = -sys.maxint-1
      for action in state.getLegalActions(0):
        if action == Directions.STOP:
          continue
        suc = state.generateSuccessor(0, action)
        val = max(val, exp_value(suc, d - 1, state.getNumAgents()-1))
      return val

    def exp_value(state, d, num):
      index = num
      if state.isWin() or state.isLose() or d == 0:
        return self.evaluationFunction(state)
      val = 0
      actions = state.getLegalActions(index)
      l = len(actions)
      for action in actions:
        if action == Directions.STOP:
          continue
        suc = state.generateSuccessor(index, action)
        if num == 1:
          val = max_value(suc, d - 1)
        else:
          val += exp_value(suc, d, num - 1)
      return val/l

    if gameState.isWin() or gameState.isLose():
      return self.evaluationFunction(gameState)
    a = Directions.STOP
    v = -sys.maxint-1
    for actions in gameState.getLegalActions():
      successor = gameState.generateSuccessor(0, actions)
      temp = v
      v = max(v, exp_value(successor, self.depth, gameState.getNumAgents()-1))
      if v > temp:
        a = actions
    return a
    util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """
  "*** YOUR CODE HERE ***"
  newPos = currentGameState.getPacmanPosition()
  newFood = currentGameState.getFood()
  newGhostStates = currentGameState.getGhostStates()
  initialScore = currentGameState.getScore()
  mindistanceToFood = sys.maxint
  mindistanceToGhost = sys.maxint
  free = True

  for food in newFood.asList():
    distanceToFood = abs(newPos[0] - food[0]) + abs(newPos[1] - food[1])
    if distanceToFood < mindistanceToFood:
      mindistanceToFood = distanceToFood

  for ghost in newGhostStates:
    if ghost.scaredTimer != 0:
      continue
    distanceToGhost = abs(newPos[0] - ghost.getPosition()[0]) + abs(newPos[1] - ghost.getPosition()[1])
    if distanceToGhost < mindistanceToGhost:
      mindistanceToGhost = distanceToGhost
    free = False

  if mindistanceToGhost > 5 or free:
    mindistanceToGhost = 100

  return initialScore + mindistanceToGhost + 10/mindistanceToFood

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

