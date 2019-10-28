from Snake import Snake

from random import randint

EMPTY = 0
BODY = 1
APPLE = 2

class Logic:
	def __init__(self):
		self.game_finished = False
		self.width = 20
		self.height = 15
		self.matrix = [[EMPTY] * self.height for _ in range(self.width)]
		self.snake = Snake(self)
		for x, y in self.snake.body:
			self.matrix[x][y] = BODY
		self.gen_apple()

	def gen_apple(self):
		x = randint(0, self.width - 1)
		y = randint(0, self.height - 1)
		while self.matrix[x][y] != EMPTY:
			x = randint(0, self.width - 1)
			y = randint(0, self.height - 1)
		self.apple_x = x
		self.apple_y = y
		self.matrix[self.apple_x][self.apple_y] = APPLE

	def move(self):
		snake = self.snake
		snake.move()
		x = snake.x
		y = snake.y
		if self.matrix[x][y] == APPLE:
			self.matrix[x][y] = BODY
			if len(snake.body) == self.width * self.height:
				print('WIN!')
			self.gen_apple()

		else:
			self.matrix[snake.body[0][0]][snake.body[0][1]] = EMPTY
			snake.body.pop(0)
			if self.matrix[x][y] == BODY:
				print('GAME OVER!')
				self.game_finished = True
			else:
				self.matrix[x][y] = BODY
