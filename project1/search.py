# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
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
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first
    [2nd Edition: p 75, 3rd Edition: p 87]

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm
    [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    sets = set()
    # value = (list(), problem.getStartState())
    steps = problem.getStartState()
    # result = []
    result = util.Stack()
    dfshelper(problem, steps, sets, result)
    ans = []
    while not result.isEmpty():
        ans.insert(0, result.pop())
    print ans
    return ans
    util.raiseNotDefined()

def dfshelper(problem, steps, sets, result):
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    n = Directions.NORTH
    e = Directions.EAST
    state = steps
    if problem.isGoalState(state):
        return True
    elif state not in sets:
        sets.add(state)
        for sucs in problem.getSuccessors(state):
            if sucs[1] == 'South':
                result.push(s)
            elif sucs[1] == 'North':
                result.push(n)
            elif sucs[1] == 'West':
                result.push(w)
            else:
                result.push(e)
            #next = list(result) + [sucs[1]]
            # result.append(sucs[1])
            # value = (next, sucs[0])
            steps = sucs[0]
            if dfshelper(problem, steps, sets, result) == True:
                return True
            result.pop()
    return False

# def depthFirstSearch(problem):
#     """
#     Search the deepest nodes in the search tree first
#     [2nd Edition: p 75, 3rd Edition: p 87]
#
#     Your search algorithm needs to return a list of actions that reaches
#     the goal.  Make sure to implement a graph search algorithm
#     [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].
#
#     To get started, you might want to try some of these simple commands to
#     understand the search problem that is being passed in:
#
#     print "Start:", problem.getStartState()
#     print "Is the start a goal?", problem.isGoalState(problem.getStartState())
#     print "Start's successors:", problem.getSuccessors(problem.getStartState())
#     """
#     "*** YOUR CODE HERE ***"
#     stack = util.Stack()
#     visited = []
#     start = (problem.getStartState(), [])
#     stack.push(start)
#     while not stack.isEmpty():
#             point = stack.pop()
#             location = point[0]
#             if location in visited:
#                 continue
#
#             visited.append(location)
#             if problem.isGoalState(location):
#                 print point[1]
#                 return point[1]
#
#             nextpoint = problem.getSuccessors(location)
#             for successor in nextpoint:
#                 nextlocation = successor[0]
#                 move = successor[1]
#                 stack.push((nextlocation, point[1]+[move]))
#     return []
#
#     print "Start:", problem.getStartState()
#     print "Is the start a goal?", problem.isGoalState(problem.getStartState())
#     print "Start's successors:", problem.getSuccessors(problem.getStartState())
#     util.raiseNotDefined()

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    [2nd Edition: p 73, 3rd Edition: p 82]
    """
    "*** YOUR CODE HERE ***"
    queue = util.Queue()
    visited = []
    start = (problem.getStartState(), [])
    queue.push(start)
    while not queue.isEmpty():
        point = queue.pop()
        location = point[0]
        if location in visited:
            continue

        visited.append(location)
        if problem.isGoalState(location):
            # print point[1]
            return point[1]

        nextpoint = problem.getSuccessors(location)
        for successor in nextpoint:
            nextlocation = successor[0]
            move = successor[1]
            queue.push((nextlocation, point[1] + [move]))
    return []
    util.raiseNotDefined()

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    priorityqueue = util.PriorityQueue()
    visited = []
    start = (problem.getStartState(), [], 0)
    priorityqueue.push(start, 0)
    while not priorityqueue.isEmpty():
        point = priorityqueue.pop()
        location = point[0]
        if location in visited:
            continue

        visited.append(location)
        if problem.isGoalState(location):
            # print point[1]
            return point[1]

        nextpoint = problem.getSuccessors(location)
        for successor in nextpoint:
            nextlocation = successor[0]
            move = successor[1]
            priorityqueue.push((nextlocation, point[1] + [move], point[2]+successor[2]), point[2]+successor[2])
    return []
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    priorityqueue = util.PriorityQueue()
    visited = []
    start = (problem.getStartState(), [], 0)
    priorityqueue.push(start, 0)
    while not priorityqueue.isEmpty():
        point = priorityqueue.pop()
        location = point[0]
        if location in visited:
            continue

        visited.append(location)
        if problem.isGoalState(location):
            # print point[1]
            return point[1]

        nextpoint = problem.getSuccessors(location)
        for successor in nextpoint:
            nextlocation = successor[0]
            move = successor[1]
            priorityqueue.push((nextlocation, point[1] + [move], point[2]+successor[2]), point[2]+successor[2]+heuristic(nextlocation,problem))

    return []
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
