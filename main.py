import sys

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QPoint, QTimer
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog

from random import randint

WIDTH = 20
HEIGHT = 15
CELL = 40

EMPTY = 0
BODY = 1
APPLE = 2

PAUSE = True

PLAYER = 'anonymous'

matrix = [[EMPTY] * HEIGHT for _ in range(WIDTH)]

apple_x = 0
apple_y = 0

def gen_apple():
	global apple_x, apple_y
	x = randint(0, WIDTH - 1)
	y = randint(0, HEIGHT - 1)
	while matrix[x][y] != EMPTY:
		x = randint(0, WIDTH - 1)
		y = randint(0, HEIGHT - 1)
	apple_x = x
	apple_y = y
	matrix[x][y] = APPLE


def write_data(snake):
	print('NAME:', PLAYER, ' ; SCORE:', len(snake.body) - 3)

class Snake:
	def __init__(self):
		x = WIDTH // 2 + 1
		y = HEIGHT // 2
		self.body = [[x - 2, y], [x - 1, y], [x, y]]
		matrix[x - 2][y] = BODY
		matrix[x - 1][y] = BODY
		matrix[x][y] = BODY
		self.x = x
		self.y = y
		self.x_dir = 1
		self.y_dir = 0
		self.next_x_dir = 1
		self.next_y_dir = 0

	def move(self):
		self.x_dir = self.next_x_dir
		self.y_dir = self.next_y_dir
		x = self.x + self.x_dir
		y = self.y + self.y_dir
		x %= WIDTH
		y %= HEIGHT
		self.x = x
		self.y = y
		self.body.append([x, y])
		if len(self.body) == WIDTH * HEIGHT:
			print('WIN!')
			matrix[x][y] = BODY
		if matrix[x][y] == APPLE:
			matrix[x][y] = BODY
			gen_apple()
		elif matrix[x][y] == EMPTY:
			matrix[self.body[0][0]][self.body[0][1]] = EMPTY
			self.body.pop(0)
			matrix[x][y] = BODY
		elif matrix[x][y] == BODY:
			print('GAME OVER!')
			write_data(self)
			for x, y in self.body:
				matrix[x][y] = EMPTY
			matrix[apple_x][apple_y] = EMPTY
			self.__init__()
			gen_apple()


class MainForm(QWidget):
	def __init__(self):
		global PLAYER
		super().__init__()
		self.resize(WIDTH * CELL, HEIGHT * CELL)
		gen_apple()	
		self.painter = QPainter()
		self.snake = Snake()
		name, is_ok = QInputDialog.getText(self, "Enter your name", 
											   "What is your name?")
		if is_ok and name != '':
			PLAYER = name
		print('Hello,', PLAYER + '!')
		self.timer = QTimer()
		self.timer.timeout.connect(self.start_game)
		self.timer.start(3000)

	def start_game(self):
		global PAUSE
		PAUSE = False
		self.timer.stop()
		self.timer.timeout.disconnect()
		self.timer.timeout.connect(self.logic)
		self.timer.start(100)

	def pause_game(self):
		global PAUSE
		PAUSE = True
		self.timer.stop()
		self.timer.timeout.disconnect()

	def logic(self):
		global PAUSE
		if not PAUSE:
			self.snake.move()
		self.update()

	def draw(self):
		color_brush = QColor(0, 0, 0)
		color_pen = QColor(0, 0, 0)
		self.painter.setBrush(color_brush)
		self.painter.setPen(color_pen)
		self.painter.drawRect(0, 0, WIDTH * CELL, HEIGHT * CELL)
		color_brush = QColor(255, 211, 95)
		color_pen = QColor(255, 211, 95)
		self.painter.setBrush(color_brush)
		self.painter.setPen(color_pen)
		for i in range(WIDTH + 1):
			self.painter.drawPolygon(*[QPoint(i * CELL, 0), QPoint(i * CELL, HEIGHT * CELL)])
		for i in range(HEIGHT + 1):
			self.painter.drawPolygon(*[QPoint(0, i * CELL), QPoint(WIDTH * CELL, i * CELL)])
		color_brush = QColor(0, 153, 0)
		color_pen = QColor(0, 153, 0)
		self.painter.setBrush(color_brush)
		self.painter.setPen(color_pen)
		for x, y in self.snake.body:
			r = CELL - 4
			self.painter.drawEllipse(CELL * x + 2, CELL * y + 2, r, r)
		color_brush = QColor(200, 0, 0)
		color_pen = QColor(200, 0, 0)
		self.painter.setBrush(color_brush)
		self.painter.setPen(color_pen)
		self.painter.drawEllipse(CELL * apple_x + 2, CELL * apple_y + 2, r, r)

	def draw_text(self, a0):
		self.painter.setPen(QColor(255, 255, 255))
		self.painter.setFont(QFont('Arial', 16))
		self.painter.drawText(0, 0, CELL, CELL, Qt.AlignCenter, str(len(self.snake.body) - 3))
		self.painter.drawText((WIDTH -  4) * CELL, 0, 4 * CELL, CELL, Qt.AlignCenter, PLAYER)

	def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
		self.painter.begin(self)
		self.painter.setRenderHints(QPainter.HighQualityAntialiasing)
		self.draw()
		self.draw_text(a0)
		self.painter.end()

	def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
		if event.key() == Qt.Key_Left:
			if self.snake.y_dir:
				self.snake.next_x_dir = -1
				self.snake.next_y_dir = 0
		if event.key() == Qt.Key_Right:
			if self.snake.y_dir:
				self.snake.next_x_dir = 1
				self.snake.next_y_dir = 0
		if event.key() == Qt.Key_Up:
			if self.snake.x_dir:
				self.snake.next_x_dir = 0
				self.snake.next_y_dir = -1
		if event.key() == Qt.Key_Down:
			if self.snake.x_dir:
				self.snake.next_x_dir = 0
				self.snake.next_y_dir = 1

		if event.key() == Qt.Key_Space:
			if PAUSE == True:
				self.timer.timeout.connect(self.start_game)
				self.timer.start(0)
			else:
				self.pause_game()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	wnd = MainForm()
	wnd.show()
	sys.exit(app.exec())
