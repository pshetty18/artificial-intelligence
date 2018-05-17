import random
import math

goal_state = [[1,2,3],
              [4,5,6],
              [7,8,0]]

def index(item, s):
    if item in s:
        return s.index(item)
    else:
        return -1

class EightPuzzle:

    def __init__(self):
        self.hval = 0
        self.depth = 0
        self.parent = None
        self.adj_matrix = []
        for i in range(3):
            self.adj_matrix.append(goal_state[i][:])

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        else:
            return self.adj_matrix == other.adj_matrix

    def __str__(self):
        res = ''
        for row in range(3):
            res += ' '.join(map(str, self.adj_matrix[row]))
            res += '\r\n'
        return res

    def clone(self):
        p = EightPuzzle()
        for i in range(3):
            p.adj_matrix[i] = self.adj_matrix[i][:]
        return p

    def get_legal_moves(self):
        row, col = self.find(0)
        free = []
        
        if row > 0:
            free.append((row - 1, col))
        if col > 0:
            free.append((row, col - 1))
        if row < 2:
            free.append((row + 1, col))
        if col < 2:
            free.append((row, col + 1))

        return free

    def generate_moves(self):
        free = self.get_legal_moves()
        zero = self.find(0)

        def swap_and_clone(a, b):
            p = self.clone()
            p.swap(a,b)
            p.depth = self.depth + 1
            p.parent = self
            return p

        return map(lambda pair: swap_and_clone(zero, pair), free)

    def generate_solution_path(self, path):
        if self.parent == None:
            return path
        else:
            path.append(self)
            return self.parent.generate_solution_path(path)

    def solve(self, h):
        def is_solved(puzzle):
            return puzzle.adj_matrix == goal_state

        open_list = [self]
        closed_list = []
        move_count = 0
        while len(open_list) > 0:
            x = open_list.pop(0)
            move_count += 1
            if (is_solved(x)):
                if len(closed_list) > 0:
                    return x.generate_solution_path([]), move_count
                else:
                    return [x]

            succ = x.generate_moves()
            idx_open = idx_closed = -1
            for move in succ:
                idx_open = index(move, open_list)
                idx_closed = index(move, closed_list)
                hvalue = h(move)
                fval = hvalue + move.depth

                if idx_closed == -1 and idx_open == -1:
                    move.hval = hvalue
                    open_list.append(move)
                elif idx_open > -1:
                    copy = open_list[idx_open]
                    if fval < copy.hval + copy.depth:
                        copy.hval = hvalue
                        copy.parent = move.parent
                        copy.depth = move.depth
                elif idx_closed > -1:
                    copy = closed_list[idx_closed]
                    if fval < copy.hval + copy.depth:
                        move.hval = hvalue
                        closed_list.remove(copy)
                        open_list.append(move)

            closed_list.append(x)
            open_list = sorted(open_list, key=lambda p: p.hval + p.depth)

        return [], 0

    def shuffle(self, step_count):
        for i in range(step_count):
            row, col = self.find(0)
            free = self.get_legal_moves()
            target = random.choice(free)
            self.swap((row, col), target)            
            row, col = target

    def find(self, value):
        if value < 0 or value > 8:
            raise Exception("value out of range")

        for row in range(3):
            for col in range(3):
                if self.adj_matrix[row][col] == value:
                    return row, col
    
    def peek(self, row, col):
        return self.adj_matrix[row][col]

    def poke(self, row, col, value):
        self.adj_matrix[row][col] = value

    def swap(self, pos_a, pos_b):
        temp = self.peek(*pos_a)
        self.poke(pos_a[0], pos_a[1], self.peek(*pos_b))
        self.poke(pos_b[0], pos_b[1], temp)


def heur(puzzle, item_total_calc, total_calc):
    t = 0
    for row in range(3):
        for col in range(3):
            val = puzzle.peek(row, col) - 1
            target_col = val % 3
            target_row = val / 3

            if target_row < 0: 
                target_row = 2

            t += item_total_calc(row, target_row, col, target_col)

    return total_calc(t)

def h_manhattan(puzzle):
    return heur(puzzle,
                lambda r, tr, c, tc: abs(tr - r) + abs(tc - c),
                lambda t : t)

def main():
    p = EightPuzzle()
    p.shuffle(20)
    print p

    path, count = p.solve(h_manhattan)
    path.reverse()
    for i in path: 
        print i

    print "Solved with Manhattan distance exploring", count, "states"

for i in range(0,3):
    main()
    print""
