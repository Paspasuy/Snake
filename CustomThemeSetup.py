from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton
from PyQt5.QtWidgets import QColorDialog

class CustomThemeSetup(QWidget):

	def __init__(self):
		super().__init__()
		grid = QGridLayout()
		text = ['background', 'grid', 'snake', 'apple', 'font']
		actions = [self.set_background_color,
		self.set_grid_color, self.set_snake_color, 
		self.set_apple_color, self.set_font_color]
		for i in range(5):
			button = QPushButton(text[i])
			button.clicked.connect(actions[i])
			grid.addWidget(button, i, 0)
		self.setLayout(grid)
		self.colors = [None] * 5
		self.changed = False

	def set_background_color(self):
		self.changed = True
		self.colors[0] = QColorDialog.getColor()

	def set_grid_color(self):
		self.changed = True
		self.colors[1] = QColorDialog.getColor()

	def set_snake_color(self):
		self.changed = True
		self.colors[2] = QColorDialog.getColor()

	def set_apple_color(self):
		self.changed = True
		self.colors[3] = QColorDialog.getColor()

	def set_font_color(self):
		self.changed = True
		self.colors[4] = QColorDialog.getColor()

