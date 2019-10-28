import os

import sqlite3 

class DBWorker:
	def __init__(self):
		self.name = 'snake_achievements.sqlite3'
		self.dir = os.getcwd()
		self.path = os.path.join(self.dir, self.name)
		try:
			new_created = False
			if not os.path.exists(self.path):
				new_created = True
			self.conn = sqlite3.connect(self.path)
			self.cursor = self.conn.cursor()
			if new_created:
				self.init_db()
				print(new_created)
			print("Successfully inited DB")
			self.get_max('pavel')
# os.popen('sudo chmod 777 ' + path_db).read()
		except sqlite3.Error as e:            
			print('DB error: ' + str(e))

	def init_db(self):
		self.cursor.executescript("""
			CREATE TABLE "records" (
			`id`    INTEGER PRIMARY KEY AUTOINCREMENT,
			`player`    TEXT,
			`score`    INTEGER,
			`date`    TEXT
			);
			""")

	def save_result(self, size, player):
		self.cursor.executescript("""
			INSERT INTO `records`  (player, score, date)  
			VALUES('%s',%s, DATETIME('now'));
		""" % (player, str(size)))
		self.conn.commit()
		result = self.cursor.execute("""SELECT * FROM records""").fetchall()
		for _ in result:
			print(_)

	def get_max(self, player):
		result = self.cursor.execute("""SELECT * FROM records WHERE score = (SELECT MAX(score) FROM records)""").fetchall()
		player_result = self.cursor.execute("""SELECT * FROM records WHERE
		 										score = (SELECT MAX(score) FROM records WHERE 
												player = ("%s"))""" % player).fetchall()
		print(result)
		print(player_result)
