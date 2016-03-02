# coding:utf8
__author__ = 'modm'
import MySQLdb
from scrapy.utils import project


class MysqlClient(object):
    def __init__(self):
        self.settings = project.get_project_settings()  # get settings
        self.MYSQL_HOST = self.settings.get('MYSQL_HOST')
        self.MYSQL_PORT = self.settings.getint('MYSQL_PORT')
        self.MYSQL_USER = self.settings.get('MYSQL_USER')
        self.MYSQL_PASSWD = self.settings.get('MYSQL_PASSWD')
        self.MYSQL_DB = self.settings.get('MYSQL_DB')
        self._conn()

    def _conn(self):
        while True:
            try:
                self.conn = MySQLdb.connect(host=self.MYSQL_HOST, port=self.MYSQL_PORT, user=self.MYSQL_USER,
                                            passwd=self.MYSQL_PASSWD, db=self.MYSQL_DB, charset="utf8")
                break
            except:
                continue

    def _getCursor(self):
        if not self.conn:
            self._conn()
        cur = None
        try:
            cur = self.conn.cursor()
        except:
            self._conn()
        cur = self.conn.cursor()
        return cur

class TestDAO(MysqlClient):
    def __init__(self):
        super(TestDAO,self).__init__()
    def queryOne(self):
        cur=self._getCursor()
        cur.execute("SELECT * FROM test")
        row = cur.fetchone()
        cur.close
        if row:
            return row[0]