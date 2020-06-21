'''
Hamed Waezi
AI HW1 
A*
Heuristic => Disjoint Patter database 4-4-4-3
'''
import heapq
import copy
import pickle as p

if __name__ == '__main__':
    dim = int(input('Dimensions: '))
    tiles = dim*dim


class Node: # Node is the state
    
    def __init__(self, n, data, pp, blank, g):
        self.n = n
        self.data = data # A 2D array 
        self.pp = pp
        self.blank = blank
        self.hash = None
        self.heuristic = None
        self.g = g
        self.subHashes = [0,0,0,0]
        self.subData = [0,0,0,0]
        temp = [{1,2,5,6,0},{3,4,7,8,0},{9,10,13,14,0},{11,12,15,0}]
        for idx in range(4):
            data = copy.deepcopy(self.data)
            for i in range(self.n):
                for j in range(self.n):
                    if data[i][j] not in temp[idx]:
                        data[i][j] = -1
            self.subData[idx] = data
            hashBase = 293
            hashMode = 100000000000000000007
            hashh = 1
            for i in range(0,self.n):
                for j in range(0,self.n):
                    hashh = hashh * hashBase
                    hashh = hashh + data[i][j]
                    hashh = hashh % hashMode
            self.subHashes[idx] = hashh
    def __str__(self,):
        ret = ''
        for rows in self.data:
            ret = ret + '\n' + rows.__str__()
        return self.data.__str__()
    
    def __hash__(self,):
        if self.hash is not None:
            return self.hash
        hashBase = 67
        hashMode = 1e12+7
        self.hash = 1
        for i in range(0,self.n):
            for j in range(0,self.n):
                self.hash = self.hash * hashBase
                self.hash = self.hash + self.data[i][j]
                self.hash = self.hash % hashMode
        self.hash = int(self.hash)
        return self.hash

    def __gt__(self,other):
        return self.f() > other.f()
    
    def __lt__(self, other):
        return self.f() < other.f()

    def __eq__(self, other):
        return self.hash == other.hash
    
    def move(self, pp, direction):
        if pp is None:
            g = 1
        else:
            g = pp.g + 1
        if direction == 0: # UP
            newData = copy.deepcopy(self.data)
            newData[self.blank[0]][self.blank[1]] = newData[self.blank[0] - 1][self.blank[1]]
            newData[self.blank[0] - 1][self.blank[1]] = 0
            temp = Node(n=self.n, data=newData, pp=self, blank=(self.blank[0] - 1, self.blank[1]), g=g)
            return temp
        elif direction == 1: # DOWN
            newData = copy.deepcopy(self.data)
            newData[self.blank[0]][self.blank[1]] = newData[self.blank[0] + 1][self.blank[1]]
            newData[self.blank[0] + 1][self.blank[1]] = 0
            temp = Node(n=self.n, data=newData, pp=self, blank=(self.blank[0] + 1, self.blank[1]), g=g)
            return temp
        elif direction == 2: # RIGHT
            newData = copy.deepcopy(self.data)
            newData[self.blank[0]][self.blank[1]] = newData[self.blank[0]][self.blank[1] + 1]
            newData[self.blank[0]][self.blank[1] + 1] = 0
            temp = Node(n=self.n, data=newData, pp=self, blank=(self.blank[0], self.blank[1] + 1), g=g)
            return temp
        elif direction == 3: # LEFT
            newData = copy.deepcopy(self.data)
            newData[self.blank[0]][self.blank[1]] = newData[self.blank[0]] [self.blank[1] - 1]
            newData[self.blank[0]] [self.blank[1] - 1] = 0
            temp = Node(n=self.n, data=newData, pp=self, blank=(self.blank[0], self.blank[1] - 1), g=g)
            return temp


    def f(self,):
        self.res = 0
        for i in range(4):
            if int(self.subHashes[i]) in Node.dbs[i]:
                Node.nodesFound += 1
                self.res += Node.dbs[i][int(self.subHashes[i])]
            else:
                Node.nodesNotFound += 1
        
        return self.res + self.g
    
class Puzzle: # it is the current puzzle

    
    def countInversions(self,):
        dd = []
        for i in range (0, self.n):
            for j in range(0,self.n):
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
        if self.n % 2 == 1:
            return inversions % 2 == 0
        else:
            return (inversions % 2 == 0 and ((self.root.blank[0] - self.n) % 2 == 1)) or (inversions % 2 == 1 and ((self.root.blank[0] - self.n) % 2 == 0))


    def __init__(self, n,):  # `n` is the dim of puzzle
        self.states = set() # it holds hashes pointing to states
        self.root= []
        blank = None
        self.nodes = []
        self.nodesExpanded = 1
        self.nodesDeleted = 0
        self.n = n
        goal = []
        for i in range(0,self.n):
            temp = []
            for j in range(0,self.n):
                temp.append(i * self.n + j + 1)
            goal.append(temp)
        goal[i][j] = 0
        goal = Node(n=self.n,data=goal,pp=None,blank=(self.n - 1,self.n - 1), g = 0)
        self.goalhash = goal.__hash__()
        
        print('Input your matrix')
        for i in range(0, self.n):
            temp = input().split()
            temp = list(map(int, temp))
            if len(temp) != self.n:
                raise Exception("Bad Input\n"+"Dimension is: "+str(self.n))
            for j in range(0, self.n):
                 if temp[j] == 0:
                     blank = (i,j)
            self.root.append(temp)
        
        
#        self.root=[[13,2,10,3],[1,12,8,4],[5,0,9,6],[15,14,11,7]]
#        blank=(2,1)
        
#        self.root=[[1,2,3,4],[0,6,7,8],[5,10,11,12],[9,13,14,15]]
#        blank=(1,0)
        #### DEVIL'S CONFIGURATION
#        self.root=[[0, 15, 8, 3], [12, 11, 7, 4] ,[14, 10, 5, 6], [9, 13, 2, 1]]
#        blank=(0,0)
        #####
#        self.root=[[3, 4, 8, 12], [7, 5, 10, 14], [0, 1, 6, 15], [2, 9, 13, 11]]
#        blank=(2,0)
        self.root = Node(n=self.n,data=self.root, pp=None, blank=blank, g=1)
        self.solvable = self.isSolvable()
        heapq.heappush(self.nodes,self.root)
        self.states.add(self.root)

    def verify(self, node):
        return node.__hash__() == self.goalhash


    def run(self,):
        if not self.solvable:
            print ('is not solvable')
            return None
        print('search started ...')
        iteration = 0
        while True:
            iteration += 1
            bestNode = heapq.heappop(self.nodes)
            blank = bestNode.blank
            moves = []
            if blank[0] > 0:
                moves.append(0)
            if blank[0] < self.n-1 :
                moves.append(1)
            if blank[1] > 0 :
                moves.append(3)
            if blank[1] < self.n-1 :
                moves.append(2)
            for i in moves:
                newNode = bestNode.move(pp=bestNode, direction=i)
                if newNode in self.states:
                    self.nodesDeleted = self.nodesDeleted + 1
                    del newNode
                else:
                    self.nodesExpanded = self.nodesExpanded + 1
                    if self.nodesExpanded % 5000 == 0:
                        print(self.nodesExpanded)
                    if self.verify(newNode):
                        print('Done : ' + str(newNode.f()))
                        return newNode
                    
                    self.states.add(newNode)
                    heapq.heappush(self.nodes,newNode)

if __name__ == '__main__':
    fileName = input('output file name : ')
    #Disjoint Patter Databases Initialization
    try:
        Node.dbs
        print('Databases already loaded')
    except:
        Node.dbs = [{},{},{},{}]
        for i in range(4):
            f = open('db-4443-'+str(i+1)+'.pkl','rb')
            Node.dbs[i] = p.load(f)
        print('Databases loaded :')
    Node.nodesFound = 0
    Node.nodesNotFound = 0
    
    puzzle = Puzzle(n=dim,)
    res = puzzle.run()
    if res is not None:
        f = open(fileName,'w+')
        temp = res
        f.write(str(dim)+'\n')
        badChars = ['[',']']
        result = [str(res)]
        while temp.pp is not None:
            temp = temp.pp
            result.append(str(temp))
        for i in range(len(result)-1,-1,-1):
            temp= result[i].replace('[','')
            temp= temp.replace(']','')
            f.write(temp+'\n')
#        f.write('NodesExpanded: '+str(puzzle.nodesExpanded))
        f.close()
