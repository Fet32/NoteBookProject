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
				database='notebook',
				# auth_plugin='mysql_native_password'
			)
		except Exception as exc:
			print(exc)

	def create_cursor(self) -> connector.connection.MySQLCursor:
		return self.connection.cursor()#buffered=True)

	def close(self):
		self.connection.close()

	def execute(self, query: str) -> tuple:

		with self.create_cursor() as cur: #self.connection.cursor() as cur:
			cur.execute(query)

			return tuple(cur)

	def commit(self):
		self.connection.commit()


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

num_req = 100

##############################################

# db_test.execute(query='insert into user (name) values ("Fet")')
# db_test.execute(query='insert into book (name,user_id) values ("book1", 1)')
# for i in range(1,10):
# 	db_test.execute(query='insert into book_field (field_name, field_type, book_id) values ("field%s","txt",1)'%i)
# for record in range(2000):
# 	for i in range(1,10):
# 		db_test.execute(query='''
# 							insert into book_record
# 							(record_id, field_id, value_num, value_txt)
# 							values
# 							(%(record)d, %(i)d, %(i)d, "field%(i)s")
# 							''' % {'record': record, 'i': i})
#
# db_test.commit()

start_a = time.perf_counter()
all_types = db_test.execute(query='SELECT * FROM book_field')

for i in range(num_req):
	r = db_test.execute(query='SELECT * FROM book_record WHERE value_txt="field5"')

fin_a = time.perf_counter() - start_a
print('---> only select', fin_a)

##############################################

start_b = time.perf_counter()

for i in range(num_req):

	QUERY_SELECT_JOIN = """
	SELECT book_record.id, book_record.record_id, book_record.field_id, book_field.field_name
	FROM book_record
	INNER JOIN book_field
	ON book_record.field_id=book_field.id and field_name="field5";
	"""

	db_test.execute(query=QUERY_SELECT_JOIN)

fin_b = time.perf_counter() - start_b
print('---> with join', fin_b)

print('---> diff', fin_b / fin_a)

nb.close_db()

