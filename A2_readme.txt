MinMax :
#Takes way too long I only ran on smaller instances (smaller branching factor) for testing..
Depth = 3
**Number of nodes expanded supposed to  = 288^3
But without any rotations = 36^3




Depth = 5
**Number of nodes expanded = 288^5
But without any rotations = 36^5




Time complexity = O(b^m)
Best case space complexity (DLS) = O (bm)




MinMax with Alpha Beta Pruning :
Depth = 3
#Number of nodes expanded= 4687


Worst case if no pruning is done the running time is still b^d = 288^3
I reorder the children in descending to prune as much as possible, best case the running time will be:
        O (sqrt(b^d)) =  O (Sqrt(288^3)) 


Space complexity (DLS) = O (bm)


Depth = 4
#Number of nodes expanded=  78400
Worst case if no pruning is done the running time is b^d = 288^4


I attempt to reorder the children to prune as much as possible, best case the running time will be:
        O (sqrt(b^d)) =  O (Sqrt(288^4)) = 78400
        


**This is not exact since the branching factor of first level is 288, the second is 272, the third 264 and so on… 
















For extra Credit:
        1- I implemented a more sophisticated utility function that take in consideration both the winning and losing chances instead of just counting a streak.


        2- The closer the AI is to winning the higher the utility will be to encourage smarter moves.
         
        3- The winning node utility value is 1000 so the AI will always make that move.


        4- I implemented blocking.


        5-  I reorder the children in descending to optimize pruning.


Lastly, the lookahead start with 2 since the very early moves are not that significant and the branching factor is high.  I  increase the depth by one every three pair of moves since the branching factor decrease and lookahead becomes more critical as the game progress.