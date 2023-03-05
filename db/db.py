"""Description..."""
from abc import ABC, abstractmethod
from mysql import connector

from typing import Optional


class BaseDB(ABC):
	"""ABC class for DB."""

	@abstractmethod
	def connect(self):
		"""Create DB connection."""

	@abstractmethod
	def close(self):
		"""Close DB connection."""

	@abstractmethod
	def create_cursor(self):
		"""Create cursor."""

	@abstractmethod
	def execute(self, query: str, parameters: Optional[tuple]):
		"""Execute SQL query."""


class MySQL(BaseDB):
	"""Class ..."""

	def __init__(self):
		self.connection: connector.connection.MySQLConnection = self.connect()
		self.cursor: connector.connection.CursorBase = self.create_cursor()

	def connect(self) -> connector.connection.MySQLConnection:
		try:
			return connector.connect()
		except Exception as exc:
			print(exc)

	def create_cursor(self):
		return self.connection.cursor()

	def close(self):
		self.cursor.close()
		self.connection.close()

	def execute(self, query: str, parameters: Optional[tuple] = None):

		if not parameters:
			parameters = tuple()

		self.cursor.execute(query, parameters)

	def select(self, table, fields, where):
		...


class Notebook(object):

	def __init__(self, db):
		self.db: BaseDB = db

	def connect_db(self):
		self.db.connect()

	def close_db(self):
		self.db.close()


db_test = MySQL()

nb = Notebook(db=db_test)
nb.connect_db()
nb.close_db()

