# Project 2 DFS-based Topological Sorting
# starter code
# student name: Logan Bradac
# student id number: 1604464

# The small built-in DAG G1
# Use this graph to verify the correctness of your DFS-based topological sorting
import time

cs143, cs321, cs322, cs142, cs370, cs341, cs326, cs378, cs401, cs421 = range(10)

G1 = {
     cs143: [cs321, cs341, cs370, cs378],
     cs321: [cs322, cs326],
     cs322: [cs401, cs421],
     cs142: [cs143],
     cs370: [],
     cs341: [cs401],
     cs326: [cs401, cs421],
     cs378: [cs401],
     cs401: [],
     cs421: []
     }

names = []    


def openFile(fileName):

    AdjacencyList = {} # Initialize an empty dictionary for adjacency list

    OpenedFile = open(fileName, "r")  # Open the file in read mode
    
    for line in OpenedFile:
        line = line.strip()  # Remove leading and trailing white spaces
        parts = line.split() # split the head and tail nodes into a list
        headNode = int(parts[0])  # Parse head node into integer
        edges = list(map(int, parts[1:]))  # Convert edges to integers

        if headNode not in AdjacencyList:
            AdjacencyList[headNode] = []
            names.append(headNode) # Add head node to names list

        for edge in edges:
            if edge not in AdjacencyList:
                AdjacencyList[edge] = []  # Initialize the edge node if missing
                names.append(edge) # Add edge node to names list
            AdjacencyList[headNode].append(edge)  # Add edge to the head node

    OpenedFile.close()  # Close the file

    return AdjacencyList

# For project step1    
# Input
#    G as the input graph
#    s as the current vertex to be explored   
def dfs_topo(G, s, L, CurLabel, E): # You may modify the input argument list if necessary
    E.add(s) # Add each explored node into explored set
    
    for connection in (G[s]):
        if connection not in E:
            dfs_topo(G, connection, L, CurLabel, E) # Recursively call DFS until sink node is found

    L[s] = CurLabel[0] # assign label to next found sink node
    CurLabel[0] -= 1 # decrement label to next highest label

    return

# For project step1
# Input
#    G as the input graph
# Output
#    L as the Python list to record the ordering of vertices. Example L[0] = 5 means node 0 is assigned topo sort number 5
def topo_sort(G): # you CANNOT change the input argument list
    start_time = time.time() # Start time for performance comparison
    L = [-1]*(max(G.keys()) + 1)
    E = set() # Explored set for explored nodes

    CurLabel = [len(G)]  # List to allow updates
    for vertex in G.keys():
        if vertex not in E: # if the node is not in the explored set, call for DFS
            dfs_topo(G, vertex, L, CurLabel, E) # Call for DFS on node
    end_time = time.time() # End time for performance comparison
    run_time = end_time - start_time
    print("DFS based sorting run time: {:.3f} seconds".format(run_time)) # Print runtime for comparison with 6 decimal places
    return L

# I. This is the provided function for induction-based topological 
# sorting. You need to call this function and compare with your 
# DFS-based topological sorting for performance     
# II. DO NOT change any part of this function
# III. This function destroys the input graph G because it 
# removes one node in every iteration. During performance comparison, 
# if you call this function before topo_sort(), you need to make a 
# deep copy of your graph G and pass that copy to topo_sort() 
def ind_topo(G):
    startTime = time.time()
    count = dict((u, 0) for u in G) # in-degree of each node
    for u in G:
        for v in G[u]:
            count[v] += 1

    L = [0]*len(G) # a list to record the ordering of all nodes
    k = 1 # topo order's value starts from 1 in induction-based method
    while G:
        for u in G:
            if count[u]==0: break # break after finding a source node
        L[u] = k # assign a topo order value to this node
        k += 1
        for v in G[u]:
            count[v] -= 1
        G.pop(u) # remove this source node and its outgoing edges from G

    endTime = time.time()
    totalTime = endTime - startTime
    print("Induction based sorting run time: {:.3f} seconds".format(totalTime)) # Print runtime for comparison with 10 decimal places

    return L

if __name__=="__main__": # main program
    # Section 1: for project step 2, verify the correctness of your topo_sort() functions
    #     no need to change this section, just verify the correctness of the printout
    fileToRead = "C:/Users/brada/projects/helloworld/Data Structures/TopoSort/DAG2.txt" # change the file name to test other graphs (should only need to change DAG number)
    File1 = openFile(fileToRead)
    File1Copy = File1.copy()

    topo_order = topo_sort(File1)
    solo = ind_topo(File1Copy)

    print({names[x]: topo_order[x] for x in range(len(topo_order))})
    print("\n")
    print("\n")
    print("\n")
    print("\n")
    print({names[x]: solo[x] for x in range(len(solo))})

    
    # Section 2: for project step3, performance comparison
    #   load each graph from DAG1.txt-DAG5.txt
    #   store each graph in memory using the format of G1
    #     Hint: you may need Python's built-in open()/close() function, and some file operations like readline() 
    #   call your topo_sort and the provided ind_topo by passing each graph as the input to obtain the execution time (in milliseconds) 
    # 
    # Complete the code for performance comparison here    