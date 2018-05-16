#Sources:
#https://docs.python.org/3/reference/datamodel.html#data-model
#http://eddmann.com/posts/depth-first-search-and-breadth-first-search-in-python/

import math

class State():
	def __init__(self, cLeft, mLeft, boat, cRight, mRight):
		self.cLeft = cLeft
		self.mLeft = mLeft
		self.boat = boat
		self.cRight = cRight
		self.mRight = mRight
		self.parent = None

	def is_goal(self):
		if self.cLeft == 0 and self.mLeft == 0:
			return True
		else:
			return False

	def is_valid(self):
		if self.mLeft >= 0 and self.mRight >= 0 \
                   and self.cLeft >= 0 and self.cRight >= 0 \
                   and (self.mLeft == 0 or self.mLeft >= self.cLeft) \
                   and (self.mRight == 0 or self.mRight >= self.cRight):
			return True
		else:
			return False

	def __eq__(self, other):
		return self.cLeft == other.cLeft and self.mLeft == other.mLeft \
                   and self.boat == other.boat and self.cRight == other.cRight \
                   and self.mRight == other.mRight

	def __hash__(self):
		return hash((self.cLeft, self.mLeft, self.boat, self.cRight, self.mRight))

def successors(cur_state):
	solution = [];
	if cur_state.boat == 'left':
		new_state = State(cur_state.cLeft, cur_state.mLeft - 2, 'right',
                                  cur_state.cRight, cur_state.mRight + 2)
		if new_state.is_valid():
			new_state.parent = cur_state
			solution.append(new_state)
		new_state = State(cur_state.cLeft - 2, cur_state.mLeft, 'right',
                                  cur_state.cRight + 2, cur_state.mRight)
		if new_state.is_valid():
			new_state.parent = cur_state
			solution.append(new_state)
		new_state = State(cur_state.cLeft - 1, cur_state.mLeft - 1, 'right',
                                  cur_state.cRight + 1, cur_state.mRight + 1)
		if new_state.is_valid():
			new_state.parent = cur_state
			solution.append(new_state)
		new_state = State(cur_state.cLeft, cur_state.mLeft - 1, 'right',
                                  cur_state.cRight, cur_state.mRight + 1)
		if new_state.is_valid():
			new_state.parent = cur_state
			solution.append(new_state)
		new_state = State(cur_state.cLeft - 1, cur_state.mLeft, 'right',
                                  cur_state.cRight + 1, cur_state.mRight)
		if new_state.is_valid():
			new_state.parent = cur_state
			solution.append(new_state)
	else:
		new_state = State(cur_state.cLeft, cur_state.mLeft + 2, 'left',
                                  cur_state.cRight, cur_state.mRight - 2)
		if new_state.is_valid():
			new_state.parent = cur_state
			solution.append(new_state)
		new_state = State(cur_state.cLeft + 2, cur_state.mLeft, 'left',
                                  cur_state.cRight - 2, cur_state.mRight)
		if new_state.is_valid():
			new_state.parent = cur_state
			solution.append(new_state)
		new_state = State(cur_state.cLeft + 1, cur_state.mLeft + 1, 'left',
                                  cur_state.cRight - 1, cur_state.mRight - 1)
		if new_state.is_valid():
			new_state.parent = cur_state
			solution.append(new_state)
		new_state = State(cur_state.cLeft, cur_state.mLeft + 1, 'left',
                                  cur_state.cRight, cur_state.mRight - 1)
		if new_state.is_valid():
			new_state.parent = cur_state
			solution.append(new_state)
		new_state = State(cur_state.cLeft + 1, cur_state.mLeft, 'left',
                                  cur_state.cRight - 1, cur_state.mRight)
		if new_state.is_valid():
			new_state.parent = cur_state
			solution.append(new_state)
	return solution

def bfs():
	init_state = State(3,3,'left',0,0)
	if init_state.is_goal():
		return init_state
	x = list()
	y = set()
	x.append(init_state)
	while x:
		state = x.pop(0)
		if state.is_goal():
			return state
		y.add(state)
		solution = successors(state)
		for child in solution:
			if (child not in y) or (child not in x):
				x.append(child)
	return None

def final_sol(s):
		path = []
		path.append(s)
		parent = s.parent
		while parent:
			path.append(parent)
			parent = parent.parent

		for t in range(len(path)):
			state = path[len(path) - t - 1]
			print "(" + str(state.mLeft) + "," + str(state.cLeft) \
                              + "," + state.boat + "," + str(state.mRight) + "," + \
                              str(state.cRight) + ")"

def main():
	s = bfs()
	print "Missionaries and Cannibals solution:"
	print "(mLeft,cLeft,boat,mRight,cRight)"
	final_sol(s)
    
main()
