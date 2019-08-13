# Instructions

This program simulates a tournement with four categories of games.  Players are randomly matched with eachother to play in scrums of 4 in either 2v2 or FFA games.  
If scrums of 4 cannot be formed, matchmaking will assign a bye to leftover players.  Players with the least byes have priority selection for bye assignment. Players are
otherwise assigned to play in their least played category, assuring broad distribution.

Two primary data sets are created.  `players`, and `scrums`.  

`players` stores all information relating to a single participant in the structure `[['Name'],[[Points r1],[Points r2]...],[[Lawn Games Played],[Bar Games Played]...]]`
`scrums` divides the players into the 5 possible categories of games `[[Players in Lawn],[Players in Bar],[Players in Board],[Players in Video],[Players in Bye]]`

The user selects an operation to carry out on the data sets.  The datasets are passed to these functions, modified, and returned.  The available operations are below:

`M`odify roster - Add or remove players from the sitting out list.  These players will be ignored by matchmaking and recieve a bye for the round. 
`P`erform matchmaking - Create scrums of 4 and assign them to a category of game.  Leftover players receive a bye
`A`ward points - Select a game to resolve and assign points to the winner.
`G`et new games - Reselect the game sets if they are not satisfactory.  Does not change teams.
`E`nd the round - Move on to the next round when all points have been awarded.
`D`isplay player stats - Display the name, scores, and game history for each player
`O`verwrite player score - Edit a players score through the current round
`R`estore game to previous round - Revert the game to a previous round.

At the end of the desired number of rounds, the game ends and a champion is chosen

# How to run

Matt how do I run this thing
