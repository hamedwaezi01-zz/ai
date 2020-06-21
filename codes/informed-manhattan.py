'''
Hamed Waezi
AI HW1 
A*
Heuristic => Manhattan Distance
'''
import heapq
import copy

print('Dimensions:')
dim = int(input())
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

    
    def manhattanDistance(self, curr, goal,): # h-value
        return abs(curr[0]- goal // self.n) + abs(curr[1] - goal % self.n) # dX + dY
    
    def linearConflicts(self,): # todo
        pass
    
    def f(self,): # Always call f
        if self.heuristic is not None:
            return self.heuristic + self.g
        heuristic = 0
        for i in range(0, self.n):
            for j in range(0, self.n):
                temp = self.data[i][j] - 1
                if self.data[i][j] != 0:
                    heuristic = heuristic + self.manhattanDistance(curr=(i, j), goal=temp)
        self.heuristic = heuristic
        return heuristic + self.g
        


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
#        print(str(inversions)+ ' ' + str((self.root.blank[0] - self.n) % 1))
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
        heapq.heapify(self.nodes)
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

        #self.root=[[13,2,10,3],[1,12,8,4],[5,0,9,6],[15,14,11,7]]
        #blank=(2,1)
        
        #self.root=[[3, 4, 8, 12], [7, 5, 10, 14], [0, 1, 6, 15], [2, 9, 13, 11]]
        #blank=(2,0)
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
        iteration = 0
        while True:
            iteration += 1
            bestNode = heapq.heappop(self.nodes)
            #print('# expanded : ' + str(self.nodesExpanded) + '    # deleted : '+str(self.nodesDeleted) + '  F: '+str(bestNode.f()))
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
#            print('MOVES : '+str(moves))
            for i in moves:
                newNode = bestNode.move(pp=bestNode, direction=i)
                if newNode in self.states:
                    self.nodesDeleted = self.nodesDeleted + 1
                    #print ('Expanded : ' + str(self.nodesExpanded) +' deleted : ' + str(self.nodesDeleted) + ' f : ' + str(bestNode.f())+'  blank:'+ bestNode.blank.__str__() + ' node :\n'+bestNode.__str__()+' deleting')
                    del newNode
                else:
                    self.nodesExpanded = self.nodesExpanded + 1
                    if self.nodesExpanded % 5000 == 0:
                        print(self.nodesExpanded)
                    #print ('Expanded : ' + str(self.nodesExpanded) + ' deleted : ' + str(self.nodesDeleted) + ' f : ' + str(bestNode.f())+'  blank:'+ bestNode.blank.__str__() + ' node :\n'+bestNode.__str__()+' adding')
#                    print('f : ' + str(newNode.f()) + ' ' + str(newNode.g))
                    if self.verify(newNode):
                        print('Done : ' + str(newNode.f()))
                        return newNode

                    self.states.add(newNode)
                    heapq.heappush(self.nodes,newNode)

if __name__ == '__main__':
    fileName = input()
    puzzle = Puzzle(n=dim,)
    res = puzzle.run()
    if res is not None:
    #    fileName = r'result-without-conflicts.txt'
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
        f.write('NodesExpanded: '+str(puzzle.nodesExpanded))
        f.close()
