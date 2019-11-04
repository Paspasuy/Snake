#!/bin/python3
import sys

from PyQt5.QtCore import Qt, QPoint, QTimer, QSize
from PyQt5.QtGui import QPainter, QColor, QFont, QPaintEvent, QKeyEvent
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QMessageBox, QMainWindow, QAction

from DBWorker import DBWorker
from Logic import Logic
from DataTable import DataTable
from SoundPlayer import SoundPlayer
from ThemeWorker import ThemeWorker
from ThemeChooser import ThemeChooser
from CustomThemeSetup import CustomThemeSetup

class MainForm(QMainWindow):
	def __init__(self, database_worker, sound_player):
		super().__init__()
		self.database_worker = database_worker
		self.sound_player = sound_player
		self.player = 'anonymous'
		self.get_name()
		self.status_bar_text = 'Space: pause, Esc: quit'
		self.cell = 40
		self.pause = True
		self.logic = Logic()
		self.timer = QTimer()
		self.theme_worker = ThemeWorker()
		self.play_sounds = True
		self.init_ui()

	def init_ui(self):
		self.status_bar = self.statusBar()
		menubar = self.menuBar()
		self.h = menubar.size().height()
		action_menu = menubar.addMenu('&Actions')
		settings_menu = menubar.addMenu('&Settings')
		play_action = QAction('&Play', self)
		history_action = QAction('&History', self)
		logout_action = QAction('&Log out', self)
		exit_action = QAction('&Exit', self)
		play_action.triggered.connect(self.show_game)
		history_action.triggered.connect(self.show_all)
		logout_action.triggered.connect(self.logout)
		exit_action.triggered.connect(app.exit)
		exit_action.setShortcut('Esc')
		change_theme_action = QAction('&Choose theme', self)
		theme_setup_action = QAction('&Set up custom theme', self)
		change_sounds_action = QAction('&Disable/enable sounds', self)
		change_eye_action = QAction('&Disable/enable eye', self)
		change_theme_action.triggered.connect(self.change_theme)
		theme_setup_action.triggered.connect(self.setup_custom_theme)
		change_sounds_action.triggered.connect(self.change_sounds)
		change_eye_action.triggered.connect(self.theme_worker.change_eye)
		action_menu.addAction(play_action)
		action_menu.addAction(history_action)
		action_menu.addAction(logout_action)
		action_menu.addAction(exit_action)
		settings_menu.addAction(change_theme_action)
		settings_menu.addAction(theme_setup_action)
		settings_menu.addAction(change_sounds_action)
		settings_menu.addAction(change_eye_action)
		self.setFixedSize(self.logic.width * self.cell, self.logic.height * self.cell + self.h + self.status_bar.height())
		self.canvas = Canvas(self.logic.width * self.cell, self.logic.height * self.cell)
		self.setCentralWidget(self.canvas)
		self.canvas.move(0, self.h)

	def get_name(self):
		name, is_ok = QInputDialog.getText(self, "Enter your name", "What is your name?")
		name = name.strip()
		if is_ok and name != '':
			self.player = name
		elif is_ok and name == '':
			self.player = 'anonymous'
		return is_ok

	def logout(self):
		self.pause_game()
		if self.get_name():
			self.update()
			self.logic = Logic()

	def show_game(self):
		self.theme_worker.update_colors()
		if self.theme_worker.theme_chooser != None:
			self.theme_worker.set_theme(self.theme_worker.theme_chooser.choose)
		self.theme_worker.write_custom()
		self.canvas = Canvas(self.logic.width * self.cell, self.logic.height * self.cell)
		self.setCentralWidget(self.canvas)

	def start_game(self):
		if self.pause == True:
			self.pause = False
			self.timer.timeout.connect(self.logic_process)
			self.timer.start(100)

	def pause_game(self):
		if self.pause == False:
			self.pause = True
			self.timer.stop()
			self.timer.timeout.disconnect()
			self.update()

	def change_sounds(self):
		self.play_sounds = not self.play_sounds

	def change_theme(self):
		self.pause_game()
		self.theme_worker.init_theme_chooser()
		self.setCentralWidget(self.theme_worker.theme_chooser)

	def setup_custom_theme(self):
		self.pause_game()
		self.theme_worker.init_custom_theme_setup()
		self.setCentralWidget(self.theme_worker.custom_theme_setup)

	def logic_process(self):
		if not self.pause:
			l1 = len(self.logic.snake.body)
			self.logic.move()
			l2 = len(self.logic.snake.body)
			if self.logic.game_finished:
				self.database_worker.save_result(len(self.logic.snake.body) - 3, self.player)
				if self.play_sounds:
					self.sound_player.play_lose()
				self.show_best()
				self.logic = Logic()
				self.pause_game()
			elif l2 - l1 == 1 and self.play_sounds:
				self.sound_player.play_apple()
		self.update()

	def show_best(self):
		score = len(self.logic.snake.body) - 3
		best_all, best_player = self.database_worker.get_max(self.player)
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
		self.pause_game()
		table = DataTable(self.database_worker.get_all())
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
		self.status_bar.showMessage(self.status_bar_text)

	def draw_background(self):
		self.canvas.set_color(self.theme_worker.colors[0])
		self.canvas.painter.drawRect(0, 0 + self.h, self.logic.width * self.cell, self.logic.height * self.cell)

	def draw_grid(self):
		self.canvas.set_color(self.theme_worker.colors[1])
		for i in range(self.logic.width + 1):
			self.canvas.painter.drawPolygon(*[QPoint(i * self.cell, 0 + self.h), QPoint(i * self.cell, self.logic.height * self.cell + self.h)])
		for i in range(self.logic.height + 1):
			self.canvas.painter.drawPolygon(*[QPoint(0, i * self.cell + self.h), QPoint(self.logic.width * self.cell, i * self.cell + self.h)])

	def draw_snake(self):
		self.canvas.set_color(self.theme_worker.colors[2])
		r = self.cell - 4
		for x, y in self.logic.snake.body:
			self.canvas.painter.drawEllipse(self.cell * x + 2, self.cell * y + 2 + self.h, r, r)
		if self.theme_worker.draw_eye:
			x = self.logic.snake.x
			x = int(self.cell * (x + 0.25)) + int(self.cell * 0.25) * self.logic.snake.x_dir
			y = self.logic.snake.y
			y = int(self.cell * (y + 0.25)) + int(self.cell * 0.25) * self.logic.snake.y_dir
			y += self.h
			self.canvas.set_color(self.inv_color(self.theme_worker.colors[2]))
			self.canvas.painter.drawEllipse(x, y, r // 2, r // 2)

	def draw_apple(self):
		self.canvas.set_color(self.theme_worker.colors[3])
		r = self.cell - 4
		self.canvas.painter.drawEllipse(self.cell * self.logic.apple_x + 2, self.cell * self.logic.apple_y + 2 + self.h, r, r)		

	def draw_text(self):
		self.canvas.set_color(self.theme_worker.colors[4])
		self.canvas.painter.setFont(QFont('Arial', 16))
		self.canvas.painter.drawText(0, 0 + self.h, self.cell, self.cell, Qt.AlignCenter, str(len(self.logic.snake.body) - 3))
		self.canvas.painter.drawText((self.logic.width - 4) * self.cell, 0 + self.h, 4 * self.cell, self.cell, Qt.AlignCenter, self.player)
		if self.pause == True:
			self.canvas.painter.setFont(QFont('Arial', 32))
			self.canvas.painter.drawText((self.logic.width // 2 - 4) * self.cell, (self.logic.height // 2 - 1) * self.cell + self.h, 8 * self.cell, self.cell * 4, Qt.AlignCenter, 'PAUSED')

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
				self.start_game()
			else:
				self.pause_game()
	def inv_color(self, color):
		return QColor(255 - color.red(),
			 255 - color.green(), 255 - color.blue()) 


class Canvas(QWidget):
	def __init__(self, x, y):
		super().__init__()
		self.resize(x, y)
		self.painter = QPainter()
	def set_color(self, color):
		self.painter.setBrush(color)
		self.painter.setPen(color)


if __name__ == '__main__':
	app = QApplication(sys.argv)
	database_worker = DBWorker()
	sound_player = SoundPlayer()
	wnd = MainForm(database_worker, sound_player)
	wnd.show()
	sys.exit(app.exec())
