# Main program for assignment 2. Your job here is to finish the
# Solver class's __init__ method to solve the puzzle as described
# in the handout.
#
from MinPQ import MinPQ
from Board import Board

import functools
@functools.total_ordering


class Node(object):
    def __init__(self, bd, moves, node):
        '''Construct a new node object.'''
        self.board = bd         # save the board
        self.moves = moves      # number of moves to reach this board.
        self.cost = bd.distance() # save the distance metric.
        self.previous = node      # save the previous node.
    def __gt__(self, other):
        '''A node is 'greater' than another if the cost plus the
        number of moves is larger. Note that this code will fail
        if 'other' is None.'''
        return (self.cost + self.moves) > (other.cost + other.moves)
    def __eq__(self, other):
        '''Two nodes are equal if the sum of the cost and moves are
        the same. The board itself is ignored.'''
        if self is other:       # comparing to itself?
            return True
        if other is None:       # comparing to None
            return False
        return (self.cost + self.moves) == (other.cost + other.moves)


class Solver(object):
    def __init__(self, initial):
        '''Initialize the object by finding the solution for the
        puzzle.'''
        self.__solvable = False
        self.__trace = []
        #This is where your code to solve the puzzle will go!
        #initial is the starting state of the puzzle
        #create a MinPQ, then create a Node based on the initial Board, and insert the initial Node on the queue

        if Board.use_hamming == True:
            print("Examining by Hamming distance.")
        else:
            print("Examining by Manhattan distance.")
            
        BoardTotalNumber = 1 #This is for exercise 2, set the default count as 1 since the original(unchanged) puzzle counts.
        
        heap = MinPQ()    #create a minimum heap tree
        rootNode = Node(initial, 0, None)    #initial = board, 0 moves, there is no node yet
        heap.insert(rootNode)    #insert initial node into a minimum heap tree
        while not heap.isEmpty():    #when queue is not empty
            node = heap.delMin()    #delete the minimum item in the tree
            if not node.board.solved():    #if the puzzle is not solved
                if node.previous != None:    #if there is previous node(parent node)
                    for c_board in node.board.neighbors():    #then look for its neighbors(children)
                        if c_board != node.previous.board:    #if childrens does not matches with the current node's _parent
                        #Here, children shouldn't match with its grand parents becuase we don't want the trace(tile) to go step back to the previous tile
                        #Also, comparing children with grand-parent is possible but with its parent is impossible because it's impossible to have same board as parent after when you move the tile
                            c_node = Node(c_board, node.moves+1, node)    #make neighbors boards into Nodes
                            heap.insert(c_node)    #insert children nodes(neighbor nodes) into tree
                            BoardTotalNumber += 1    #exercise 2: count 1 for every node.moves
                            
                else:    #if there is no parent node, (only a root)
                    for n_board in node.board.neighbors():    #look for its children(neighbors) right underneath the root node
                        heap.insert(Node(n_board, node.moves+1, node))    #insert into tree
                        BoardTotalNumber += 1   #exercise 2: count 1 for every node.moves
            else:    #if board is solved
                print("\n")
                print("This is a Solved puzzle ! ! !")
                print("Total number of board positions: ", BoardTotalNumber)    #for exercise 2
                print("Total number moved: ", node.moves)
                print("\n")
                while node.previous:    #if a node has parent node
                    self.__trace = [node.board] + self.__trace    #add each nodes(taces) into list trace
                    node = node.previous
                self.__trace = [node.board] + self.__trace
                self.__solvable = True

                break

    def solvable(self): ##IMPORTANT
        '''Returns True if this puzzle can be solved.'''
        return self.__solvable;

    def moves(self):
        '''Returns the number of moves in the solution, or -1 if
        not solvable.'''
        return len(self.__trace) - 1 if self.__solvable else -1

    def solution(self):  ##IMPORTANT
        '''Returns the list of board positions in the solution.'''
        return self.__trace.copy()




# Add your main program here. It should prompt for a file name, read
# the file, and create and run the Solver class to find the solution
# for the puzzle. Then it should print the result (see the example output
# file for details).
#

import os
path = os.getcwd()
puzzlefolder = path + ".\puzzles\\"
files = os.listdir(puzzlefolder)

def openFile(full_filepath):
    fp = open(full_filepath)
    lines = fp.read()
    fp.close()
    lines = lines.replace("\n", "")
    InitialBoard = Board(lines)

    SolveBoard = Solver(InitialBoard)
    solution = SolveBoard.solution()
    for i, j in enumerate(solution):
        print("Number moved: ", str(i), "\n", str(j), "\n\n")

def scanEveryFile():
    #path = os.getcwd()
    #puzzlefolder = path + ".\puzzles\\"
    #files = os.listdir(puzzlefolder)
    for file in files:
        full_filepath = puzzlefolder + file
        if ".txt" in full_filepath:
            print("\n########", file, "########") #just to distinguish which file's output it is
            openFile(full_filepath)

def scanSelectedFile():
    while True:
        x = input("Enter a file name: ")
        x = x + ".txt"
        #path = os.getcwd()
        #puzzlefolder = path + ".\puzzles\\"
        #files = os.listdir(puzzlefolder)
        for file in files:
            if x == file:
                full_filepath = puzzlefolder + file
                openFile(full_filepath)


while True:
    option = input("Type by file name(1) or scan through every file(2)? Enter 1 or 2: ")
    if not option.isdigit():
        print("Invalid number, type again.")
    else:
        option = int(option)
        if option == 1:
            scanSelectedFile()
        elif option == 2:
            scanEveryFile()
        else:
            print("Invalid number, type again.")
