from PyQt5.QtMultimedia import QSound

class SoundPlayer():
	def __init__(self):
		self.apple = QSound('sound.wav')
		self.lose = QSound('sound2.wav')
		self.lose2 = QSound('sound3.wav')

	def play_apple(self):
		self.apple.play()

	def play_lose(self, theme):
		if theme not in [4, 5, 6]:
			self.lose.play()
		else:
			self.lose2.play()
