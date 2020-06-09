from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
import inspect
import sys
import asyncio


class DBWrapper:
    RDB_HOST = None
    RDB_PORT = None
    APP_DB = None
    _rdb = None
    _connection = None

    _instance = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DBWrapper, cls).__new__(cls)
        return cls.instance

    def __init__(self, **kwargs):
        self.APP_DB = kwargs.get('APP_DB', 'test_db')
        self.RDB_HOST = kwargs.get('RDB_HOST', 'localhost')
        self.RDB_PORT = kwargs.get('RDB_PORT', 28015)

    def setup(self):
        r = RethinkDB()
        self._connection = r.connect(host=self.RDB_HOST, port=self.RDB_PORT)
        try:
            r.db_create(self.APP_DB).run(self._connection)
            print(f' * [x] Database "{self.APP_DB}" created')
        except RqlRuntimeError:
            print(f' * [-] Database "{self.APP_DB}" is already exist.')
        finally:
            self._rdb = r.db(self.APP_DB)
            self._connection.close()
        self.init_tables()

    def init_tables(self):
        import db.models
        class_list = [m for m in inspect.getmembers(db.models, inspect.isclass)]
        # a[0].init_table()
        for item in class_list:
            self.table_create(item)

    def table_create(self, class_item):
        conn = self.connection
        try:
            class_item[1].init_table()
            self._rdb.table_create(class_item[1]._table).run(conn)
            print(f' * [x] Table "{class_item[1]._table}" created')
        except RqlRuntimeError:
            print(f' * [-] Table "{class_item[0]}" is already exist.')
        finally:
            conn.close()

    @property
    def connection(self):
        r = RethinkDB()
        try:
            conn = r.connect(host=self.RDB_HOST, port=self.RDB_PORT)
            return conn
        except RqlDriverError as e:
            raise

    @property
    def rdb(self):
        return self._rdb

    @classmethod
    def get_solo(cls):
        if not cls.__instance:
            cls.__instance = DBWrapper()
        return cls.__instance


def establish_connection(func):
    def wrapper(*args, **kwargs):
        db = DBWrapper.get_solo()
        print('[x] Before request')
        # try:
        #     db.connection = db.get_connection()
        # except RqlDriverError:
        #     raise

        result = func(*args, **kwargs)

        print('[x] After request')

        try:
            db.connection.close()
        except AttributeError:
            pass
        return result

    return wrapper
