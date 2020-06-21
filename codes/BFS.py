'''
Hamed Waezi
AI HW1 
Uninformed
BFS
'''
from collections import deque
import copy
if __name__ == '__main__':
    print('Dimensions:')
    dim = int(input())

class Node: # Node is the state
    def __init__(self, n, data, parent, blank):
        self.n = n
        self.data = data # A 2D array 
        self.parent = parent
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
    
    def move(self, parent, direction):
        if direction == 0: # UP
            newData = copy.deepcopy(self.data)
            newData[self.blank[0]][self.blank[1]] = newData[self.blank[0] - 1][self.blank[1]]
            newData[self.blank[0] - 1][self.blank[1]] = 0
            temp = Node(self.n, data=newData, parent=self, blank=(self.blank[0] - 1, self.blank[1]))
            return temp
        elif direction == 1: # DOWN
            newData = copy.deepcopy(self.data)
            newData[self.blank[0]][self.blank[1]] = newData[self.blank[0] + 1][self.blank[1]]
            newData[self.blank[0] + 1][self.blank[1]] = 0
            temp = Node(self.n, data=newData, parent=self, blank=(self.blank[0] + 1, self.blank[1]))
            return temp
        elif direction == 2: # RIGHT
            newData = copy.deepcopy(self.data)
            newData[self.blank[0]][self.blank[1]] = newData[self.blank[0]][self.blank[1] + 1]
            newData[self.blank[0]][self.blank[1] + 1] = 0
            temp = Node(self.n, data=newData, parent=self, blank=(self.blank[0], self.blank[1] + 1))
            return temp
        elif direction == 3: # LEFT
            newData = copy.deepcopy(self.data)
            newData[self.blank[0]][self.blank[1]] = newData[self.blank[0]] [self.blank[1] - 1]
            newData[self.blank[0]] [self.blank[1] - 1] = 0
            temp = Node(self.n, data=newData, parent=self, blank=(self.blank[0], self.blank[1] - 1))
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
        self.states = set() # it holds hashes pointing to states
        self.root= root
        blank = None
        self.nodes = deque()
        self.nodesExpanded = 1
        self.nodesDeleted = 0
        self.n = n
        self.precheck=precheck
        goal = []
        for i in range(0,self.n):
            temp = []
            for j in range(0,self.n):
                temp.append(i * self.n + j + 1)
            goal.append(temp)
        goal[i][j] = 0

        goal = Node(n=self.n,data=goal,parent=None,blank=(self.n - 1,self.n - 1))
        self.goalhash = goal.__hash__()
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
        self.root = Node(n=self.n,data=self.root, parent=None, blank=blank)
        if (precheck):
            self.solvable = self.isSolvable()
        else: 
            self.solvable = True
        self.nodes.appendleft(self.root)
        self.states.add(self.root)


    def verify(self, node):
        return node.__hash__() == self.goalhash


    def run(self,):
        if not self.solvable:
            print ('is not solvable')
            return None
        while True:
            bestNode = self.nodes.pop()
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
                newNode = bestNode.move(parent=self, direction=i)
                if newNode in self.states:
                    self.nodesDeleted = self.nodesDeleted + 1
                    del newNode
                else:
                    self.nodesExpanded = self.nodesExpanded + 1
                    if self.verify(newNode):
                        return newNode
                    self.states.add(newNode)
                    self.nodes.appendleft(newNode)

if __name__ == '__main__':
    fileName=input()
    puzzle = Puzzle(n=dim,)
    res = puzzle.run()
    if res is not None:
        
        f = open(fileName,'w+')
        temp = res
        f.write(str(dim)+'\n')
        badChars = ['[',']']
        
        result = [str(res)]
        while temp.parent is not None:
            temp = temp.parent
            result.append(str(temp))
        
        for i in range(len(result)-1,-1,-1):
            temp= result[i].replace('[','')
            temp= temp.replace(']','')
            f.write(temp+'\n')
#        f.write('NodesExpanded: '+str(puzzle.nodesExpanded))
        f.close()