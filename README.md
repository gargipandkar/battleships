# battleships
10.008 Digital World Final Assignment

Battleships is a 2-player paper-and-pen guessing game originally published by the Milton Bradley Company in 1943. Each player uses two square grids: one to place one's own ships (placement grid) and one to record the shots fired at the opponent (target grid). Ships of various sizes have to be placed by each player according to the rules as detailed below. After the initial placement phase, players alternate in shooting at enemy ships. 

The objective of the game is to sink all enemy ships before one’s own ships are sunk.

This is a scaled-down variation which uses 5 by 5 square grids and a fleet composed of a 2-unit cruiser, a 2-unit destroyer and a 1-unit submarine. The grids are labeled with rows from A to E and columns from 1 to 5 thus a coordinate must specify an alphabet-integer pair.

The placement rules are as follows:
  1. Ships must be placed horizontally or vertically.  
  2. Ships cannot be overlapped.  
  3. Ships cannot share any edges; touching corners are accepted.  

After each turn, both players are informed whether the shot was a "hit" or a "miss" and which ship, if any, has been sunk. This information is reflected on the target grid by the symbols:
  1. \* for locations not yet attacked  
  2. w for "miss"  
  3. X for "hit"  

This version is designed to be a 1-player game against an algorithm. The algoritm is state-machine with a "hunt" mode and a "target" mode. In the "hunt" mode, it shoots at random locations with odd (or even) parity. Once a ship is hit, it switches to "target" mode in which it searches at all surrounding locations. It returns to "hunt" mode when that ship has been sunk.

Video demo can be found [here](https://sutdapac-my.sharepoint.com/:v:/g/personal/gargi_pandkar_mymail_sutd_edu_sg/EZunIzsgDhFJkJsl3ZD4-QAB8EWuflBFysuWurQa5wJs0A?e=Jxm2oR).

References:  
https://paulvanderlaken.com/2019/01/21/beating-battleships-with-algorithms-and-ai/
http://www.datagenetics.com/blog/december32011/

