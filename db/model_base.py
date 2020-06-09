from db.utils import DBWrapper, establish_connection
from flask import g
from rethinkdb import RethinkDB
from .errors import DatabaseProcessError


class MetaModel(type):
    pk = None

    def __new__(cls, name, bases, attrs):
        if name.lower() not in ['metamodel', 'rethinkdbmodel']:
            attrs['_table'] = name.lower()
        return type.__new__(cls, name, bases, attrs)

    @property
    def table(self):
        return self._table


class RethinkDBModel(metaclass=MetaModel):
    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)

    # @classmethod
    # def init_table(cls):
    #     if cls.__name__.lower() not in ['metamodel', 'rethinkdbmodel']:
    #         print(cls.__name__.lower())

    @classmethod
    @establish_connection
    def create(cls, **kwargs):
        try:
            db_wrap = DBWrapper.get_solo()
            conn = db_wrap.connection

            try:
                db_wrap.rdb.table_create(cls._table).run(conn)
            except Exception as e:
                print(f" * [-] Table '{cls._table}' is already exist")

            data = db_wrap.rdb.table(cls._table).insert(kwargs).run(conn)
            conn.close()
            obj = cls(**kwargs)
            obj.pk = data['generated_keys'][0]
            return obj

        except:
            print(f" * [-] {cls} object create error error")
            # raise

    @classmethod
    @establish_connection
    def get(cls, id):
        db_wrap = DBWrapper.get_solo()
        rdb = db_wrap.rdb
        # conn = g.rdb_conn
        conn = db_wrap.connection
        data = rdb.table(cls._table).get(id).run(conn)
        obj = None
        if data is not None:
            print('data', data)
            obj = cls(**data)

        return obj

    @classmethod
    @establish_connection
    def filter(cls, predicate, fields=None):
        db_wrap = DBWrapper.get_solo()
        rdb = db_wrap.rdb
        # conn = g.rdb_conn
        conn = db_wrap.connection
        print("HERE", fields)
        if fields:
            print('here')
            return list(rdb.table(cls._table).filter(predicate).pluck(fields).run(conn))
        return list(rdb.table(cls._table).filter(predicate).run(conn))

    @classmethod
    @establish_connection
    def all(cls):
        db_wrap = DBWrapper.get_solo()
        rdb = db_wrap.rdb
        # conn = g.rdb_conn
        conn = db_wrap.connection

        return list(rdb.table(cls._table).run(conn))

    @classmethod
    @establish_connection
    def update(cls, id, fields):
        db_conn = DBWrapper.get_solo()
        rdb = db_conn.rdb
        conn = g.rdb_conn
        status = r.table(cls._table).get(id).update(fields).run(conn)
        if status['errors']:
            raise DatabaseProcessError("Could not complete the update action")
        return True

    @classmethod
    @establish_connection
    def delete(cls, id):
        db_conn = DBWrapper.get_solo()
        rdb = db_conn.rdb
        conn = g.rdb_conn
        status = r.table(cls._table).get(id).delete().run(conn)
        if status['errors']:
            raise DatabaseProcessError("Could not complete the delete action")
        return True
