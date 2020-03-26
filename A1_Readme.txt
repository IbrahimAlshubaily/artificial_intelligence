initial state configuration 1 ( "123456789ABC DEF" ):
 ['1' '2' '3' '4']
 ['5' '6' '7' '8']
 ['9' 'A' 'B' 'C']
 [' ' 'D' 'E' 'F']


BFS:
                3 16 7 10


        DFS: 
                3 6 3 4


        GBFS - h1:
                3 6 3 4


        GBFS - h2:
                3 6 3 4


        AStar - h1:
                3 8 4 5
        
        AStar - h2:
                3 6 3 4


        DLS - depth = 2:
                -1 0 0 0


DLS - depth = 3:
        3 6 3 4
___________________________________________


initial state configuration 2 ( "123456789ABC DEF" ):
 ['1' '2' '3'  ' ']
 ['5' '6' '7' '4']
 ['9' 'A' 'B' '8']
 ['D' 'E' 'F' 'C']


BFS:
3 16 7 10


DFS: 
        3 6 3 4


GBFS - h1:
        3 6 3 4


GBFS - h2:
        3 6 3 4


AStar - h1: (does better for this config)
        3 6 3 4
        
AStar - h2:
        3 6 3 4


DLS - depth = 2:
        -1 0 0 0


DLS - depth = 3:
3 6 3 4


___________________________________________



initial state configuration 2 ( "123456789ABC DEF" ):
 [' ' '1' '2' '3']
 ['5' '6' '7' '4']
 ['9' 'A' 'B' '8']
 ['D' 'E' 'F' 'C']


BFS:
6 201 95 107




DFS: 
        6 11 6 6




GBFS - h1:
        6 11 6 6



GBFS - h2:
        6 11 6 6


AStar - h1: 
        6 11 6 6
        
AStar - h2:
        3 6 3 4


DLS - depth = 5:
        -1 0 0 0


DLS - depth = 6:
3 6 3 4

___________________________________________


Time Complexity:



V = the number of nodes we visit.



BFS:
O (V)


DFS: 
O(V)


DLS:
O(V)




M = maximum fringe size.




GBFS:
        O(M)


AStar:
        O(M)