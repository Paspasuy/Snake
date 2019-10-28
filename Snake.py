
EMPTY = 0
BODY = 1
APPLE = 2
class Snake:
	def __init__(self, logic):
		self.logic = logic
		self.x = self.logic.width // 2 + 1
		self.y = self.logic.height // 2
		self.x_dir = 1
		self.y_dir = 0
		self.next_x_dir = 1
		self.next_y_dir = 0
		self.w = logic.width
		self.h = self.logic.height
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
		if len(self.body) == self.logic.width * self.logic.height:
			print('WIN!')
			self.logic.matrix[x][y] = BODY
		if self.logic.matrix[x][y] == APPLE:
			self.logic.matrix[x][y] = BODY
			self.logic.gen_apple()
		elif self.logic.matrix[x][y] == EMPTY:
			self.logic.matrix[self.body[0][0]][self.body[0][1]] = EMPTY
			self.body.pop(0)
			self.logic.matrix[x][y] = BODY
		elif self.logic.matrix[x][y] == BODY:
			print('GAME OVER!')
			write_data(self)
			for x, y in self.body:
				self.logic.matrix[x][y] = EMPTY
			self.logic.matrix[self.logic.apple_x][self.logic.apple_y] = EMPTY
			self.__init__(self.logic)
			self.logic.gen_apple()

