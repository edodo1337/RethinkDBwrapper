from db.utils import DBWrapper, establish_connection
from db.models.user import User, Book

from rethinkdb import r

db_wrap = DBWrapper()

db_wrap.setup()


conn = db_wrap.connection
rdb = db_wrap.rdb

print('TABLE', User.table, Book.table)
# print(User.filter(r.row['age'].eq(21), fields=['age', 'name']))