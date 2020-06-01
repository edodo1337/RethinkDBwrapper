from db.utils import DBWrapper, establish_connection
from db.models.user import User



db_wrap = DBWrapper()

db_wrap.setup()


conn = db_wrap.connection
rdb = db_wrap.rdb