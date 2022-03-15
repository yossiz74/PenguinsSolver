# PenguinsSolver
This is a tool for solving the Penguins game introduced in Skillz 2022

## Penguins Game Description
The game consist of a 5x5 board with at least one waterhole and at least one penguin
The goal is to bring all penguins to the water, which they dive into.
The board may also include polar bears.
Movement is done by sliding either a penguin or a bear in a direction of another penguin or bear, which serves as a stopping point.
It's not possible to slide to the edge of the board.

## About the solver
The solver allows placing elements on the board, and then computes a solution.
Currently it attempts to find the shortest solution (minimal number of steps).
This is done by straightforward traversing a depth-first search tree, with little optimization.
Once a solution is found, the user can view it on the board, step by step.
