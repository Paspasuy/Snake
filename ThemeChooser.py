from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton

class ThemeChooser(QWidget):
	def __init__(self, themes_str, choose):
		super().__init__()
		self.choose = choose
		grid = QGridLayout()
		actions = [self.dark,
		self.dark_soft, self.light, 
		self.light_soft, self.custom]
		for i in range(5):
			button = QPushButton(themes_str[i])
			button.clicked.connect(actions[i])
			grid.addWidget(button, i, 0)
		self.setLayout(grid)

	def dark(self):
		self.choose = 0

	def dark_soft(self):
		self.choose = 1

	def light(self):
		self.choose = 2

	def light_soft(self):
		self.choose = 3

	def custom(self):
		self.choose = 4

