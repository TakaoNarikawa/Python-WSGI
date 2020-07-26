import random
import string
import cgi
import cgitb
import sqlite3

from pages.base import BasePage
from utils import EasyDict

cgitb.enable()

def random_string(n=16):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(n))


class Index(BasePage):
    def body(self, env):
        gen_id       = random_string()
        leader_board = self.create_leader_board()

        return self.load_html("../static/index.html", embedding_dict={
            "id": gen_id,
            "leader_board": leader_board
        })

    def create_leader_board(self, limit=10):
        con = sqlite3.connect(self.dbname)
        cur = con.cursor()
        con.text_factory = str

        sql = f'''
            select id, try_count, decieve_count,
            IFNULL(CAST(decieve_count as float) / try_count, 0) as decieve_rate
            from images
        '''
        cur.execute(sql)

        # データベースの内容を取得
        leader_board = [
            EasyDict(
                img_id=img_id, try_count=try_count,
                decieve_count=decieve_count, decieve_rate=decieve_rate
            )
            for img_id, try_count, decieve_count, decieve_rate in cur.fetchall()
        ]
        # ランクの情報を追加
        leader_board = [
            self.create_leader_board_row(rank=i+1, **d)
            for i, d in enumerate(sorted(leader_board, key=lambda x: -x.decieve_rate))
        ]
        # 表示数を制限
        leader_board = leader_board[:limit]

        cur.close()
        con.close()

        return ''.join(leader_board)

    def create_leader_board_row(self, rank, img_id, try_count, decieve_count, decieve_rate):
        return f'''
            <tr>
              <th>{rank}</th>
              <td>{format(decieve_rate, '.2f')}</td>
              <td>{try_count}</td>
              <td>{decieve_count}</td>
              <td><a href="image?id={img_id}">Link</a></td>
            </tr>
        '''