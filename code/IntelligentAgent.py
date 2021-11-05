
import random
from BaseAI import BaseAI
import math
from Grid import Grid
import time


class IntelligentAgent(BaseAI):
    startTime = 0
    alocatedTime = 0
    inTime = True
    def getMove(self, grid):
        depth = 0
        self.startTime = time.time()
        self.inTime = True
        self.alocatedTime = 0.21
        maxDepth = 5
        maxChild = None
        maxUtil = 0
        while self.inTime:
            (child, utility) = self.maximize(grid, float("-inf"), float("inf"), maxDepth)
            if child is not None and utility > maxUtil:
                maxUtil = utility
                maxChild = child
            maxDepth += 1
            #print("depth: ", maxDepth)
        #print("util: " + str(utility))
        #print("total move time: " + str(time.time() - self.startTime))
        return maxChild[0] if maxChild else None


    def getMaxFive(self, grid):
        #return top 5
        list = []
        for row in grid.map:
            for i in row:
                list.append(i)
        topFive = sorted(list)[-5:]
        return topFive

    #def medianTile(self, grid):
    #    return statistics.median(self.getMaxFive(grid)) 


    def weightMatrix(self, grid):
        matrix = [[4**15, 4**14, 4**13, 4**12],
                  [4**8, 4**9, 4**10, 4**11],
                  [4**7, 4**6, 4**5, 4**4],
                  [4**0, 4**1, 4**2, 4**3]]
        utility = 0
        for i in range(4):
            for j in range(4):
                utility += grid.map[i][j] * matrix[i][j] 
        return utility

    def gradientMatrix(self, grid):
        matrix = [[4**6, 4**5, 4**4, 4**3],
                  [4**5, 4**4, 4**3, 4**2],
                  [4**4, 4**3, 4**2, 4**1],
                  [4**3, 4**2, 4**1, 4**0]]
        utility = 0
        for i in range(0, 4):
            for j in range(0, 4):
                utility += grid.map[i][j] * matrix[i][j] 
        return utility

    def utility(self, grid):
        return self.weightMatrix(grid) + len(grid.getAvailableCells())*(4**5)
        #return math.log2(self.weightMatrix(grid)) + len(grid.getAvailableCells())*10 + math.log2(grid.getMaxTile())*5 + math.log2(self.sumOfTiles(grid))*5 + 100*math.log2(self.gradientMatrix(grid))


    def monotonicity(self, grid):
        penalty = 0
        for i in range(4):
            for j in range(3):
                if grid.map[i][j + 1] > grid.map[i][j]:
                    penalty += grid.map[i][j + 1]
                if grid.map[j + 1][i] > grid.map[j][i]:
                    penalty += grid.map[j + 1][i]
        return penalty

    def sumOfTiles(self, grid):
        sum = 0
        for i in range(4):
            for j in range(4):
                sum += grid.map[i][j]
        return sum

    def numberOfMergers(self, grid):
        num = 0
        for i in range(4):
            for j in range(4):
                if grid.crossBound((i + 1, j)) and grid.map[i + 1][j] == grid.map[i][j]:
                    num += 1
                if grid.crossBound((i - 1, j)) and grid.map[i - 1][j] == grid.map[i][j]:
                    num += 1
                if grid.crossBound((i, j + 1)) and grid.map[i][j + 1] == grid.map[i][j]:
                    num += 1
                if grid.crossBound((i, j - 1)) and grid.map[i][j - 1] == grid.map[i][j]:
                    num += 1
        return num

    def outOfTime(self):
        if time.time() - self.startTime > self.alocatedTime:
            #print("out of time")
            self.inTime = False
            return True
        return False

    def maxDepth(self, maxDepth):
        return maxDepth == 0

    def maximize(self, state, a, b, maxDepth):
        if self.maxDepth(maxDepth) or self.terminalMaxTest(state) or self.outOfTime():
            return (None, self.utility(state))

        (maxChild, maxUtility) = (None, float("-inf"))
        stateChildren = state.getAvailableMoves()
        if len(stateChildren) > 1:
            stateChildren = list(filter(lambda x: x[0] != 1, stateChildren)) #remove one move from list

        for child in stateChildren:
            utility = self.chance(child[1], a, b, maxDepth - 1)
            if utility > maxUtility:
                (maxChild, maxUtility) = (child, utility)

            if maxUtility >= b:
                break
            if maxUtility > a:
                a = maxUtility
        
        return (maxChild, maxUtility)

    def chance(self, state, a, b, maxDepth):
        if self.maxDepth(maxDepth) or self.outOfTime():
            return self.utility(state)
        return 0.9 * self.minimize(state, a, b, 2, maxDepth - 1) + 0.1 * self.minimize(state, a, b, 4, maxDepth - 1)

    def minimize(self, state, a, b, tileVal, maxDepth):
        if self.maxDepth(maxDepth) or self.terminalMinTest(state) or self.outOfTime():
            return self.utility(state)

        minUtility = float("inf")
        for tile in state.getAvailableCells():
            copyState = state.clone()
            copyState.insertTile(tile, tileVal)
            (_, utility) = self.maximize(copyState, a, b, maxDepth - 1)
            if utility < minUtility:
                minUtility = utility

            if minUtility <= a:
                break
            if minUtility < b:
                b = minUtility
        return minUtility

    def terminalMaxTest(self, grid):
        return not grid.getAvailableMoves()

    def terminalMinTest(self, grid):
        return not grid.getAvailableCells()

#if __name__ == '__main__':
#    agent = IntelligentAgent()
#    g = Grid()

#    g.map = [[2, 0, 4, 0],
#             [0, 0, 0, 0],
#             [0, 2, 4, 0],
#             [0, 0, 0, 0]]

#    utility= agent.minimize(g, float("-inf"), float("inf"), 2, 0,1)
#    print(utility)
    #print(agent.monotonicity(g))

#    for i in g.map:
#        print(i)
#    print("max five")
#    print(agent.getMaxFive(g))

#    print("min")
#    print(agent.minTile(g))

#    print(agent.utility(g))


#    agent.weightMatrix()
