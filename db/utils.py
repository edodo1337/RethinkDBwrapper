from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
import inspect
import sys

class DBWrapper:
    RDB_HOST = None
    RDB_PORT = None
    APP_DB = None
    __rdb = None
    __connection = None

    __instance = None

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
        self.__connection = r.connect(host=self.RDB_HOST, port=self.RDB_PORT)
        try:
            r.db_create(self.APP_DB).run(self.__connection)
            print(f' * [x] Database "{self.APP_DB}" created')
        except RqlRuntimeError:
            print(f' * [-] Database "{self.APP_DB}" is already exist.')
        finally:
            self.__rdb = r.db(self.APP_DB)
            self.__connection.close()



    def init_tables(self):
        import db.models
        a = [m[0].lower() for m in inspect.getmembers(db.models, inspect.isclass)]
        # a[0].init_table()
        self.table_create(a[0])


    def table_create(self, table_name):
        print('here')
        conn = self.connection
        try:
            self.__rdb.table_create(table_name).run(conn)
            print(f' * [x] Table "{table_name}" created')
        except RqlRuntimeError:
            print(f' * [-] Table "{table_name}" is already exist.')
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
        return self.__rdb

    @classmethod
    def get_solo(cls):
        if not cls.__instance:
            cls.__instance = DBWrapper()
        return cls.__instance


def establish_connection(func):
    def wrapper(*args, **kwargs):
        db = DBWrapper.get_solo()
        print('[x] Before request')
        try:
            db.connection = db.get_connection()
        except RqlDriverError:
            raise

        result = func(*args, **kwargs)

        print('[x] After request')
        try:
            db.connection.close()
        except AttributeError:
            pass
        return result

    return wrapper
