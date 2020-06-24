import sys
from collections import namedtuple
from pages.index import Index
from pages.challenge import Challenge, Result
from pages.bad_request import BadRequest
from resource import Static, Image, Css, Js
# sqlite3（SQLサーバ）モジュールをインポート
import sqlite3
from utils import RegexDict

Config = namedtuple("Config", "dbname")
config = Config(dbname="database.db")


class Router:
    def __init__(self):
        self.router = {
            r'.*\.css': Css,
            r'.*\.js': Js,
            r'.*\.png': Image,
            r'.*\.jpg': Image,

            r'^/$': Index,
            r'^/challenge.*$': Challenge,
            r'^/result.*$': Result,
        }
        self.router = {key: cls(config=config) for key, cls in self.router.items()}
        self.router = RegexDict(self.router)
        self.bad_request = BadRequest(config=config)

        print("Router initialized")

    def __call__(self, env, start_response):
        status, headers, body = self.routing(env, start_response)
        start_response(status, headers)
        return [body]

    def routing(self, env, start_response):
        request_path = env.get("PATH_INFO")
        return self.router.get(request_path, self.bad_request)(env)

    def init_db(self):
        con = sqlite3.connect(config.dbname)
        cur = con.cursor()
        create_table = 'create table if not exists users (id int, name varchar(64))'
        cur.execute(create_table)
        con.commit()
        cur.close()
        con.close()

