# 2048
2048 solver using expectiminimax algorithm with alpha-beta pruning

# Game
2048 is played on a 4x4 grid with numbered tiles which can slide up, down, left, or right. This game can be
modeled as a two player game, in which the computer AI generates a 2- or 4-tile placed randomly on the board,
and the player then selects a direction to move the tiles. The tiles move until they either (1) collide with
another tile, or (2) collide with the edge of the grid. If two tiles of the same number collide in a move, they merge
into a single tile valued at the sum of the two originals. The resulting tile cannot merge with another tile again in
the same move.

# Goal
An adversarial search agent to play the 2048-puzzle game. The Player AI is allowed 0.2 seconds to come up with each move. The
process continues until the game is over; that is, until no further legal moves can be made. At the end of the game,
the maximum tile value on the board is displayed.

## Implementation
Implemented the **expectiminimax** algorithm for adversarial search (a variation of Minimax algorithm). Note that 90% of tiles placed by the computer are 2’s, while the remaining 10% are 4’s.  
![expectiminimax sample](/images/expectiminimax.png)  
**Alpha-beta pruning** which should speed up the search process by eliminating irrelevant branches.  
**Heuristic functions and weights:** After trying many different hueristics and weights I found a combination of two to be the most useful: Weight Matrix (snake shaped) to converge the tiles to one corner of the grid, and Empty Tile with high weights to support merging. Explenation for heuristics can be found [here](http://cs229.stanford.edu/proj2016/report/NieHouAn-AIPlays2048-report.pdf). I also found that constantly eliminating moves in one direction, unless no other move is possible, reduced branches and increased end goal value.  

### To execute 
**run** ```$ python3 GameManager.py```

