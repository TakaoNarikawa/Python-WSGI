import os
import glob
import random
# CGIモジュールをインポート
import cgi
import cgitb
cgitb.enable()

# sqlite3（SQLサーバ）モジュールをインポート
import sqlite3
from pages.base import BasePage
from utils import EasyDict


def optional_parse(s, optional=0):
    if s == None:
        return optional
    try:
        return int(s)
    except ValueError:
        return optional

class FakeImageRecord(BasePage):
    def body(self, env):
        img_id = self.parse(env)

        if img_id is None:
            return self.bad_request("エラー：指定されたパラメータが無効です。")

        # record = {'rank': 20, 'try_count': 0, 'decieve_count': 0, 'decieve_rate': 0}
        record, leader_board_count = self.get_record(img_id)
        if record is None:
            return self.bad_request("エラー：指定されたパラメータが無効です。")

        return self.load_html("../static/fake_image_record.html", embedding_dict={
            "img_id": img_id,
            "leader_board_count": leader_board_count,
            "rank": record.rank,
            "decieve_rate": format(record.decieve_rate, '.4f'),
            "try_count": record.try_count,
            "decieve_count": record.decieve_count
        })

    def parse(self, env):
        request_path = env.get("PATH_INFO")
        store        = cgi.FieldStorage(environ=env, keep_blank_values=True)
        img_id       = store.getvalue("id") if "id" in store else None

        return img_id

    # image_id の record と leader_board の総数を返す
    def get_record(self, image_id):
        con = sqlite3.connect(self.dbname)
        cur = con.cursor()
        con.text_factory = str

        sql = f'''
            select id, try_count, decieve_count,
            IFNULL(CAST(decieve_count as float) / try_count, 0) as decieve_rate
            from images
        '''
        cur.execute(sql)
        leader_board = [
            EasyDict(
                img_id=img_id, try_count=try_count,
                decieve_count=decieve_count, decieve_rate=decieve_rate
            )
            for img_id, try_count, decieve_count, decieve_rate in cur.fetchall()
        ]
        leader_board = {
            d.img_id: EasyDict(
                rank=i+1, try_count=d.try_count,
                decieve_count=d.decieve_count, decieve_rate=d.decieve_rate
            )
            for i, d in enumerate(sorted(leader_board, key=lambda x: -x.decieve_rate))
        }

        cur.close()
        con.close()

        return leader_board.get(image_id, None), len(leader_board)


