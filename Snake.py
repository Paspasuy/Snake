class Snake:
	def __init__(self, logic):
		self.x = logic.width // 2 + 1
		self.y = logic.height // 2
		self.x_dir = 1
		self.y_dir = 0
		self.next_x_dir = 1
		self.next_y_dir = 0
		self.w = logic.width
		self.h = logic.height
		self.body = [[self.x - 2, self.y], [self.x - 1, self.y], [self.x, self.y]]

	def move(self):
		self.x_dir = self.next_x_dir
		self.y_dir = self.next_y_dir
		x = self.x + self.x_dir
		y = self.y + self.y_dir
		x %= self.w
		y %= self.h
		self.x = x
		self.y = y
		self.body.append([x, y])
