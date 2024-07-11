# doublecrossed

This is a small AI to play the game "Dots and Boxes". If you do not know the game check out it's Wikipedia (https://en.wikipedia.org/wiki/Dots_and_boxes).

The aim of the game is to complete as many boxes as you can, and the AI tries to play as optimally as it can to win - however it's not perfect especially on bigger boards. The way it does this is with various game theory approaches, and I aim to also train a machine learning model to compete against this model in the future.

This game is solved (https://en.wikipedia.org/wiki/Solved_game) for games upto size 4x5 (in dots). For a 4x4 game, the second player always wins assuming optimal play and for a 4x5 game it's always a draw. However, it is still unknown for larger board sizes and so to make a bot we have to use models which have the possibility of losing.

All of this information can be found in the links I provide below (and probably explained a bit better there too). 

Essentially, the main rule you have to keep in mind whilst playing is the "long chain rule":
### If you are player 1, you want the number of dots on the board + the number of long chains to be even, if you are player 2 you want this to be odd.
Note: a long chain is a chain of length 3+

The algorithm essentially revolves around this rule: playing and looking ahead to try and find a set of moves which forces the number of chains to be whatever it wants. 
If it cant look ahead that far/ or is in the endgame, then it uses a minimax algorithm to try and find the best sequence of moves.

The code is fully commented and explained as well.

https://www.youtube.com/watch?v=KboGyIilP6k&t=206s
https://www.youtube.com/watch?v=rBngUo0JTzs
Solving Dots and Boxes - scientific paper
Book: The dots and boxes game by Berlekamp
