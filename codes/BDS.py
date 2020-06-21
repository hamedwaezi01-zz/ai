'''
Hamed Waezi
AI HW1 
Uninformed
BDS
'''
from collections import deque
import copy

if __name__ == '__main__':
    print('Dimensions:')
    dim = int(input())

class Node: # Node is the state
    def __init__(self, n, data, parent, child, blank):
        self.n = n
        self.data = data # A 2D array 
        self.parent = parent
        self.child = child
        self.blank = blank
        self.hash = None
        self.heuristic = None

    def __str__(self,):
        ret = ''
        for rows in self.data:
            ret = ret + '\n' + rows.__str__()
        return self.data.__str__()
    
    def __hash__(self,):
        if self.hash is not None:
            return self.hash
        hashBase = 67
        hashMode = 1e9+7
        self.hash = 1
        for i in range(0,self.n):
            for j in range(0,self.n):
                self.hash = self.hash * hashBase
                self.hash = self.hash + self.data[i][j]
                self.hash = self.hash % hashMode
        self.hash = int(self.hash)
        return self.hash
    
    def __eq__(self, other):
        return self.__hash__() == other.__hash__()
    
    def move(self, direction, fromGoal):
        if direction == 0: # UP
            newData = copy.deepcopy(self.data)
            newData[self.blank[0]][self.blank[1]] = newData[self.blank[0] - 1][self.blank[1]]
            newData[self.blank[0] - 1][self.blank[1]] = 0
            temp = Node(self.n, data=newData, parent=None if fromGoal else self, child=self if fromGoal else None, blank=(self.blank[0] - 1, self.blank[1]))
            return temp
        elif direction == 1: # DOWN
            newData = copy.deepcopy(self.data)
            newData[self.blank[0]][self.blank[1]] = newData[self.blank[0] + 1][self.blank[1]]
            newData[self.blank[0] + 1][self.blank[1]] = 0
            temp = Node(self.n, data=newData, parent=None if fromGoal else self, child=self if fromGoal else None, blank=(self.blank[0] + 1, self.blank[1]))
            return temp
        elif direction == 2: # RIGHT
            newData = copy.deepcopy(self.data)
            newData[self.blank[0]][self.blank[1]] = newData[self.blank[0]][self.blank[1] + 1]
            newData[self.blank[0]][self.blank[1] + 1] = 0
            temp = Node(self.n, data=newData, parent=None if fromGoal else self, child=self if fromGoal else None, blank=(self.blank[0], self.blank[1] + 1))
            return temp
        elif direction == 3: # LEFT
            newData = copy.deepcopy(self.data)
            newData[self.blank[0]][self.blank[1]] = newData[self.blank[0]] [self.blank[1] - 1]
            newData[self.blank[0]] [self.blank[1] - 1] = 0
            temp = Node(self.n, data=newData, parent=None if fromGoal else self, child=self if fromGoal else None, blank=(self.blank[0], self.blank[1] - 1))
            return temp


class Puzzle: # it is the current puzzle
    
    def countInversions(self,):
        dd = []
        for i in range (0, self.n):
            for j in range(0,self.n):
#                print(str(i)+'  '+str(j))
                dd.append(self.root.data[i][j])
        
        inversions = 0
        for i in range(0,self.n*self.n-1):
            for j in range(i+1, self.n*self.n):
                if dd[j] != 0 and dd[i] != 0 and dd[i] > dd[j]:
                    inversions = inversions + 1

        print('# Inversions : '+str(inversions))
        return inversions
   

    def isSolvable(self,):
        inversions = self.countInversions()
#        print(str(inversions)+ ' ' + str((self.root.blank[0] - self.n) % 1))
        if self.n % 2 == 1:
            return inversions % 2 == 0
        else:
            return (inversions % 2 == 0 and ((self.root.blank[0] - self.n) % 2 == 1)) or (inversions % 2 == 1 and ((self.root.blank[0] - self.n) % 2 == 0))

    

    def __init__(self, n, root=None, precheck=True):  # `n` is the dim of puzzle
        self.leftStates = set() # it holds hashes pointing to states of Left
        self.rightStates = set() # it holds hashes pointing to states of Right
        self.leftFring1 = set()
        self.leftFring2 = set()
        self.rightFring1 = set()
        self.rightFring2 = set()
        
        self.root= root
        blank = None
        self.nodes = deque()
        self.nodesExpanded = 1
        self.nodesDeleted = 0
        self.n = n
        self.precheck=precheck
        self.goal = []
        for i in range(0,self.n):
            temp = []
            for j in range(0,self.n):
                temp.append(i * self.n + j + 1)
            self.goal.append(temp)
        self.goal[i][j] = 0

        self.goal = Node(n=self.n,data=self.goal,parent=None, child=None,blank=(self.n - 1,self.n - 1))
        if root is None:
            print('Input your matrix')
            self.root = []
            for i in range(0, self.n):
                temp = input().split()
                temp = list(map(int, temp))
                if len(temp) != self.n:
                    raise Exception("Bad Input\n"+"Dimension is: "+str(self.n))
                for j in range(0, self.n):
                     if temp[j] == 0:
                         blank = (i,j)
                self.root.append(temp)
            
            #blank = (1,2)
            #self.root = [[1, 2, 3, 4],[ 5, 10, 7, 8], [13, 6, 11, 12],[ 9, 14, 0, 15]]
            #blank=(2,2)
            #self.root=[[1, 2, 3, 4], [5, 6, 7, 8], [9, 11, 0, 12], [13, 10, 14, 15]]
        else:
            for i in range(self.n):
                for j in range(self.n):
                    if root[i][j] == 0:
                        blank=(i,j)
                        break
        self.root = Node(n=self.n,data=self.root, parent=None, child=None, blank=blank)
        if (precheck):
            self.solvable = self.isSolvable()
        else: 
            self.solvable = True
        self.nodes.appendleft(self.root)
        
        self.rightFring1.add(self.root)
        self.leftFring1.add(self.goal)
        
        self.rightStates.add(self.root)
        self.leftStates.add(self.goal)

    
    def moveRight(self,): # From Root State ## right to left
        for bestNode in self.rightFring1:
            blank = bestNode.blank
            moves = []
            if blank[0] < self.n-1 :
                moves.append(1)
            if blank[0] > 0:
                moves.append(0)
            if blank[1] > 0 :
                moves.append(3)
            if blank[1] < self.n-1 :
                moves.append(2)
            for i in moves:
                newNode = bestNode.move(direction=i, fromGoal=False)
                if newNode in self.rightStates:
                    self.nodesDeleted = self.nodesDeleted + 1
                    del newNode
                else:
                    self.nodesExpanded = self.nodesExpanded + 1
                    self.rightStates.add(newNode)
                    self.rightFring2.add(newNode)
                    self.nodes.append(newNode)
    
    
    def moveLeft(self,): # From Goal State ## left to right
        for bestNode in self.leftFring1:
            blank = bestNode.blank
            moves = []
            if blank[0] > 0: 
                moves.append(0)# UP
            if blank[1] > 0 :  
                moves.append(3)# LEFT
            if blank[1] < self.n-1 : 
                moves.append(2)# RIGHT
            if blank[0] < self.n-1 : 
                moves.append(1)# DOWN
            for i in moves:
                newNode = bestNode.move(direction=i,fromGoal=True)
                if newNode in self.leftStates:
                    self.nodesDeleted = self.nodesDeleted + 1
                    del newNode
                else:
                    self.nodesExpanded = self.nodesExpanded + 1
                    self.leftStates.add(newNode)
                    self.leftFring2.add(newNode)
                    self.nodes.append(newNode)

    
    def swapLeft(self,):
        self.leftFring1.clear()
        self.leftFring1.update(self.leftFring2)
        self.leftFring2.clear()
        pass
    
    
    def swapRight(self,):
        self.rightFring1.clear()
        self.rightFring1.update(self.rightFring2)
        self.rightFring2.clear()
        pass
    
    
    def verify(self,):
        for node in self.rightFring1:
            if node in self.leftFring2 or node in self.leftFring1:
                return node, 1
        
        for node in self.rightFring2:
            if node in self.leftFring2 or node in self.leftFring1:
                return node, 2
        
        return None, -1
    
    
    def search(self,):
        if not self.solvable:
            print ('is not solvable')
            return None
        while True:
            self.moveRight()
            self.moveLeft()
            
            result, fringIndex = self.verify()
            if result is not None:
                return result, fringIndex
            
            self.swapLeft()
            self.swapRight()
    
    
    def run(self,):
        result, fringIndex = self.search() # its child are all None
        
        #
        # the `result` node is on right fring
        # which is on the root side of the puzzle
        #
        
        
        # looks for the same node in left and right fringes
        for node in self.leftFring1:
            if result == node:
                result.child = node.child
                break
        else:
            for node in self.leftFring2:
                if result == node:
                    result.child = node.child
                    break
        while result.parent is not None:
            child = result
            result = result.parent
            result.child = child
        
        return result
            

if __name__ == '__main__':
    fileName=input()
    puzzle = Puzzle(n=dim,)
    result = puzzle.run()
    if result is not None:
        
        f = open(fileName,'w+')
        f.write(str(dim)+'\n')
        badChars = ['[',']']
        
        while result is not None:
            temp = str(result.data)
            
            for char in badChars:
                temp= temp.replace(char, '')
#            print(temp)
            f.write(temp+'\n')
            result = result.child
#        f.write('NodesExpanded: '+str(puzzle.nodesExpanded))
        
        f.close()