from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QColorDialog
from PyQt5.QtGui import QColor

class CustomThemeSetup(QWidget):

	def __init__(self, colors):
		super().__init__()
		grid = QGridLayout()
		text = ['background', 'grid', 'snake', 'apple', 'font']
		actions = [self.set_background_color,
		self.set_grid_color, self.set_snake_color, 
		self.set_apple_color, self.set_font_color]
		self.colors = colors
		self.changed = False
		self.buttons = [None] * 5
		for i in range(5):
			self.buttons[i] = QPushButton(text[i])
			p = self.buttons[i].palette()
			p.setColor(self.buttons[i].backgroundRole(), colors[i])
			p.setColor(self.buttons[i].foregroundRole(), self.inv_color(colors[i]))
			self.buttons[i].setPalette(p)
			self.buttons[i].clicked.connect(actions[i])
			grid.addWidget(self.buttons[i], i, 0)
		self.setLayout(grid)

	def set_color(self, color):
		self.changed = True
		self.colors[color] = QColorDialog.getColor()
		for i in range(5):
			p = self.buttons[i].palette()
			p.setColor(self.buttons[i].backgroundRole(), self.colors[i])
			p.setColor(self.buttons[i].foregroundRole(), self.inv_color(self.colors[i]))
			self.buttons[i].setPalette(p)
		self.update()

	def set_background_color(self):
		self.set_color(0)

	def set_grid_color(self):
		self.set_color(1)

	def set_snake_color(self):
		self.set_color(2)

	def set_apple_color(self):
		self.set_color(3)

	def set_font_color(self):
		self.set_color(4)

	def inv_color(self, color):
		return QColor(255 - color.red(),
			 255 - color.green(), 255 - color.blue()) 
