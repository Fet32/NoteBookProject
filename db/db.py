"""Description..."""
from abc import ABC, abstractmethod
from mysql import connector

import time


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
	def execute(self, query: str):
		"""Execute SQL query."""


class MySQL(BaseDB):
	"""Class ..."""

	def __init__(self):
		self.connection: connector.connection.MySQLConnection = self.connect()

	def connect(self) -> connector.connection.MySQLConnection:
		try:
			return connector.connect(
				user='testuser',
				password='testpassword',
				host='localhost',
				port=3307,
				database='notebook'
			)
		except Exception as exc:
			print(exc)

	def create_cursor(self):
		return self.connection.cursor(buffered=True)

	def close(self):
		self.connection.close()

	def execute(self, query: str) -> tuple:

		with self.connection.cursor() as cur:
			cur.execute(query)

			return tuple(cur)


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

num_req = 20000

##############################################

start_a = time.perf_counter()
all_types = db_test.execute(query='SELECT * FROM field_type')

for i in range(num_req):
	r = db_test.execute(query='SELECT * FROM book_field WHERE field_name="field1"')

fin_a = time.perf_counter() - start_a
print('---> only select', fin_a)

##############################################

start_b = time.perf_counter()

for i in range(num_req):

	QUERY_SELECT_JOIN = """
	SELECT book_field.id, book_field.field_name, book_field.book_id, field_type.name
	FROM book_field
	INNER JOIN field_type
	ON book_field.type_id=field_type.id and field_name="field1";
	"""

	db_test.execute(query=QUERY_SELECT_JOIN)

fin_b = time.perf_counter() - start_b
print('---> with join', fin_b)

print('---> diff', fin_b / fin_a)

nb.close_db()

