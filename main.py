class Node:
    def __init__(self, state, parent, actions):
        self.state = state
        self.parent = parent
        self.actions = actions

class Stack:
    def __init__(self):
        self.frontier = []

    def add(self, other):
        self.frontier.append(other)

    def remove(self):
        if not self.is_empty():
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node
        else:
            raise Exception("Empty Frontier")

    def contains_state(self, state):
        return any(state == s for s in self.frontier)

    def is_empty(self):
        return self.frontier == []

class Queue(Stack):
    def remove(self):
        if not self.is_empty():
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node
        else:
            raise Exception("Empty Frontier")

class Maze:
    def __init__(self, filename):
        with open(filename) as f:
            contents = f.read()

        if contents.count("A") != 1:
            raise Exception("Should have 1 start point")
        if contents.count("B") != 1:
            raise Exception("Should have 1 end point")
        
        contents = contents.splitlines()

        self.height = len(contents)
        self.width = max(len(line) for line in contents)
        
        self.walls = []
        for i in range(self.height):
            r = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i,j)
                        r.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i,j)
                        r.append(False)
                    elif contents[i][j] == " ":
                        r.append(False)
                    else:
                        r.append(True)
                except IndexError:
                    r.append(False)        

            self.walls.append(r)

        for line in self.walls:
            print(line)

        self.solution = None

    def neighbours(self, state):
        r, c = state
        options = [("up", (r-1, c)),
                   ("down", (r+1, c)),
                   ("left", (r, c-1)),
                   ("right", (r, c+1))]

        result = []
        for action, (row, col) in options:
            if 0 <= row < self.height and 0 <= col < self.width and not(self.walls[row][col]):
                result.append((action, (row, col)))

        print(state, ":", result)
        return result

    '''def solve(self):
        frontier = Stack()
        self.num_exp = 0

        self.exp_spaces = set()

        start = Node(state = self.start, parent=None, actions=None)
        frontier.add(start)

        while True:
            if frontier.is_empty():
                raise Exception("No Solution found")

            node = frontier.remove()
            self.num_exp += 1
            if node.state == self.goal:
                action = []
                cells = []

                while node.parent is not None:
                    cells.append(node.state)
                    action.append(node.actions)
                    node = node.parent

                action.reverse()
                cells.reverse()

                self.solution = (action, cells)
                return

        self.exp_spaces.add(node.state)

        for action, state in self.neighbours(node.state):
            if not frontier.contains_state(state) and state not in self.exp_spaces:
                child = Node(state = state, parent = node, actions=action)
                frontier.add(child)'''

    def solve(self):
        self.num_exp = 0
        self.exp_spaces = set()

        frontier = Queue()
        startNode = Node(state=self.start, parent=None, actions=None)
        frontier.add(startNode)

        while True:

            if frontier.is_empty():
                raise Exception("No Sol")

            node = frontier.remove()
            self.num_exp += 1

            if node.state == self.goal:
                cells = []
                actions = []

                while node.parent is not None:
                    cells.append(node.state)
                    actions.append(node.actions)
                    node = node.parent

                cells.reverse()
                actions.reverse()

                self.solution = (actions, cells)
                return

            self.exp_spaces.add(node.state)

            for action, state in self.neighbours(node.state):
                if not frontier.contains_state(state) and state not in self.exp_spaces:
                    child = Node(state = state, parent=node, actions=action)
                    frontier.add(child)

    def print_maze(self):
        sol = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end = "")
                elif (i, j) == self.start:
                    print("A", end = "")
                elif (i, j) == self.goal:
                    print("B", end = "")
                elif sol is not None and (i, j) in sol:
                    print("*", end = "")
                else:
                    print(" ", end = "")
            print()
        print()


m = Maze("maze2.txt")
m.print_maze()
m.solve()
print(m.num_exp)
m.print_maze()