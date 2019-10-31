from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt

class DataTable(QTableWidget):
	def __init__(self, data):
		super().__init__()
		self.setColumnCount(3)
		self.setHorizontalHeaderLabels(["Player", "Score", "Date"])
		self.setRowCount(len(data))
		self.horizontalHeaderItem(0).setTextAlignment(Qt.AlignHCenter)
		self.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)
		self.horizontalHeaderItem(2).setTextAlignment(Qt.AlignHCenter)
		for i in range(len(data)):
			for j in range(3):
				self.setItem(i, j, QTableWidgetItem(str(data[i][j + 1])))
		self.resizeColumnsToContents()
