import sys

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QPoint, QTimer
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog

from DBWorker import DBWorker
from Logic import Logic

PLAYER = 'anonymous'

dbw = None

def write_data(snake):
	print('NAME:', PLAYER, ' ; SCORE:', len(snake.body) - 3)
	dbw.save_result(len(snake.body) - 3, PLAYER)

class MainForm(QWidget):
	def __init__(self):
		super().__init__()
		global PLAYER
		self.cell = 40
		self.pause = True
		self.logic = Logic()
		self.resize(self.logic.width * self.cell, self.logic.height * self.cell)
		self.painter = QPainter()

		name, is_ok = QInputDialog.getText(self, "Enter your name", "What is your name?")
		if is_ok and name != '':
			PLAYER = name
		print('Hello,', PLAYER + '!')
		self.timer = QTimer()
		self.timer.timeout.connect(self.start_game)
		self.timer.start(3000)

	def start_game(self):
		self.pause = False
		self.timer.stop()
		self.timer.timeout.disconnect()
		self.timer.timeout.connect(self.logic_process)
		self.timer.start(100)

	def pause_game(self):
		self.pause = True
		self.timer.stop()
		self.timer.timeout.disconnect()

	def logic_process(self):
		if not self.pause:
			self.logic.snake.move()
		self.update()

	def draw(self):
		self.draw_background()
		self.draw_grid()
		self.draw_snake()
		self.draw_apple()
		self.draw_text()

	def draw_background(self):
		color = QColor(0, 0, 0)
		self.painter.setBrush(color)
		self.painter.setPen(color)
		self.painter.drawRect(0, 0, self.logic.width * self.cell, self.logic.height * self.cell)

	def draw_grid(self):
		color = QColor(255, 211, 95)
		self.painter.setBrush(color)
		self.painter.setPen(color)
		for i in range(self.logic.width + 1):
			self.painter.drawPolygon(*[QPoint(i * self.cell, 0), QPoint(i * self.cell, self.logic.height * self.cell)])
		for i in range(self.logic.height + 1):
			self.painter.drawPolygon(*[QPoint(0, i * self.cell), QPoint(self.logic.width * self.cell, i * self.cell)])

	def draw_snake(self):
		color = QColor(0, 153, 0)
		self.painter.setBrush(color)
		self.painter.setPen(color)
		r = self.cell - 4
		for x, y in self.logic.snake.body:
			self.painter.drawEllipse(self.cell * x + 2, self.cell * y + 2, r, r)

	def draw_apple(self):
		color = QColor(200, 0, 0)
		self.painter.setBrush(color)
		self.painter.setPen(color)
		r = self.cell - 4
		self.painter.drawEllipse(self.cell * self.logic.apple_x + 2, self.cell * self.logic.apple_y + 2, r, r)		

	def draw_text(self):
		color = QColor(255, 255, 255)
		self.painter.setPen(color)
		self.painter.setFont(QFont('Arial', 16))
		self.painter.drawText(0, 0, self.cell, self.cell, Qt.AlignCenter, str(len(self.logic.snake.body) - 3))
		self.painter.drawText((self.logic.width -  4) * self.cell, 0, 4 * self.cell, self.cell, Qt.AlignCenter, PLAYER)

	def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
		self.painter.begin(self)
		self.painter.setRenderHints(QPainter.HighQualityAntialiasing)
		self.draw()
		self.painter.end()

	def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
		if event.key() == Qt.Key_Left:
			if self.logic.snake.y_dir:
				self.logic.snake.next_x_dir = -1
				self.logic.snake.next_y_dir = 0
		if event.key() == Qt.Key_Right:
			if self.logic.snake.y_dir:
				self.logic.snake.next_x_dir = 1
				self.logic.snake.next_y_dir = 0
		if event.key() == Qt.Key_Up:
			if self.logic.snake.x_dir:
				self.logic.snake.next_x_dir = 0
				self.logic.snake.next_y_dir = -1
		if event.key() == Qt.Key_Down:
			if self.logic.snake.x_dir:
				self.logic.snake.next_x_dir = 0
				self.logic.snake.next_y_dir = 1

		if event.key() == Qt.Key_Space:
			if self.pause == True:
				self.timer.timeout.connect(self.start_game)
				self.timer.start(0)
			else:
				self.pause_game()


if __name__ == '__main__':
	dbw = DBWorker()
	app = QApplication(sys.argv)
	wnd = MainForm()
	wnd.show()
	sys.exit(app.exec())
