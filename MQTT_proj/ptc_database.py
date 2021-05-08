import mysql.connector
from database import Database


class PTC_db(Database):
    def __init__(self):
        super().__init__()

        self.db, self.curs = super().return_db_obj()

    def create_table(self):
        pass
