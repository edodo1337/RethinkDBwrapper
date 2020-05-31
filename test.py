from db.utils import DBWrapper, establish_connection
from db.models.user import User



db_wrap = DBWrapper()

db_wrap.setup()

db_wrap.init_tables()

conn = db_wrap.connection
rdb = db_wrap.rdb
# print(rdb.table('user').run(conn))

# # print(User.table)


# import inspect
# import sys
# import db.models

# a = [m[0] for m in inspect.getmembers(db.models, inspect.isclass)]

# # a[0].init_table()

# print(a[0])

# db_wrap.table_create('things')
