import sys

from PyQt5.QtCore import Qt, QPoint, QTimer, QSize
from PyQt5.QtGui import QPainter, QColor, QFont, QPaintEvent, QKeyEvent
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QMessageBox, QMainWindow, QAction

from DBWorker import DBWorker
from Logic import Logic
from DataTable import DataTable

PLAYER = 'anonymous'
STATUS_BAR_TEXT = 'Space: pause, Esc: quit'

dbw = None
app = None

class MainForm(QMainWindow):
	def __init__(self):
		super().__init__()
		global PLAYER
		self.cell = 40
		self.pause = True
		self.logic = Logic()
		self.h = 0
		name, is_ok = QInputDialog.getText(self, "Enter your name", "What is your name?")
		name = name.strip()
		if is_ok and name != '':
			PLAYER = name
		self.initUI()
		self.timer = QTimer()

	def initUI(self):
		self.statusBar().showMessage(STATUS_BAR_TEXT)
		menubar = self.menuBar()
		self.h = menubar.size().height()
		action_menu = menubar.addMenu('&Actions')
		play_action = QAction('&Play', self)
		history_action = QAction('&History', self)
		exit_action = QAction('&Exit', self)
		play_action.triggered.connect(self.show_game)
		history_action.triggered.connect(self.show_all)
		exit_action.triggered.connect(app.exit)
		exit_action.setShortcut('Esc')
		action_menu.addAction(play_action)
		action_menu.addAction(history_action)
		action_menu.addAction(exit_action)
		self.resize(self.logic.width * self.cell, self.logic.height * self.cell + 50)
		self.canvas = Canvas(self.logic.width * self.cell, self.logic.height * self.cell)
		self.setCentralWidget(self.canvas)
		self.canvas.move(0, self.h)

	def show_game(self):
		self.canvas = Canvas(self.logic.width * self.cell, self.logic.height * self.cell)
		self.statusBar().showMessage(STATUS_BAR_TEXT)
		self.setCentralWidget(self.canvas)

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
			self.logic.move()
			if self.logic.game_finished:
				dbw.save_result(len(self.logic.snake.body) - 3, PLAYER)
				self.show_best()
				self.logic.__init__()
				self.pause_game()
		self.update()

	def show_best(self):
		score = len(self.logic.snake.body) - 3
		best_all, best_player = dbw.get_max(PLAYER)
		s1 = "The best result on this PC:\n" + best_all[0][1] + ": " + str(best_all[0][2]) + ' (' + best_all[0][3] + ')\n'
		s2 = "Your best result:\n" + best_player[0][1] + ": " + str(best_player[0][2]) + ' (' + best_player[0][3] + ')\n'
		s3 = 'Your result:\n' + str(score) + '\n'
		if score == best_player[0][2]:
			s3 += 'You beat your own record!\n'
		if score == best_all[0][2]:
			s3 += 'You beat your PC record!\n'
		buttonReply = QMessageBox.question(self, 'Best results', s1 + s2 + s3, 
			QMessageBox.Yes)

	def show_all(self):
		table = DataTable(dbw.get_all())
		central_widget = table
		self.setCentralWidget(central_widget)

	def paintEvent(self, a0: QPaintEvent) -> None:
		self.canvas.painter.begin(self)
		self.canvas.painter.setRenderHints(QPainter.HighQualityAntialiasing)
		self.draw()
		self.canvas.painter.end()

	def draw(self):
		self.draw_background()
		self.draw_grid()
		self.draw_snake()
		self.draw_apple()
		self.draw_text()

	def draw_background(self):
		color = QColor(0, 0, 0)
		self.canvas.painter.setBrush(color)
		self.canvas.painter.setPen(color)
		self.canvas.painter.drawRect(0, 0 + self.h, self.logic.width * self.cell, self.logic.height * self.cell)

	def draw_grid(self):
		color = QColor(255, 211, 95)
		self.canvas.painter.setBrush(color)
		self.canvas.painter.setPen(color)
		for i in range(self.logic.width + 1):
			self.canvas.painter.drawPolygon(*[QPoint(i * self.cell, 0 + self.h), QPoint(i * self.cell, self.logic.height * self.cell + self.h)])
		for i in range(self.logic.height + 1):
			self.canvas.painter.drawPolygon(*[QPoint(0, i * self.cell + self.h), QPoint(self.logic.width * self.cell, i * self.cell + self.h)])

	def draw_snake(self):
		color = QColor(0, 153, 0)
		self.canvas.painter.setBrush(color)
		self.canvas.painter.setPen(color)
		r = self.cell - 4
		for x, y in self.logic.snake.body:
			self.canvas.painter.drawEllipse(self.cell * x + 2, self.cell * y + 2 + self.h, r, r)

	def draw_apple(self):
		color = QColor(200, 0, 0)
		self.canvas.painter.setBrush(color)
		self.canvas.painter.setPen(color)
		r = self.cell - 4
		self.canvas.painter.drawEllipse(self.cell * self.logic.apple_x + 2, self.cell * self.logic.apple_y + 2 + self.h, r, r)		

	def draw_text(self):
		color = QColor(255, 255, 255)
		self.canvas.painter.setPen(color)
		self.canvas.painter.setFont(QFont('Arial', 16))
		self.canvas.painter.drawText(0, 0 + self.h, self.cell, self.cell, Qt.AlignCenter, str(len(self.logic.snake.body) - 3))
		self.canvas.painter.drawText((self.logic.width -  4) * self.cell, 0 + self.h, 4 * self.cell, self.cell, Qt.AlignCenter, PLAYER)

	def keyPressEvent(self, event: QKeyEvent) -> None:
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


class Canvas(QWidget):
	def __init__(self, x, y):
		super().__init__()
		self.resize(x, y)
		self.painter = QPainter()
	def setColor(self, r, g, b):
		color = QColor(r, g, b)
		self.painter


if __name__ == '__main__':
	dbw = DBWorker()
	app = QApplication(sys.argv)
	wnd = MainForm()
	wnd.show()
	sys.exit(app.exec())
