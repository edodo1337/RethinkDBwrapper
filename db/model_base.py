from db.utils import DBConnector, establish_connection
from flask import g
import rethinkdb as r
from .errors import DatabaseProcessError


class MetaModel(type):
    pk = None
    _table_data = None

    def __new__(cls, name, bases, attrs):
        if name.lower() not in ['metamodel', 'rethinkdbmodel']:
            attrs['_table'] = name.lower()
        return type.__new__(cls, name, bases, attrs)

    @property
    def table_data(self):
        return self._table_data

    @table_data.setter
    def table_data(self, data):
        self._table_data = data



class RethinkDBModel(metaclass=MetaModel):
    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)

    @classmethod
    @establish_connection
    def create(cls, **kwargs):
        try:
            db_conn = DBConnector.get_solo()
            rdb = r.RethinkDB()
            # conn = db_conn.get_connection()
            conn = g.rdb_conn

            try:
                db_conn.rdb.table_create(cls._table).run(conn)
            except Exception as e:
                print(f" * [-] Table '{cls._table}' is already exist")

            data = db_conn.rdb.table(cls._table).insert(kwargs).run(conn)
            conn.close()
            obj = cls(**kwargs)
            obj.pk = data['generated_keys'][0]
            return obj

        except:
            print(f" * [-] {cls} object create error error")
            # raise

    @classmethod
    @establish_connection
    def find(cls, id):
        db_conn = DBConnector.get_solo()
        rdb = db_conn.rdb
        # conn = g.rdb_conn
        conn = db_conn.get_connection()
        data = rdb.table(cls._table).get(id).run(conn)
        obj = None
        if data is not None:
            print('data', data)
            obj = cls(**data)

        return obj

    @classmethod
    @establish_connection
    def filter(cls, predicate):
        db_conn = DBConnector.get_solo()
        rdb = db_conn.rdb
        conn = g.rdb_conn
        return list(r.table(cls._table).filter(predicate).run(conn))

    @classmethod
    @establish_connection
    def update(cls, id, fields):
        db_conn = DBConnector.get_solo()
        rdb = db_conn.rdb
        conn = g.rdb_conn
        status = r.table(cls._table).get(id).update(fields).run(conn)
        if status['errors']:
            raise DatabaseProcessError("Could not complete the update action")
        return True

    @classmethod
    @establish_connection
    def delete(cls, id):
        db_conn = DBConnector.get_solo()
        rdb = db_conn.rdb
        conn = g.rdb_conn
        status = r.table(cls._table).get(id).delete().run(conn)
        if status['errors']:
            raise DatabaseProcessError("Could not complete the delete action")
        return True