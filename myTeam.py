# myTeam.py
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

from captureAgents import CaptureAgent
import random, time, util
from game import Directions
import game
from argparse import Action
from operator import xor
import distanceCalculator
from distanceCalculator import Distancer
from __builtin__ import True

#################
# Team creation #
#################


def createTeam(firstIndex, secondIndex, isRed,
               first='DummyAgent', second='DummyAgent'):
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

    # The following line is an example only; feel free to change it.
    return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########
    
class DummyAgent(CaptureAgent):
    """
    A Dummy agent to serve as an example of the necessary agent structure.
    You should look at baselineTeam.py for more details about how to
    create an agent as this is the bare minimum.
    """

    def registerInitialState(self, gameState):

        """
        This method handles the initial setup of the
        agent to populate useful fields (such as what team
        we're on).
    
        A distanceCalculator instance caches the maze distances
        between each pair of positions, so your agents can use:
        self.distancer.getDistance(p1, p2)
    
        IMPORTANT: This method may run for at most 15 seconds.
        """
    
        '''
        Make sure you do not delete the following line. If you would like to
        use Manhattan distances instead of maze distances in order to save
        on initialization time, please take a look at
        CaptureAgent.registerInitialState in captureAgents.py.
        '''
        CaptureAgent.registerInitialState(self, gameState)
    
        '''
        Your initialization code goes here, if you need any.
        '''
        self.prevDirection = None

    def chooseAction(self, gameState):

        """
        Picks among actions randomly.
        """
        actions = gameState.getLegalActions(self.index)
        '''
        You should change this in your own agent.
        '''
        
        foodCoords = self.getFood(gameState).asList()
        startPos = gameState.getAgentPosition(self.index)
        distancer = Distancer(gameState.data.layout)
        foodCoords.sort(key = lambda pos: distancer.getDistance(startPos, pos))
        
        if len(foodCoords) > 0:
            path = aStar(startPos[0], startPos[1], foodCoords[0][0], foodCoords[0][1], gameState)
            x, y = path[-2].position
            for stop in path:
                print stop.position
            if x > startPos[0]:
                return Directions.EAST
            elif x < startPos[0]:
                return Directions.WEST
            elif y > startPos[1]:
                return Directions.NORTH
            elif y < startPos[1]:
                return Directions.SOUTH
            
        else:
            return Directions.STOP


#         carrying = gameState.getAgentState(self.index).numCarrying
#         if self.red != carrying:
#             priorities = [Directions.EAST, self.prevDirection, Directions.NORTH, Directions.SOUTH, Directions.WEST]
#         else:
#             priorities = [Directions.WEST, self.prevDirection, Directions.SOUTH, Directions.NORTH, Directions.EAST]
#     
#         for a in priorities:
#             if a in actions:
#                 self.prevDirection = a
#                 return a
#         
#         return a
    
def aStar(startX, startY, endX, endY, gameState):
    openList = list()
    closedList = list()
    maxX = gameState.data.layout.width
    maxY = gameState.data.layout.height
    
    startNode = Node((startX, startY))
    endNode = Node((endX, endY))
    
    openList.append(startNode)
    
    openList.sort(key=lambda x: (x.f))
    
    while len(openList) > 0:
        currentNode = openList.pop(0)
        closedList.append(currentNode)
        
        # is this node the target?
        if currentNode.position == endNode.position:
            path = list()
            generatePath(path, currentNode)
            return path
       
        #generate children
        children = list()
        childOffsets = [(1,0), (-1, 0), (0,1), (0,-1)]
        for offset in childOffsets:
            x, y = offset
            pos = currentNode.position
            pos = (pos[0]+x, pos[1]+y)
            if pos[0] < maxX and pos[1] < maxY and not gameState.hasWall(pos[0], pos[1]):
                children.append(Node(pos, parent = currentNode))
        
        for child in children:
            stop = False
            for closedN in closedList:
                if child.position == closedN.position:
                    stop = True
                    continue
            if stop:
                continue
            
            #calculate f
            child.g = currentNode.g + 1
            child.h = ((child.position[0] - endNode.position[0]) ** 2) + ((child.position[1] - endNode.position[1]) ** 2)
            child.calcF()
            
            stop = False
            for openN in openList:
                if child.position == openN.position and child.g > openN.g:
                    stop = True
                    continue
            if stop:
                continue
            
            openList.append(child)
            
        openList.sort(key=lambda x: (x.f))
            
def generatePath(path, n):
    path.append(n)
    if n.parent != None:
        generatePath(path, n.parent)

class Node:
    def __init__(self, position, f=0, g=0, h=0, parent=None):
        self.f = f
        self.g = g
        self.h = h
        self.position = position
        self.children = list()
        self.parent = parent
        
    def __eq__(self, other):
        return self.position == other.position
    
    def calcF(self):
        self.f = self.g + self.h
            
    
