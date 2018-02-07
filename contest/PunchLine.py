# baselineTeam.py
# ---------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from captureAgents import CaptureAgent
import distanceCalculator
import random, time, util
from game import Directions
import game
from util import nearestPoint
import sys

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'OffensiveReflexAgent', second = 'DefensiveReflexAgent'):
  """
  This function should return a list of two agents that will form the
  team, initialized using firstIndex and secondIndex as their agent
  index numbers.  isRed is True if the red team is being created, and
  will be False if the blue team is being created.

  As a potentially helpful development aid, this function can take
  additional string-valued keyword arguments ("first" and "second" are
  such arguments in the case of this function), which will come from
  the --redOpts and --blueOpts command-line arguments to capture.py.
  For the nightly contest, however, your team will be created without
  any extra arguments, so you should make sure that the default
  behavior is what you want for the nightly contest.
  """
  return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########

class ReflexCaptureAgent(CaptureAgent):
  """
  A base class for reflex agents that chooses score-maximizing actions
  """
  def chooseAction(self, gameState):
      enemies = [a for a in self.getOpponents(gameState) if gameState.getAgentState(a).getPosition() != None]
      def max_val(gameState, d):
          if d == 0 or gameState.isOver():
              return self.evaluationFunction(gameState), Directions.STOP

          enemy = min(enemies)

          actions = gameState.getLegalActions(self.index)

          actions.remove(Directions.STOP)
          suc = [gameState.generateSuccessor(self.index, action)
                 for action in actions]

          values = [min_val(successor, enemy, d)[0]
                    for successor in suc]

          maxval = max(values)
          bestmove = [index for index in range(len(values)) if
                         values[index] == maxval]
          move = random.choice(bestmove)

          return maxval, actions[move]

      def min_val(gameState, enemy, d):
          if d == 0 or gameState.isOver():
              return self.evaluationFunction(gameState), Directions.STOP

          actions = gameState.getLegalActions(enemy)

          actions.remove(Directions.STOP)
          suc = [gameState.generateSuccessor(enemy, action)
                 for action in actions]

          if enemy < max(enemies):
              values = [min_val(successor, max(enemies), d)[0]
                        for successor in suc]
          else:
              values = [max_val(successor, d - 1)[0]
                        for successor in suc]
          minval = min(values)

          return minval, Directions.STOP

      if len(enemies) != 0:
          # print "1"
          action = max_val(gameState, d=2)[1]
      else:
          actions = gameState.getLegalActions(self.index)
          actions.remove(Directions.STOP)
          sucs = [self.getSuccessor(gameState, action) for action in actions]
          # You can profile your evaluation time by uncommenting these lines
          # start = time.time()
          values = [self.evaluationFunction(suc) for suc in sucs]
          # print 'eval time for agent %d: %.4f' % (self.index, time.time() - start)

          maxValue = max(values)
          # print "1"
          action = random.choice([a for a, v in zip(actions, values) if v == maxValue])
      # print action
      return action


  def getSuccessor(self, gameState, action):
    """
    Finds the next successor which is a grid position (location tuple).
    """
    successor = gameState.generateSuccessor(self.index, action)
    pos = successor.getAgentState(self.index).getPosition()
    if pos != nearestPoint(pos):
      # Only half a grid position was covered
      return successor.generateSuccessor(self.index, action)
    else:
      return successor

  def evaluationFunction(self, gameState):
    util.raiseNotDefined()

class OffensiveReflexAgent(ReflexCaptureAgent):
  """
  A reflex agent that seeks food. This is an agent
  we give you to get an idea of what an offensive agent might look like,
  but it is by no means the best or only way to build an offensive agent.
  """
  def evaluationFunction(self, gameState):

    # Useful information you can extract from a GameState (pacman.py)
    myState = gameState.getAgentState(self.index)
    myPos = myState.getPosition()
    enemies = [gameState.getAgentState(i) for i in self.getOpponents(gameState)]
    invaders = [a for a in enemies if not a.isPacman and a.getPosition() != None]
    capsules = None
    if self.red:
        capsules = gameState.getBlueCapsules()
    else:
        capsules = gameState.getRedCapsules()

    capsulesDistances = [self.getMazeDistance(myPos, capsule) for capsule in
                                capsules]
    minCapsuleDistance = min(capsulesDistances) if len(capsulesDistances) else 0

    mindistanceToFood = sys.maxint
    mindistanceToGhost = 0

    initialScore = self.getScore(gameState)
    # print initialScore

    foodList = self.getFood(gameState).asList()
    if len(foodList) > 0: # This should always be True,  but better safe than sorry
      myPos = myState.getPosition()
      minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
      mindistanceToFood = minDistance

    if len(invaders) > 0:
      diststog = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
      mindistanceToGhost = min(diststog)
    else:
        mindistanceToGhost = 0
    # if mindistanceToGhost >= 3:
    #     mindistanceToGhost = 0

    scaredTimes = [gameState.getAgentState(enemy).scaredTimer for enemy
                   in self.getOpponents(gameState)]

    # If they are scared be aggressive.
    if min(scaredTimes) >= 3 or not gameState.getAgentState(self.index).isPacman:
        mindistanceToGhost = 0
    # if mindistanceToFood <= mindistanceToGhost:
    #     mindistanceToGhost = 0

    if min(scaredTimes) <= 6 and mindistanceToGhost < 4:
        mindistanceToGhost *= -1

    return  1*initialScore - 3*mindistanceToFood + 100*mindistanceToGhost - 100*len(foodList) - 10000*len(capsules) - 10*minCapsuleDistance


  def chooseAction(self, gameState):
      return ReflexCaptureAgent.chooseAction(self, gameState)



class DefensiveReflexAgent(ReflexCaptureAgent):
    def evaluationFunction(self, gameState):
        myPos = gameState.getAgentPosition(self.index)

        enemies = self.getOpponents(gameState)

        enemies = [gameState.getAgentState(i) for i in self.getOpponents(gameState)]
        invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]

        if len(invaders) > 0:
            dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
            mindistanceToPac = min(dists)
        else:
            mindistanceToPac = 0

        capsules = self.getCapsulesYouAreDefending(gameState)
        capsulesDistances = [self.getMazeDistance(myPos, capsule) for capsule in
                             capsules]
        minCapsuleDistance = min(capsulesDistances) if len(capsulesDistances) else 0

        EdistC = [self.getMazeDistance(a.getPosition(), capsule) for a in invaders for capsule in capsules]
        if len(invaders) > 0 and len(EdistC)!=0 and min(EdistC) > 3:
            minCapsuleDistance = 0

        return -1000000 * len(invaders) - 10000 * mindistanceToPac - minCapsuleDistance

    def chooseAction(self, gameState):
        return ReflexCaptureAgent.chooseAction(self, gameState)
