'''
Hamed Waezi
AI HW1
Disjoint pattern Generator
'''


import copy
from collections import deque
import pickle as p

if __name__ == '__main__':
#    print('Dimensions:')
#    dim = int(input())
    dim = 4

class Node: # Node is the state
    def __init__(self, n, data, parent, blank,cost=0):
        self.n = n
        self.data = data # A 2D array 
        self.parent = parent
        self.cost = cost
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
        hashBase = 293
        hashMode = 100000000000000000007
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
    

    def move(self, direction):
        if direction == 0: # UP
            newData = copy.deepcopy(self.data)
            newData[self.blank[0]][self.blank[1]] = newData[self.blank[0] - 1][self.blank[1]]
            newData[self.blank[0] - 1][self.blank[1]] = 0
            c = 0
            if newData[self.blank[0]][self.blank[1]] != -1:
                c = 1
            temp = Node(self.n, data=newData, parent=self, blank=(self.blank[0] - 1, self.blank[1]), cost=self.cost+c)
            return temp
        elif direction == 1: # DOWN
            newData = copy.deepcopy(self.data)
            newData[self.blank[0]][self.blank[1]] = newData[self.blank[0] + 1][self.blank[1]]
            newData[self.blank[0] + 1][self.blank[1]] = 0
            c = 0
            if newData[self.blank[0]][self.blank[1]] != -1:
                c = 1
            temp = Node(self.n, data=newData, parent=self, blank=(self.blank[0] + 1, self.blank[1]), cost=self.cost+c)
            return temp
        elif direction == 2: # RIGHT
            newData = copy.deepcopy(self.data)
            newData[self.blank[0]][self.blank[1]] = newData[self.blank[0]][self.blank[1] + 1]
            newData[self.blank[0]][self.blank[1] + 1] = 0
            c = 0
            if newData[self.blank[0]][self.blank[1]] != -1:
                c = 1
            temp = Node(self.n, data=newData, parent=self, blank=(self.blank[0], self.blank[1] + 1), cost=self.cost+c)
            return temp
        elif direction == 3: # LEFT
            newData = copy.deepcopy(self.data)
            newData[self.blank[0]][self.blank[1]] = newData[self.blank[0]] [self.blank[1] - 1]
            newData[self.blank[0]] [self.blank[1] - 1] = 0
            c = 0
            if newData[self.blank[0]][self.blank[1]] != -1:
                c = 1
            temp = Node(self.n, data=newData, parent=self, blank=(self.blank[0], self.blank[1] - 1), cost=self.cost+c)
            return temp


class Puzzle: # it is the current puzzle
    
    def __init__(self, n, root=None):  # `n` is the dim of puzzle
        self.states = set() # it holds hashes pointing to states
        self.nodes = deque() # IT IS A STACK
        self.nodesExpanded = 1
        self.nodesDeleted = 0
        self.results = dict()
        self.n = n
#        self.patternDim = patternDim
        if root == None:
            root = []
            for i in range(0,self.n):
                temp = []
                for j in range(0,self.n):
                    temp.append(i * self.n + j + 1)
                root.append(temp)
            root[i][j] = 0
        
        self.root = Node(n=self.n, data=root, parent=None, blank=(self.n - 1,self.n - 1))
        self.goalhash = self.root.__hash__()
        self.nodes.append(self.root)
#        self.states.add(self.root)
        

    
    def run(self,): # depthToGo : Number of depth to go starts by 1
        iteration = 0
#        self.levelNodes = []
#        for i in range(depthToGo+1):
#            self.levelNodes.append(0)
#        currDepth = 0
#        self.levelNodes[0] = 1
        #print('asd '+str(levelNodes[0]))
        while len(self.nodes) != 0:
            iteration += 1
            if iteration == 5000 :
                print(len(self.results))
                iteration = 0
           # iterations += 1
            #levelNodes[currDepth] -= 1
#            print("lol : "+str(currDepth))
            
            
#            if self.levelNodes[currDepth] == 0:
#                currDepth = currDepth+1
            
#            if currDepth == depthToGo-1 or levelNodes[currDepth] == 0:
#                while levelNodes[currDepth] == 0 and currDepth >= 0:
#                   # print("currDepth :" + str(currDepth))
#                    currDepth -= 1
#                if levelNodes[currDepth] != 0:
#                    levelNodes[currDepth] -= 1
#            else:
#            self.levelNodes[currDepth] -= 1
            bestNode = self.nodes.pop()
            
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
                newNode = bestNode.move(direction=i)
                if newNode in self.states:
                    self.nodesDeleted = self.nodesDeleted + 1
                    del newNode
                else:
                    self.nodesExpanded = self.nodesExpanded + 1
                    self.results[newNode.__hash__()] = newNode.cost
                    self.states.add(newNode)
                    self.nodes.appendleft(newNode)

            
if __name__ == '__main__':
    fileName=input("Database name: ")
    # 4 4 4 3
    puzzle = Puzzle(n=dim,root=[[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,11,12],[-1,-1,15,0]])
#    puzzle = Puzzle(n=dim,root=[[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,11,12],[13,14,15,0]])
    
#    puzzle = Puzzle(n=dim,root=[[-1,-1,-1,-1],[-1,6,7,8],[9,10,-1,-1],[-1,-1,-1,0]])
    puzzle.run()
    f = open(fileName,'wb')
    #f.write("lol")
#    while len(res)> 0:
#        print("LOL")
#        node = res.pop()
#        f.write(str(node.data)+"\n")
    p.dump(puzzle.results,f)
    f.close()
    
#    for item in res:
#        temp = str(item.data)
#        temp= temp.replace('[','')
#        temp= temp.replace(']','')
##        print(str(item.data) + ' ' + str(item.cost))
#        f.write(temp+' '+ str(item.cost) +'\n')
    
    '''
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
        f.write('NodesExpanded: '+str(puzzle.nodesExpanded))
        f.close()
'''
