# WordBrain Solver

WordBrain is a word search style game where you are given a 2D grid of letters and a set of words to find that use all the letters.
The player does not know what words are used to create the board, only the lengths of the words.
When a player finds a word, those tiles disappear and the tiles above them fall down.
The player is trying to use up all the tiles to make words.

This program takes as input the game board and the lengths of the words to find.
Optionally, if the player knows any of the words in the puzzle, they can provide them as well.
The program will take this data and use an exhaustive search to find possible solutions.
As it finds possible solutions, it will print them to the console.

This program uses an english word list of 370,105 words that it searches for in the puzzle.
It may take a while to run the program due to the size of the word list.
A smaller word list would run significantly faster, but also comes at the cost of not having some of the answer words in that list.