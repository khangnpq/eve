# coding:utf8
from bitk import PostgreSQLConnector
try:
    from scrapy.utils import project
except:
    pass
class PostgreSQLClient(object):
    def __init__(self, db_name):
        self.settings = project.get_project_settings()  # get settings
        self.POSTGRESQL_HOST = self.settings.get('POSTGRESQL_HOST')
        self.POSTGRESQL_PORT = self.settings.getint('POSTGRESQL_PORT')
        self.POSTGRESQL_USER = self.settings.get('POSTGRESQL_USER')
        self.POSTGRESQL_PASSWD = self.settings.get('POSTGRESQL_PASSWD')
        self.POSTGRESQL_DB = db_name
        self._conn()

    def _conn(self):
        while True:
            try:
                self.db = PostgreSQLConnector()
                self.db.connect(host=self.POSTGRESQL_HOST, port=self.POSTGRESQL_PORT, user=self.POSTGRESQL_USER,
                                password=self.POSTGRESQL_PASSWD, db_name=self.POSTGRESQL_DB)
                break
            except:
                continue
    
    def run_query(self, query):
        self.db.run_query(query)

    def close(self):
        self.db.disconnect()

# class TestDAO(PostgreSQLClient):
#     def __init__(self):
#         super(TestDAO,self).__init__()
#     def queryOne(self):
#         rows = self.db.run_query("SELECT * FROM {}".format(self.POSTGRESQL_DB))
#         if rows:
#             return rows.items()