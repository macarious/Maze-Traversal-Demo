
'''
CS 5002 - Final Project

Maze Traversal using BFS and DFS

GILL, JagJeevin
HUI, Macarious Kin Fung
PAN, Yuchen
WANG, Judy
'''

from queue import PriorityQueue
import tkinter as tk
from tkinter import ttk


CELL_SIZE = 30 # for animation
ANIMATION_INTERVAL = 40 # milliseconds
FONT = {
    'heading' : ('Arial', 16, 'underline'),
    'info box' : ('Arial', 11),
    'cell' : ('Arial', 8, 'bold'),
}
COLOUR = {
    'wall' : 'black',
    'empty' : 'white',
    'start' : 'green1',
    'end' : 'red1',
    'path_bfs' : 'yellow1',
    'path_dfs' : 'purple1',
    'path_astar' : 'orange1',
    'font' : 'black',
}  


class Node:
    def __init__(self, position, parent, g = 0, h = 0):
        '''
        Function Name: __init__
            Constructor for Node class
        
        Parameters:
            position -- tuple, current coordinates
            parent -- Node, parent of current node
            g -- numeral, distance from start to new node, used in A*
            h -- numeral, heuristc, used in A*

        Returns:
            None
        '''
        self.position = position
        self.parent = parent
        self.g = g
        self.h = h


    def __eq__(self, other):
        '''
        Function Name: __init__
            Compares two Node objects

        Returns:
            bool, True if cost of left Node is equal the cost of right Node;
                False otherwise
        '''
        return (self.g + self.h) == (other.g + other.h)


    def __lt__(self, other):
        '''
        Function Name: __init__
            Compares two Node objects

        Returns:
            bool, True if cost of left Node is less than the cost of right Node;
                False otherwise
        '''
        return (self.g + self.h) < (other.g + other.h)


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
        self.astar_counter = 0
        self.bfs_path = []
        self.dfs_path = []
        self.astar_path = []


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
        self.label_bfs = ttk.Label(self.master, anchor = 'center', text = 'Breadth First Search', font = FONT['heading'])
        self.label_bfs.grid(column = 0, row = 0, sticky = 'nsew', padx = 20, pady = 5)
        self.label_dfs = ttk.Label(self.master, anchor = 'center', text = 'Depth First Search', font = FONT['heading'])
        self.label_dfs.grid(column = 1, row = 0, sticky = 'nsew', padx = 20, pady = 5)
        self.label_astar = ttk.Label(self.master, anchor = 'center', text = 'A* Search', font = FONT['heading'])
        self.label_astar.grid(column = 2, row = 0, sticky = 'nsew', padx = 20, pady = 5)

        # Create two canvas widgets to draw maze
        self.canvas_bfs = tk.Canvas(self.master, width = width, height = height)
        self.canvas_bfs.grid(column = 0, row = 1, sticky = 'nsew', padx = 20, pady = 5)
        self.canvas_dfs = tk.Canvas(self.master, width = width, height = height)
        self.canvas_dfs.grid(column = 1, row = 1, sticky = 'nsew', padx = 20, pady = 5)
        self.canvas_astar = tk.Canvas(self.master, width = width, height = height)
        self.canvas_astar.grid(column = 2, row = 1, sticky = 'nsew', padx = 20, pady = 5)

        # Draw maze in both canvases:
        self.draw_maze(self.canvas_bfs)
        self.draw_maze(self.canvas_dfs)
        self.draw_maze(self.canvas_astar)

        # Create buttons
        self.button_bfs = ttk.Button(self.master, text = 'Start BFS', command = self.start_bfs)
        self.button_bfs.grid(column = 0, row = 2, sticky = 'nsew', padx = 70, pady = 0)
        self.button_dfs = ttk.Button(self.master, text = 'Start DFS', command = self.start_dfs)
        self.button_dfs.grid(column = 1, row = 2, sticky = 'nsew', padx = 70, pady = 0)
        self.button_astar = ttk.Button(self.master, text = 'Start A*', command = self.start_astar)
        self.button_astar.grid(column = 2, row = 2, sticky = 'nsew', padx = 70, pady = 0)

        # Create labels for displaing results
        self.frame_bfs_results = ttk.LabelFrame(self.master, text = 'BFS Results', labelanchor = 'nw', relief = 'solid')
        self.frame_bfs_results.grid(column = 0, row = 3, sticky = 'nsew', padx = 20, pady = 5)
        self.label_bfs_results = ttk.Label(self.frame_bfs_results, anchor = 'nw', text = '', font = FONT['info box'], wraplength = len(self.maze[0]) * CELL_SIZE - 50)
        self.label_bfs_results.pack(expand = True, fill = 'both', padx = 20, pady = 5)

        self.frame_dfs_results = ttk.LabelFrame(self.master, text = 'DFS Results', labelanchor = 'nw', relief = 'solid')
        self.frame_dfs_results.grid(column = 1, row = 3, sticky = 'nsew', padx = 20, pady = 5)
        self.label_dfs_results = ttk.Label(self.frame_dfs_results, anchor = 'nw', text = '', font = FONT['info box'], wraplength = len(self.maze[0]) * CELL_SIZE - 50)
        self.label_dfs_results.pack(expand = True, fill = 'both', padx = 20, pady = 5)

        self.frame_astar_results = ttk.LabelFrame(self.master, text = 'A* Results', labelanchor = 'nw', relief = 'solid')
        self.frame_astar_results.grid(column = 2, row = 3, sticky = 'nsew', padx = 20, pady = 5)
        self.label_astar_results = ttk.Label(self.frame_astar_results, anchor = 'nw', text = '', font = FONT['info box'], wraplength = len(self.maze[0]) * CELL_SIZE - 50)
        self.label_astar_results.pack(expand = True, fill = 'both', padx = 20, pady = 5)


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
        self.bfs_counter = 0 # Reset counter
        self.bfs_path = [] # Reset path
        self.draw_maze(self.canvas_bfs)
        start_node = Node(self.start, None)
        queue = [start_node] # Use queue as data structure
        visited = set() # Create a set of visited nodes

        while len(queue) > 0: # Keep searching until queue is empty

            current_node = queue.pop(0)

            # Update info in application window
            self.bfs_counter += 1
            self.draw_path_circle(current_node, self.canvas_bfs, COLOUR['path_bfs'], self.bfs_counter)
            self.update_text()

            visited.add(current_node.position)

            if current_node.position == self.end:
                path = [] # Find path by seeking through all parents node
                while current_node is not None:
                    path.append(current_node.position)
                    current_node = current_node.parent

                self.bfs_path = path[::-1] # Reverse the list of nodes
                self.draw_path_all(self.bfs_path, self.canvas_bfs, COLOUR['path_bfs'])
                self.update_text()
                return path

            # From current cell, traverse to all possible nodes (N, E, S, W)
            for row_change, column_change in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                new_row = current_node.position[0] + row_change
                new_column = current_node.position[1] + column_change

                # Check if adjacent cell is a valid path
                # Valid path must be in range of maze boundaries
                # Valid path must not be a wall
                # Valid path cannot already be in queue
                if (
                    (0 <= new_row < len(self.maze)) and (0 <= new_column < len(self.maze[0])) and
                    (self.maze[new_row][new_column] != 1) and ((new_row, new_column) not in visited)
                    ) and all((new_row, new_column) != position for position in (node.position for node in queue)
                ):
                    # Set current node as parent and add current node to queue
                    queue.append(Node((new_row, new_column), current_node))

        self.bfs_path = 'BFS: no solution found'
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
        self.dfs_counter = 0 # Reset counter
        self.dfs_path = [] # Reset path
        self.draw_maze(self.canvas_dfs)
        start_node = Node(self.start, None)
        stack = [start_node] # Use stack as data structure
        visited = set() # Create a set of visited nodes

        while len(stack) > 0: # Keep searching until stack is empty

            current_node = stack.pop(-1)

            # Update info in application window
            self.dfs_counter += 1
            self.draw_path_circle(current_node, self.canvas_dfs, COLOUR['path_dfs'], self.dfs_counter)
            self.update_text()

            visited.add(current_node.position)

            if current_node.position == self.end:
                path = [] # Find path by seeking through all parents node
                while current_node is not None:
                    path.append(current_node.position)
                    current_node = current_node.parent

                self.dfs_path = path[::-1] # Reverse the list of nodes
                self.draw_path_all(self.dfs_path, self.canvas_dfs, COLOUR['path_dfs'])
                self.update_text()
                return path

            # From current cell, traverse to all possible nodes (W, S, E, N)
            for row_change, column_change in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                new_row = current_node.position[0] + row_change
                new_column = current_node.position[1] + column_change

                # Check if adjacent cell is a valid path
                # Valid path must be in range of maze boundaries
                # Valid path must not be a wall
                if (
                    (0 <= new_row < len(self.maze)) and (0 <= new_column < len(self.maze[0])) and
                    (self.maze[new_row][new_column] != 1) and ((new_row, new_column) not in visited)
                ):
                    # Set current node as parent and add current node to stack
                    stack.append(Node((new_row, new_column), current_node))

        self.dfs_path = 'DFS: no solution found'
        self.update_text()


    def start_astar(self):
        '''
        Function Name: start_dfs
            Starts the A* search algorithm to traverse a maze
        
        Parameters:
            Nothing
        
        Raises:
            Nothing
        
        Returns:
            list of tuples, list of positions to traverse from start to end
        '''
        # self.draw_maze(self.canvas_astar)
        self.astar_counter = 0 # Reset counter
        self.astar_path = [] # Reset path
        self.draw_maze(self.canvas_astar)
        start_node = Node(self.start, None)
        pqueue = PriorityQueue() # Instantiate a priority queue
        pqueue.put(start_node)
        visited = set() # Create a set of visited nodes

        while not pqueue.empty(): # Keep searching until priority queue is empty
            
            current_node = pqueue.get() # Takes out the node with least cost

            #Update info in application window
            self.astar_counter += 1
            self.draw_path_circle(current_node, self.canvas_astar, COLOUR['path_astar'], self.astar_counter)
            self.update_text()

            visited.add(current_node.position)

            if current_node.position == self.end:
                path = [] # Find path by seeking through all parents node
                while current_node is not None:
                    path.append(current_node.position)
                    current_node = current_node.parent

                self.astar_path = path[::-1] # Reverse the list of nodes
                self.draw_path_all(self.astar_path, self.canvas_astar, COLOUR['path_astar'])
                self.update_text()
                return path

            # From current cell, find all possible nodes (N, E, S, W)  
            for row_change, column_change in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                new_row = current_node.position[0] + row_change
                new_column = current_node.position[1] + column_change

                # Check if adjacent cell is a valid path
                # Valid path must be in range of maze boundaries
                # Valid path must not be a wall
                if (
                    (0 <= new_row < len(self.maze)) and (0 <= new_column < len(self.maze[0])) and
                    (self.maze[new_row][new_column] != 1) and ((new_row, new_column) not in visited)
                    and all((new_row, new_column) != node.position for node in pqueue.queue)
                ):
                    
                    # Distance from new cell to end cell:
                    # Calculate heuristic using Manthttan distance
                    #   h = abs(x - x_end) + abs(y - y_end)
                    h = abs(new_row - self.end[0]) + abs(new_column - self.end[1])
                    g = current_node.g + 1 # Update distance from current cell to new cell

                    # Set current node as parent and add current node to priority queue
                    new_node = Node((new_row, new_column), current_node, g, h)
                    pqueue.put(new_node)

        self.astar_path = 'A Star: no solution found'
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
                        column * CELL_SIZE, # pixels, horizontal distance to left edge
                        row * CELL_SIZE, # pixels, vertical distance to upper edge
                        column * CELL_SIZE + CELL_SIZE, # pixels, horizontal distance to right edge
                        row * CELL_SIZE + CELL_SIZE, # pixels, vertical distance to lower edge
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


    def draw_path_circle(self, current_node, canvas, colour, counter):
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
        for size in (0.20, 0.50, 0.70):
            self.wait(ANIMATION_INTERVAL)
            canvas.create_oval(
                column * CELL_SIZE + (0.5 - size / 2) * CELL_SIZE,
                row * CELL_SIZE + (0.5 - size / 2) * CELL_SIZE,
                column * CELL_SIZE + (0.5 + size / 2) *CELL_SIZE,
                row * CELL_SIZE + (0.5 + size / 2) *CELL_SIZE,
                fill = colour
            )
            canvas.create_text(
                column * CELL_SIZE + 0.5 * CELL_SIZE,
                row * CELL_SIZE + 0.5 * CELL_SIZE,
                text = counter,
                fill = COLOUR['font'],
                font = FONT['cell']
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
            self.wait(ANIMATION_INTERVAL)
            if (row, column) == path[0]:
                for size in (1.00, 0.75):
                    self.wait(ANIMATION_INTERVAL)
                    canvas.create_rectangle(
                        column * CELL_SIZE + (0.5 - size / 2) * CELL_SIZE,
                        row * CELL_SIZE + (0.5 - size / 2) * CELL_SIZE,
                        column * CELL_SIZE + (0.5 + size / 2) *CELL_SIZE,
                        row * CELL_SIZE + (0.5 + size / 2) *CELL_SIZE,
                        fill = COLOUR['start']
                )
                canvas.create_text(
                    column * CELL_SIZE + 0.5 * CELL_SIZE,
                    row * CELL_SIZE + 0.5 * CELL_SIZE,
                    text = 'S',
                    fill = COLOUR['font'],
                    font = FONT['cell']
                )

            elif (row, column) == path[-1]:
                for size in (1.00, 0.75):
                    self.wait(ANIMATION_INTERVAL)
                    canvas.create_rectangle(
                        column * CELL_SIZE + (0.5 - size / 2) * CELL_SIZE,
                        row * CELL_SIZE + (0.5 - size / 2) * CELL_SIZE,
                        column * CELL_SIZE + (0.5 + size / 2) *CELL_SIZE,
                        row * CELL_SIZE + (0.5 + size / 2) *CELL_SIZE,
                        fill = COLOUR['end']
                )
                canvas.create_text(
                    column * CELL_SIZE + 0.5 * CELL_SIZE,
                    row * CELL_SIZE + 0.5 * CELL_SIZE,
                    text = 'E',
                    fill = COLOUR['font'],
                    font = FONT['cell']
                )
            
            else:
                for size in (1.00,):
                    self.wait(ANIMATION_INTERVAL)
                    canvas.create_rectangle(
                        column * CELL_SIZE + (0.5 - size / 2) * CELL_SIZE,
                        row * CELL_SIZE + (0.5 - size / 2) * CELL_SIZE,
                        column * CELL_SIZE + (0.5 + size / 2) *CELL_SIZE,
                        row * CELL_SIZE + (0.5 + size / 2) *CELL_SIZE,
                        fill = colour
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

        text_astar = (
            f"Steps:\t{self.astar_counter}\n"
            f"Length:\t{len(self.astar_path)}\n"
            f"Path:\t{str(self.astar_path)[1 : -1]}\n"
        )
        self.label_astar_results.config(text = text_astar)


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
        [1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1],
        [1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1],
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


    
