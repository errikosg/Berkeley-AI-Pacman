from csp import *
import search
from collections import defaultdict, OrderedDict
import itertools

# Explanation of code in README -> 1115201400037_project3.pdf

def display(result, size):
    #gets result and displays it like a grid
    if(result == None):
        print("Display error: result = None")
        return
    my_dict = {}
    for r in result:
        if('X' in r):
            x = int(r.split("X")[1])
            my_dict[x] = result[r]

    temp = OrderedDict(sorted(my_dict.items(), key=lambda t: t[0]))
    items = list(temp.items())

    index=0
    for j in range(4*size):
        print('_', end='')
    print('\n')
    for i in range(size):
        for j in range(size):
            if(j < size-1):
                print("|", items[index][1], end=' ')
            else:
                print("|", items[index][1], "|", end='\n')
            index += 1
        for j in range(4*size):
            print('_', end='')
        print('\n')

class kenken(CSP):

    def __init__(self, size):
        self.cliques = self.getCliques(size)
        self.variables = self.getVariables(size, self.cliques)
        self.domains = self.getDomains(size, self.variables, self.cliques)
        self.neighbors = self.getClassicNeighbors(size, self.variables, self.cliques)
        '''print("Cliques: ", self.cliques, end='\n\n')
        print("Variables: ", self.variables, end='\n\n')
        print("Domains: ", self.domains, end='\n\n')
        print("Neighbors: ", self.neighbors, end='\n\n')'''

        #initialize csp
        CSP.__init__(self, self.variables, self.domains, self.neighbors, self.constraints)

    def constraints(self, A, a, B, b):
        if('X' in A and 'X' in B):
            return a != b
        elif('X' in A and 'E' in B):
            position = self.getPosition(A, self.cliques)
            return a == b[position]
        elif('E' in A and 'X' in B):
            position = self.getPosition(B, self.cliques)
            return b == a[position]

    def getVariables(self, size, cliques):
        #gets size (example 3 if grid is 3x3) and makes variables
        var = []
        rng = size*size

        for i in range(rng):
            string = "X" + str(i+1)
            var.append(string)

        #encapsulated variables
        for i in range(len(cliques.items())):
            string = "E" + str(i+1)
            var.append(string)
        return var

    def getDomains(self, size, variables, cliques):
        #gets size and variables and appoints initial domains
        domains = {}
        dm_casual = []
        dm_encaps = []
        rem = []

        for i in range(size):
            dm_casual.append(i+1)
        #get all domains of X.. variables
        for x in variables:
            if(not 'E' in x):
                domains[x] = dm_casual
        
        #fix encapsulated variables
        index=0
        items = list(cliques.items())
        for x in variables:
            if('E' in x):
                lst = self.getList(items[index][0])
                for y in lst:
                    dm_encaps.append(domains[y])
                evdom = list(itertools.product(*dm_encaps))
                #clear all the not needed tuples
                for y in evdom:
                    op = items[index][1][0]
                    strgoal = items[index][1].replace(op, '')
                    goal = int(strgoal)
                    if(op == '+'):
                        count = self.getCount(y)
                        if(not count is goal):
                            rem.append(y)
                    elif(op == '-'):
                        dif = abs(y[1] - y[0])
                        if(not dif is goal):
                            rem.append(y)
                    elif(op == '/'):
                        mx, mn = max(y[0],y[1]), min(y[0], y[1])
                        div = int(mx / mn)
                        if(not div is goal):
                            rem.append(y)
                    elif(op == 'x'):
                        pr = self.getProduct(y)
                        if(not pr is goal):
                            rem.append(y)
                    else:
                        if(not y[0] is goal):            #int(items[index][1][1]
                            rem.append(y)

                for y in rem:
                    evdom.remove(y)
                rem.clear()
                domains[x] = evdom
                dm_encaps.clear()
                index += 1
        return domains

    def getClassicNeighbors(self, size, variables, cliques):
        #get size and variables and finds neighbors - neighbors of a tile are the tiles in the same row and column
        neighbors = {}
        items = list(cliques.items())

        index=0
        for x in variables:
            if('X' in x):
                row = []
                column = []
                cl =[]
                #get column
                curr = int(x.split("X")[1])
                temp = curr-size
                while(temp > 0):
                    column.append("X" + str(temp))
                    temp -= size
                temp = curr+size
                while(temp <= size*size):
                    column.append("X" + str(temp))
                    temp += size
                #get row
                div, mod = int(curr/size), curr%size
                if(mod != 0):
                    row_num = div+1
                else:
                    row_num = div
                now = (row_num-1)*size + 1
                end = row_num*size
                while(now <= end):
                    if(now != curr):
                        row.append("X" + str(now))
                    now += 1

                #get info from cliques
                e_index=1
                for i in items:
                    lst = self.getList(i[0])
                    if(x not in lst):
                        e_index += 1
                    else:
                        break
                cl.append('E'+str(e_index))
                neighbors[x] = row + column + cl
            elif('E' in x):
                lst = self.getList(items[index][0])
                neighbors[x] = lst
                index += 1
        return neighbors

    def getCliques(self, size):
        try:
            fp = open("Grids.txt", "r")
        except FileNotFoundError:
            print("!!! ERROR, Grids.txt file MUST be present in this current folder in order for kenken to run. It contains all the hardcoded grids the problem needs. It is given alongside kenken.py in the project folder.", end='\n\n')
            return None
        dc = {}
        search = str(size)+"x"+str(size)
        for ln in fp:
            line = ln.replace('\n', '')
            size = line.split(":")
            if(size[0] == search):
                cl = size[1].split(" ")
                for y in cl:
                    data = y.split("]")
                    dc[data[0]+str("]")] = data[1]
        fp.close()
        return dc

    def getList(self, string):
        L = string.split(",")
        lst = []
        for l in L:
            med = l.replace(']', '')
            new = med.replace('[', '')
            lst.append(new)
        return lst

    def getCount(self, tup):
        count = 0
        for x in tup:
            count += x
        return count

    def getProduct(self, tup):
        pr = 1
        for x in tup:
            pr *= x
        return pr

    def getPosition(self, x, cliques):
        items = list(cliques.items())
        for i in items:
            lst = self.getList(i[0])
            if(x in lst):
                ret = lst.index(x)
                return ret

#main
# define the size of the grid!!!
size = 7
h = kenken(size)

#1st: FC algorithm
res1 = backtracking_search(h, inference=forward_checking)
display(res1, size)
print("->FC", end='\n\n\n')

'''Uncomment to run:

#2nd: FC+mrv algorithm
res2 = backtracking_search(h, select_unassigned_variable=mrv, inference=forward_checking)
display(res2, size)
print("FC + MRV", end='\n\n\n')

#3rd: BT algrorithm
re3 = backtracking_search(h)
display(res3, size)
print("-> BT", end='\n\n\n')

#4th: BT+mrv algorithm
res4 = backtracking_search(h, select_unassigned_variable=mrv)
display(res4, size)
print("-> BT + MRV", end='\n\n\n')

#5th: MAC
res5 = backtracking_search(h, inference=mac)
display(res5, size)
print("MAC", end='\n\n\n')'''
