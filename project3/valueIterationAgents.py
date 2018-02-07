# valueIterationAgents.py
# -----------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
  """
      * Please read learningAgents.py before reading this.*

      A ValueIterationAgent takes a Markov decision process
      (see mdp.py) on initialization and runs value iteration
      for a given number of iterations using the supplied
      discount factor.
  """
  def __init__(self, mdp, discount = 0.9, iterations = 100):
    """
      Your value iteration agent should take an mdp on
      construction, run the indicated number of iterations
      and then act according to the resulting policy.
    
      Some useful mdp methods you will use:
          mdp.getStates()
          mdp.getPossibleActions(state)
          mdp.getTransitionStatesAndProbs(state, action)
          mdp.getReward(state, action, nextState)
    """
    self.mdp = mdp
    self.discount = discount
    self.iterations = iterations
    self.values = util.Counter() # A Counter is a dict with default 0
     
    "*** YOUR CODE HERE ***"
    states = self.mdp.getStates()
    for i in range(self.iterations):
      vtemp = self.values.copy()
      for state in states:
        maxV = None
        actions = self.mdp.getPossibleActions(state)
        for act in actions:
          V = self.getQValue(state, act)
          #print(T)
          if maxV == None or V > maxV:
            maxV = V
        if maxV == None:
          maxV = 0
        vtemp[state] = maxV
      self.values = vtemp
      #self.values[state] = V


  def getValue(self, state):
    """
      Return the value of the state (computed in __init__).
    """
    return self.values[state]


  def getQValue(self, state, action):
    """
      The q-value of the state action pair
      (after the indicated number of value iteration
      passes).  Note that value iteration does not
      necessarily create this quantity and you may have
      to derive it on the fly.
    """
    "*** YOUR CODE HERE ***"
    Trans = self.mdp.getTransitionStatesAndProbs(state, action)
    V = 0
    for tran in Trans:
      nextState = tran[0]
      T = tran[1]
      R = self.mdp.getReward(state, action, nextState)
      Vn = self.values[nextState]
      V += T * (R + (self.discount * Vn))
    return V
    util.raiseNotDefined()

  def getPolicy(self, state):
    """
      The policy is the best action in the given state
      according to the values computed by value iteration.
      You may break ties any way you see fit.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return None.
    """
    "*** YOUR CODE HERE ***"
    actions = self.mdp.getPossibleActions(state)
    if len(actions) == 0:
      return None
    V = None
    A = None
    for act in actions:
      Trans = self.mdp.getTransitionStatesAndProbs(state, act)
      # for tran in Trans:
      #   nextState = tran[0]
      #   T = tran[1]
      #   V = self.values[nextState]
      #   if maxV == None or V > maxV:
      #     maxV = V
      #     A = act
      vtemp = self.getQValue(state, act)
      if V == None or vtemp > V:
        V = vtemp
        A = act
    return A
    util.raiseNotDefined()

  def getAction(self, state):
    "Returns the policy at the state (no exploration)."
    return self.getPolicy(state)
  
