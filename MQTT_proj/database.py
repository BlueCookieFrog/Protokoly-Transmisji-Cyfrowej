import json
import mysql.connector as mysql
import mysql.connector as errorcode


class Database:
    def __init__(self):
        try:
            conf = self._load_config()
            self.db = mysql.connect(
                user=conf["user"],
                password=conf["password"],
                host=conf["host"],
                database=conf["database"],
            )
        except mysql.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Incorrect login or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database doesn't exist")
                if input(f"Create {conf['database']}? (y/n)") == y:
                    self.db = self._create_database()
                else:
                    exit()
            else:
                print(err)
        self.curs = self.db.cursor()

    def _load_config(self) -> dict:
        # try:
        #     # try to open file and load it
        #     with open("config/db_conf.json", "r") as f:
        #         config = json.load(f)
        # except IOError:
        #     print("There is no config file")
        #     exit()
        with open("config/db_conf.json", "r") as f:
            config = json.load(f)

        return config

    def _create_database(self):
        conf = self.load_config()
        db = mysql.connect(
            user=conf["user"], password=conf["password"], host=conf["host"]
        )
        curs = db.cursor()
        try:
            curs.execute(
                f"CREATE DATABASE {conf['database']} DEFAULT CHARACTER SET 'utf8'"
            )
        except mysql.Error as err:
            print(f"Failed creating database: {err}")
            exit()

        return db

    def return_db_obj(self):
        """Returns database objects

        Returns
        -------
        mysql.connector.connect() output
            db object
        cursor
            db curosr
        """
        return self.db, self.curs

    def close_connection(self):
        self.db.close()


if __name__ == "__main__":
    dat = Database()
    db, curs = dat.return_db_obj()
    curs.execute("select * from `conf`")
    curs.execute("select * from `data`")

    dat.close_connection()
