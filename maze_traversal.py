
'''
CS 5002 - Final Project

Maze Traversal using BFS and DFS

GILL, JagJeevin
HUI, Macarious Kin Fung
Pan, Yuchen
Wang, Judy
'''

import tkinter as tk
from tkinter import ttk


CELL_SIZE = 30 # for animation
HEADING_FONT = ('Arial', 16, 'underline')
INFO_FONT = ('Arial', 11)
ANIMATION_INTERVAL = 100 # milliseconds
COLOUR = {
    'wall' : 'black',
    'empty' : 'white',
    'start' : 'blue1',
    'end' : 'red1',
    'path_bfs' : 'green1',
    'path_dfs' : 'purple1',
    }  


class Node:
    def __init__(self, position, parent):
        '''
        Function Name: __init__
            Constructor for Node class
        
        Parameters:
            position -- tuple, current coordinates
            parent -- Node, parent of current node
        '''
        self.position = position
        self.parent = parent


class Application:
    '''
    The 'Application' class builds a user-defined maze, solves it, and
    displays the results graphically
    '''
    def __init__(self, master, maze, start, end):
        '''
        Method Name: __init__
            Constructor for 'Application' class
        
        Parameters:
            master -- root of application window
            maze -- 2D array, represents the maze
            start -- tuple, start coordinates
            end -- tuple, end coordintes
        
        Raises:
            Nothing
        
        Returns:
            None
        '''
        self.master = master
        self.maze = maze
        self.start = start
        self.end = end
        self.bfs_counter = 0
        self.dfs_counter = 0
        self.bfs_path = []
        self.dfs_path = []


    def build_window(self):
        '''
        Function Name: build_window
            Build the application window for a graphical user interface
        
        Parameters:
            Nothing
        
        Raises:
            Nothing
        
        Returns:
            None
        '''
        # Set title of window
        self.master.title('CS 5002 - Maze Traversal')

        # Set size of window
        width = len(self.maze[0]) * CELL_SIZE
        height = len(self.maze) * CELL_SIZE

        # Create labels for displaying headers
        self.label_bfs = ttk.Label(self.master, anchor = 'center', text = 'Breadth-First Search', font = HEADING_FONT)
        self.label_bfs.grid(column = 0, row = 0, sticky = 'nsew', padx = 20, pady = 5)
        self.label_dfs = ttk.Label(self.master, anchor = 'center', text = 'Depth-First Search', font = HEADING_FONT)
        self.label_dfs.grid(column = 1, row = 0, sticky = 'nsew', padx = 20, pady = 5)

        # Create two canvas widgets to draw maze
        self.canvas_bfs = tk.Canvas(self.master, width = width, height = height)
        self.canvas_bfs.grid(column = 0, row = 1, sticky = 'nsew', padx = 20, pady = 5)
        self.canvas_dfs = tk.Canvas(self.master, width = width, height = height)
        self.canvas_dfs.grid(column = 1, row = 1, sticky = 'nsew', padx = 20, pady = 5)

        # Draw maze in both canvases:
        self.draw_maze(self.canvas_bfs)
        self.draw_maze(self.canvas_dfs)

        # Create buttons
        self.button_bfs = ttk.Button(self.master, text = 'Start BFS', command = self.start_bfs)
        self.button_bfs.grid(column = 0, row = 2, sticky = 'nsew', padx = 70, pady = 0)
        self.button_dfs = ttk.Button(self.master, text = 'Start DFS', command = self.start_dfs)
        self.button_dfs.grid(column = 1, row = 2, sticky = 'nsew', padx = 70, pady = 0)

        # Create labels for displaing results
        self.frame_bfs_results = ttk.LabelFrame(self.master, text = 'BFS Results', labelanchor = 'nw', relief = 'solid')
        self.frame_bfs_results.grid(column = 0, row = 3, sticky = 'nsew', padx = 20, pady = 5)
        self.label_bfs_results = ttk.Label(self.frame_bfs_results, anchor = 'nw', text = '', font = INFO_FONT, wraplength = len(self.maze[0]) * CELL_SIZE - 50)
        self.label_bfs_results.pack(expand = True, fill = 'both', padx = 20, pady = 5)

        self.frame_dfs_results = ttk.LabelFrame(self.master, text = 'DFS Results', labelanchor = 'nw', relief = 'solid')
        self.frame_dfs_results.grid(column = 1, row = 3, sticky = 'nsew', padx = 20, pady = 5)
        self.label_dfs_results = ttk.Label(self.frame_dfs_results, anchor = 'nw', text = '', font = INFO_FONT, wraplength = len(self.maze[0]) * CELL_SIZE - 50)
        self.label_dfs_results.pack(expand = True, fill = 'both', padx = 20, pady = 5)

        self.update_text()


    def start_bfs(self):
        '''
        Function Name: start_bfs
            Starts the breadth-first search algorithm to traverse a maze
        
        Parameters:
            Nothing
        
        Raises:
            Nothing
        
        Returns:
            list of tuples, list of positions to traverse from start to end
        '''
        self.bfs_counter = 0
        self.bfs_path = []
        self.draw_maze(self.canvas_bfs)
        start_node = Node(self.start, None)
        queue = [start_node] # Use queue as data structure
        visited = set() # Create a set of visited nodes

        while len(queue) > 0: # Keep searching until queue is empty

            current_node = queue.pop(0)
            if current_node.position not in visited:

                # Update info in application window
                self.bfs_counter += 1
                self.draw_path_circle(current_node, self.canvas_bfs, COLOUR['path_bfs'])
                self.wait(ANIMATION_INTERVAL)
                self.update_text()
                # self.refresh_path_circle_bfs(current_node)

                visited.add(current_node.position)

                if current_node.position == self.end:
                    path = [] # Find path by seeking through all parents node
                    while current_node is not None:
                        path.append(current_node.position)
                        current_node = current_node.parent

                    self.bfs_path = path[::-1] # Reverse the list of nodes
                    self.draw_path_all(path, self.canvas_bfs, COLOUR['path_bfs'])
                    self.update_text()
                    return path

                # From current cell, traverse to all possible nodes (W, S, E, N)
                for row_change, column_change in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                    new_row = current_node.position[0] + row_change
                    new_column = current_node.position[1] + column_change

                    # Check if adjacent cell is a valid path (not a wall or out of range)
                    if (
                        (0 <= new_row < len(self.maze)) and (0 <= new_column < len(self.maze[0])) and
                        (self.maze[new_row][new_column] != 1) and ((new_row, new_column) not in visited)
                        ):
                        # Set current node as parent and add current node to queue
                        queue.append(Node((new_row, new_column), current_node))

        self.bfs_path = 'FFS: no solution found'
        self.update_text()


    def start_dfs(self):
        '''
        Function Name: start_dfs
            Starts the depth-first search algorithm to traverse a maze
        
        Parameters:
            Nothing
        
        Raises:
            Nothing
        
        Returns:
            list of tuples, list of positions to traverse from start to end
        '''
        self.dfs_counter = 0
        self.dfs_path = []
        self.draw_maze(self.canvas_dfs)
        start_node = Node(self.start, None)
        stack = [start_node] # Use stack as data structure
        visited = set() # Create a set of visited nodes

        while len(stack) > 0: # Keep searching until stack is empty

            current_node = stack.pop(-1)

            # Update info in application window
            self.dfs_counter += 1
            self.draw_path_circle(current_node, self.canvas_dfs, COLOUR['path_dfs'])
            self.wait(ANIMATION_INTERVAL)
            self.update_text()
            # self.refresh_path_circle_dfs(current_node)

            visited.add(current_node.position)

            if current_node.position == self.end:
                path = [] # Find path by seeking through all parents node
                while current_node is not None:
                    path.append(current_node.position)
                    current_node = current_node.parent

                self.dfs_path = path[::-1] # Reverse the list of nodes
                self.draw_path_all(path, self.canvas_dfs, COLOUR['path_dfs'])
                self.update_text()
                return path

            # From current cell, traverse to all possible nodes (W, S, E, N)
            for row_change, column_change in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                new_row = current_node.position[0] + row_change
                new_column = current_node.position[1] + column_change

                # Check if adjacent cell is a valid path (not a wall or out of range)
                if (
                    (0 <= new_row < len(self.maze)) and (0 <= new_column < len(self.maze[0])) and
                    (self.maze[new_row][new_column] != 1) and ((new_row, new_column) not in visited)
                    ):
                    # Set current node as parent and add current node to stack
                    stack.append(Node((new_row, new_column), current_node))

        self.dfs_path = 'DFS: no solution found'
        self.update_text()

    
    def draw_maze(self, canvas):
        '''
        Function Name: draw_maze
            Draw the maze on the canvas widget
        
        Parameters:
            canvas -- Canvas, widget in tkinter, used for drawing shapes
        
        Raises:
            Nothing
        
        Returns:
            None
        '''
        # Iterate through all cells in maze
        for row in range(len(self.maze)):
            for column in range(len(self.maze[0])):
                if self.maze[row][column] == 1: # Cell is a wall
                    canvas.create_rectangle(
                        column * CELL_SIZE,
                        row * CELL_SIZE,
                        column * CELL_SIZE + CELL_SIZE,
                        row * CELL_SIZE + CELL_SIZE,
                        fill = COLOUR['wall']
                    )
                else:
                    canvas.create_rectangle(
                        column * CELL_SIZE,
                        row * CELL_SIZE,
                        column * CELL_SIZE + CELL_SIZE,
                        row * CELL_SIZE + CELL_SIZE,
                        fill = COLOUR['empty']
                    )


    def draw_path_circle(self, current_node, canvas, colour):
        '''
        Function Name: draw_path_circle
            Draws a small circle in an empty cell
        
        Parameters:
            current_node -- Node, represents a node with position and parent
            canvas -- Canvas, widget in tkinter, used for drawing shapes
            colour -- str, colour used to draw the path
        
        Raises:
            Nothing
        
        Returns:
            None
        '''
        row, column = current_node.position
        canvas.create_oval(
                    column * CELL_SIZE + 0.25 * CELL_SIZE,
                    row * CELL_SIZE + 0.25 * CELL_SIZE,
                    column * CELL_SIZE + 0.75 *CELL_SIZE,
                    row * CELL_SIZE + 0.75 *CELL_SIZE,
                    fill = colour
        )


    def draw_path_all(self, path, canvas, colour):
        '''
        Function Name: draw_path_all
            Draws the entire path solution on canvas
        
        Parameters:
            path -- list of tuples, list of positions from start to finish
            canvas -- Canvas, widget in tkinter, used for drawing shapes
            colour -- str, colour used to draw the path
        
        Raises:
            Nothing
        
        Returns:
            None
        '''
        # Plot solution path
        for row, column in path:
            canvas.create_rectangle(
            column * CELL_SIZE,
            row * CELL_SIZE,
            column * CELL_SIZE + CELL_SIZE,
            row * CELL_SIZE + CELL_SIZE,
            fill = colour
        )

        # Plot start coordinates
        row, column = path[0]
        canvas.create_rectangle(
            column * CELL_SIZE,
            row * CELL_SIZE,
            column * CELL_SIZE + CELL_SIZE,
            row * CELL_SIZE + CELL_SIZE,
            fill = COLOUR['start']
        )

        # Plot start coordinates
        row, column = path[-1]
        canvas.create_rectangle(
            column * CELL_SIZE,
            row * CELL_SIZE,
            column * CELL_SIZE + CELL_SIZE,
            row * CELL_SIZE + CELL_SIZE,
            fill = COLOUR['end']
        )


    def update_text(self):
        '''
        Function Name: update_text
            Updates the message window with search results
        
        Parameters:
            Nothing
        
        Raises:
            Nothing
        
        Returns:
            None
        '''
        text_bfs = (
            f"Steps:\t{self.bfs_counter}\n"
            f"Length:\t{len(self.bfs_path)}\n"
            f"Path:\t{str(self.bfs_path)[1 : -1]}\n"
        )
        self.label_bfs_results.config(text = text_bfs)

        text_dfs = (
            f"Steps:\t{self.dfs_counter}\n"
            f"Length:\t{len(self.dfs_path)}\n"
            f"Path:\t{str(self.dfs_path)[1 : -1]}\n"
        )
        self.label_dfs_results.config(text = text_dfs)


    def wait(self, time):
        '''
        Function Name: wait
            Pauses the event for a specific time in milliseconds
        
        Parameters:
            time -- int, in milliseconds
        
        Raises:
            Nothing
        
        Returns:
            None
        '''
        var = tk.IntVar()
        self.master.after(time, var.set, 1)
        self.master.wait_variable(var)


def main():
    # 1 is wall; 0 is empty
    maze = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1],
        [1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]
    '''
    Example 1:
    ----------
    Start and end are far away
    BFS - more steps, shorter path
    DFS - less steps, longer path
    '''
    start = (10, 1)
    end = (1, 10)

    '''
    Example 2:
    ----------
    Start and end are close together
    BFS - less steps, shorter path
    DFS - more steps, longer path
    '''
    # start = (3, 8)
    # end = (8, 3)
    
    master = tk.Tk()
    application = Application(master, maze, start, end)
    application.build_window()
    master.mainloop()

if __name__ == '__main__':
    main()


    
