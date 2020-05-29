from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from flask import g, request, abort, current_app


class DBConnector:
    connection = None
    RDB_HOST = None
    RDB_PORT = None
    APP_DB = None
    app = None
    rdb = None

    __instance = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DBConnector, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        pass

    def init_app(self, app):
        self.RDB_HOST = current_app.config.get('RDB_HOST', 'localhost')
        self.RDB_PORT = current_app.config.get('RDB_PORT', 28015)
        self.APP_DB = current_app.config.get('APP_DB', 'test_db')
        self.app = app
        self.dbSetup()
        # self.request_handling()

    def dbSetup(self):
        r = RethinkDB()
        self.connection = r.connect(host=self.RDB_HOST, port=self.RDB_PORT)
        try:
            r.db_create(self.APP_DB).run(self.connection)
            # self.rdb.db(self.APP_DB).table_create('items').run(connection)
            print(f' * [x] Database "{self.APP_DB}" created')
        except RqlRuntimeError:
            print(f' * [-] Database "{self.APP_DB}" is already exist.')
        finally:
            self.rdb = r.db(self.APP_DB)
            self.connection.close()

    def request_handling(self):
        @current_app.before_request
        def before_request():
            print('[x] Before request')
            try:
                g.rdb_conn = self.rdb.connect(host=self.RDB_HOST, port=self.RDB_PORT, db=self.APP_DB)
            except RqlDriverError:
                abort(503, "No database connection could be established.")

        @current_app.teardown_request
        def teardown_request(exception):
            print('[x] After request')

            try:
                g.rdb_conn.close()
            except AttributeError:
                pass

    @classmethod
    def get_connection(cls, new=False):
        if new or not cls.connection:
            pass
            # cls.connection = DBConnector().create_connection()
        r = RethinkDB()
        cls.connection = r.connect(host=cls.RDB_HOST, port=cls.RDB_PORT)
        return cls.connection

    @classmethod
    def get_solo(cls):
        if not cls.__instance:
            cls.__instance = DBConnector()
        return cls.__instance


def establish_connection(func):
    def wrapper(*args, **kwargs):
        db = DBConnector.get_solo()
        print('[x] Before request')
        try:
            # g.rdb_conn = db.rdb.connect(host=db.RDB_HOST, port=db.RDB_PORT, db=db.APP_DB)
            # g.rdb_conn = db.get_connection( )
            db.connection = db.get_connection()
        except RqlDriverError:
            abort(503, "No database connection could be established.")

        result = func(*args, **kwargs)

        print('[x] After request')
        try:
            g.rdb_conn.close()
        except AttributeError:
            pass
        return result

    return wrapper
