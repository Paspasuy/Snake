import os
import csv

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QColor

from CustomThemeSetup import CustomThemeSetup
from ThemeChooser import ThemeChooser

class ThemeWorker():
	def __init__(self):
		self.colors = [None for _ in range(5)]
		self.themes_str = ['dark', 'dark soft', 'light', 'light soft', 'cybernetic', 
		'gray', 'road to death', 'custom']
		self.themes = [[(0, 0, 0), (255, 255, 0), (0, 255, 0), (255, 0, 0), (255, 255, 255)],
			[(0, 0, 0), (255, 211, 95), (0, 153, 0), (200, 0, 0), (255, 255, 255)],
 			[(255, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0), (0, 0, 0)],
			[(200, 200, 200), (255, 211, 95), (0, 153, 0), (200, 0, 0), (0, 0, 0)], 
			[(0, 0, 0), (0, 0, 127), (0, 200, 0), (200, 200, 0), (255, 255, 255)], 
			[(0, 0, 0), (85, 85, 85), (100, 100, 100), (200, 200, 200), (255, 255, 255)], 
			[(0, 0, 0), (0, 0, 0), (0, 0, 0), (255, 255, 255), (255, 255, 255)], 
			[None, None, None, None, None]]
		self.theme = -10
		self.draw_eye = 1
		self.custom_theme_setup = None
		self.theme_chooser = None
		self.custom_theme_setup = None
		self.load_config()

	def set_theme(self, theme):
		self.theme = theme
		self.colors = list(map(lambda x: QColor(*x), self.themes[theme]))

	def load_config(self):
		if not os.path.exists('.snake_settings.csv'):
			for i in range(5):
				self.themes[-1][i] = self.themes[1][i]
			self.set_theme(1)
			self.write_custom()
		with open('.snake_settings.csv', 'r') as f:
			reader = list(csv.reader(f, lineterminator='\n'))
			theme = int(reader[0][0])
			self.draw_eye = int(reader[0][1])
			for i in range(5):
				self.themes[-1][i] = list(map(int, reader[i + 1][1][1:-1].split(', ')))
			self.set_theme(theme)

	def write_custom(self):
		with open('.snake_settings.csv', 'w') as f:
			writer = csv.writer(f, lineterminator='\n')
			writer.writerow([self.theme, self.draw_eye])
			st = ['background', 'grid', 'snake', 'apple', 'font']
			for i in range(5):
				writer.writerow([st[i], self.themes[-1][i]])

	def init_theme_chooser(self):
		self.theme_chooser = ThemeChooser(self.themes_str, self.theme)

	def init_custom_theme_setup(self):
		self.custom_theme_setup = CustomThemeSetup(list(map(lambda _: QColor(*_), self.themes[-1])))

	def change_eye(self):
		self.draw_eye = int(not self.draw_eye)

	def update_colors(self):
		if self.custom_theme_setup != None:
			if self.custom_theme_setup.changed:
				for i in range(5):
					kek = self.custom_theme_setup.colors[i]
					if kek != None:
						self.themes[-1][i] = (kek.red(), kek.green(), kek.blue())
				self.write_custom()
				self.set_theme(self.theme)