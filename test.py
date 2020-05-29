def func(f):
    def wrapper(*args, **kwargs):
        print('hello')
        result = f(*args, **kwargs)
        print("good")
        return result

    return wrapper


@func
def f(x):
    return x


print(f(5))

from rethinkdb import RethinkDB

rdb = RethinkDB()

conn = rdb.connect(host='localhost', port='28015', db='test_db')

db = rdb.db('test_db')
print(db.table('user').run(conn))
