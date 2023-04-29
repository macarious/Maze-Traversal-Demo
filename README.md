# Maze Traversal Demo<br>(comparing BFS, DFS, and A*)

## 1. About/Overview

This program is a visual demonstration using Tkinter in Python to illustrate three different traversal algorithms: Breadth-First Search (BFS), Depth-First Search (DFS), and A-Star (A*). It uses a customizable maze with walls represented by "1" and open spaces represented by "0". The maze can have cycles and requires a valid start and end point to be specified. Along with finding a valid path, the program also counts the number of steps taken and the total length of the valid path.

__BFS (Breadth-First Search)__ is a method for exploring a graph or tree in a breadth-first manner. In the context of maze traversal, BFS can be used to find the shortest path from the start point to the end point. The algorithm starts at the starting point and explores all of its neighbouring cells first, then moves to the next level of neighbouring cells, and so on, until it reaches the end point.

__DFS (Depth-First Search)__ is a method for exploring a graph or tree in a depth-first manner. In the context of maze traversal, DFS can be used to find any path from the start point to the end point. The algorithm starts at the starting point and explores as far as possible along each branch before backtracking. When the end point is found, the algorithm stops.

__A* (A-star)__ is a more sophisticated algorithm that uses heuristic information to guide the search. It is commonly used to find the shortest path in a graph or tree. In the context of maze traversal, A* can be used to find the shortest path from the start point to the end point. The algorithm uses a combination of the actual cost to reach the current node (the "g" value) and an estimated cost to reach the end point (the "h" value) to evaluate the best path to take. The Manhattan distance, which measures the distance between two points in a grid-like pattern, is used as the heuristic for the "h" value in A* when traversing mazes in the program. The algorithm starts at the starting point and explores the neighbouring cells with the lowest combined cost until it reaches the end point.

![Progarm Overview](https://github.com/macarious/Maze-Traversal-Demo/blob/main/screenshots/04-all-traversal.png "Program Overview")
<br>

## 2. Technologies

This project was built using:

- Python 3.5 or higher
- Tkinter module for Python

## 3. System Requirements

This program should work on any system that has Python 3.5 or higher installed.

## 4. Installation

1. Clone or download the repository to your local machine.
2. Install the Tkinter module if it is not already installed on your system.

## 5. Usage

1. Open the terminal or command prompt and navigate to the directory where the program is located.
2. The layout of the maze can be directly edited in 'main()'. The walls of the maze is represented by the integer '1' while the empty traversable tiles is represented by the integer '0'. Here is an example:

![Maze Editor](https://github.com/macarious/Maze-Traversal-Demo/blob/main/screenshots/01-maze-editor.png "Maze Editor")
<br>

3. Run the program using the command `python maze_traversal.py`.
4. The program will display a window with the maze and a button for each of the algorithm to use.
5. The program will show the traversal path, the number of steps taken, and the total length of the path to reach the end point.

## 6. Known Issues and Limitations

- The layout of the maze is currently customizable by editing the code, but there is no external editor provided with the program.
- Users cannot change how the algorithm determines tie-breakers when there are more than one node that can be traversed to at any point, or which direction to prioritize.
- There is currently no way to change the start and end points in the GUI.

## 7. Takeaway from Demo

In summary, when solving a maze, we have two common algorithms to choose from - BFS and DFS. BFS guarantees the shortest path but can be slower due to exploring many unnecessary nodes. DFS, on the other hand, may be faster, but it does not guarantee the shortest path and may get stuck in an infinite loop. Pre-order DFS is a sensible approach for solving mazes when we only know the starting point and need to find adjacent cells. However, the limitations of the research include the number of tested mazes, which could be addressed in future studies. While BFS is always optimal and complete, it can be slow. Therefore, more efficient methods like A* can be considered.

## 8. Contributing

If you encounter any issues or have any suggestions for improving the program, please submit an issue or pull request on the GitHub repository.
