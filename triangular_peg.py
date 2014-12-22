#!/usr/bin/env python

'''
Script to solve triangular peg solitaire game (http://en.wikipedia.org/wiki/Peg_solitaire). 
Ran into it in on my first US trip on christmas 2013 in Cracker Barrel restaurant and some 
friendly dispute there inspired to write following script

Triangular peg board is in format:
        01
      02, 03 
    04, 05, 06
  07, 08, 09, 10
11, 12, 13, 14, 15

Initially all positions are filled with figures besides one (or two). player aims to clear the board
by taking one figure, jumping over adjacent figure and landing on empty position (without figure).
Move can be made on straight line. For example if there is figure on 01 and 03, but not on 06, you can move figure from 
01 to 06 - jump over 03 - and so remove figure from 03

So from any position there could be 6 available moves:
- horizontally left and right
- diagonally up left and right
- diagonally down left and right
In actual game available moves depends on where does position lay on board - eg. it's not possible to move up
from positions 01, 02, 03 because there just are no positions that direction
Also requirement for move is, that in that direction, there is figure to jump over, and empty position to land on

Script below creates a board with available moves from each position (generateStepsMap)
Fills table with initial figures (getInitialStatusMap)
and then runs findSequence function that returns list of longest available list of steps on given board setup 
(uses recursion and dynamic programming techniques)

usage: ./triangular_peg.py [list of positions (1...15) initially empty]
'''

import random
import sys

__author__ = "saarlo"

def generateStepsMap():
    '''
    generate empty board and all possibly existing moves from each position on board
    @return dict stepsMap

    '''
    xs = range(1,16)
    board = [xs[i:j] for i,j in zip([0,1,3,6,10], [1,3,6,10,16])]
    stepsMap = {}
    for y in range(0,len(board)): #loop over rows
        for x in range(0, len(board[y])): #loop over elements in each row
            steps = []
            try: #horizontal right
                steps.append((board[y][x+1], board[y][x+2]))
            except IndexError as e:
                pass
            try: #horizontal left
                if x >= 2:
                    steps.append((board[y][x-1], board[y][x-2]))
            except IndexError as e:
                pass
            try: #up right
                steps.append((board[y+1][x], board[y+2][x]))
            except IndexError as e:
                pass
            try: #up left
                if y >= 2 and x >= 2:
                    steps.append((board[y-1][x-1], board[y-2][x-2]))
            except IndexError as e:
                pass
            try: #down right
                steps.append((board[y+1][x+1], board[y+2][x+2]))
            except IndexError as e:
                pass
            try: #down left
                if y >=2:
                    steps.append((board[y-1][x], board[y-2][x]))
            except IndexError as e:
                pass
            stepsMap[board[y][x]] = steps
    return stepsMap

def getInitialStatusMap(fieldsEmpty = [1]):
    '''
    get dictionary of pos => status (1/0)
    '''
    board = dict(zip(range(1,16), [1 for i in range(15)]))
    for f in fieldsEmpty:
        board[f] = 0
    return board

def getPossibleSteps(statusMap, stepsMap):
    '''
    list of possible steps available with given table status
    '''
    okSteps = []
    for pos, steps in stepsMap.iteritems():
        for step in steps:
            if statusMap[pos] and statusMap[step[0]] and not statusMap[step[1]]:
                okSteps.append([pos] + list(step))
    return okSteps

def doStep(step, statusMap):
    '''
    make the step and change table accordingly
    '''
    assert(statusMap[step[0]] and statusMap[step[1]] and not statusMap[step[2]])
    statusMap[step[0]] = 0
    statusMap[step[1]] = 0
    statusMap[step[2]] = 1
    return statusMap


def findSequence(statusMap, stepsMap):
    '''
    Find optimal sequence of steps
    - for given table setup loop through all possible steps
    - recursion: execute each step and recursively call itself for new setup
    - the longest sequence is the optimal (removes most buttons from table)
    - dynamic programming: additional step - store optimal statuses for table setups that are already checked before
    @return 
    '''
    if tuple(statusMap.values()) in bestSequences:
        return  bestSequences[tuple(statusMap.values())]
    steps = getPossibleSteps(statusMap, stepsMap)
    sequences = []
    for step in steps:
        _statusMap = doStep(step, statusMap.copy())
        #print "%s\t%s\t%s" % (step, len(steps), sum(_statusMap.values()))
        seq = [step] + findSequence(_statusMap, stepsMap)
        sequences.append(seq)
    #return max sequence
    bestSeq = max(sequences, key=len) if sequences else [] 
    bestSequences[tuple(statusMap.values())] = bestSeq
    return bestSeq

if __name__ == '__main__':
    if len(sys.argv) == 1:
        emptyPositions = [1]
    else:
        emptyPositions = set(int(arg) for arg in sys.argv[1:] if arg in map(str, range(15)))
    bestSequences = {}
    stepsMap = generateStepsMap()
    statusMap = getInitialStatusMap(emptyPositions)

    print 'Positions empty in beginning:', list(emptyPositions)
    sequence = findSequence(statusMap, stepsMap)
    print 'The longest sequence of steps:', sequence
    print 'Figures left on board:', len(stepsMap) - len(emptyPositions) - len(sequence)
    print 'Figures removed:', len(sequence)
        