# Maze Traversal Demo using BFS, DFS, and A-Star

This program is a visual demonstration using Tkinter in Python to illustrate three different traversal algorithms: Breadth-First Search (BFS), Depth-First Search (DFS), and A-Star. It uses a customizable maze with walls represented by "1" and open spaces represented by "0". The maze can have cycles and requires a valid start and end point to be specified.

## Technologies

This project was built using:

- Python 3.5 or higher
- Tkinter module for Python

## System Requirements

This program should work on any system that has Python 3.5 or higher installed.

## Installation

1. Clone or download the repository to your local machine.
2. Install the Tkinter module if it is not already installed on your system.

## Usage

1. Open the terminal or command prompt and navigate to the directory where the program is located.
2. Run the program using the command `python maze_traversal.py`.
3. The program will display a window with the maze and a menu to select the algorithm to use.
4. Select an algorithm from the menu and click "Start" to begin the traversal.
5. The program will show the traversal path and the number of steps taken to reach the end point.

## Known Issues and Limitations

- The layout of the maze is currently customizable by editing the code, but there is no external editor provided with the program.
- Users cannot change how the algorithm determines tie-breakers when there are more than one node that can be traversed to at any point, or which direction to prioritize.
- There is currently no way to change the start and end points in the GUI.

## Contributing

If you encounter any issues or have any suggestions for improving the program, please submit an issue or pull request on the GitHub repository.
