# Gess-Puzzle
CS162 (Intro to Computer science II) - Final Project - Gess Puzzle

# Overview
- Gess is a chess/Go variant created by the Puzzles and Games Ring of the Archimedeans Mathematics Society from Cambridge University. For the project, the puzzle is implemented in Puzzle, and is played through the console/terminal.


# How to Play & Rules
## Setup
- the game begins with a 18x18 grid with two players (white and black)
- each player begins with 43 stones
- players take turns to move, with black starting by default

## Player Moves
- a piece is a 3x3 group of stones, where all colors must be the same
- a piece may move in a specific direction up to three squares, if there is a stone in that direction
- otherwise, if a piece has a 'center' stone, it may move any amount of squares in any direction until overlapping another stone
- each player can only move a piece of his/her color

## How to Win / Constraints
- each player begins with a 'ring' - that is, a 3x3 piece all with stones except the center
- a player's move would be considered invalid if the ring is broken
- if the player's ring is broken by the opposing player, then the opposing player wins

# Screenshot
- starting board

![image](https://github.com/kuckikirukia/Gess-Puzzle/blob/main/images/sample1.png)

# Sources
- [Chess Variants](https://www.chessvariants.com/crossover.dir/gess.html)

# Author
- [Daniel Yu](https://github.com/kuckikirukia)
