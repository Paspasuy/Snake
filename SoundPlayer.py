from PyQt5.QtMultimedia import QSound

class SoundPlayer():
	def __init__(self):
		self.apple = QSound('sound.wav')
		self.lose = QSound('sound2.wav')

	def play_apple(self):
		self.apple.play()

	def play_lose(self):
		self.lose.play()
