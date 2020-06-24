# CGIモジュールをインポート
import cgi
import cgitb
cgitb.enable()

# sqlite3（SQLサーバ）モジュールをインポート
import sqlite3

from .base import BasePage

import random
import string

def random_string(n=16):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(n))


class Index(BasePage):
    def body(self, env):
        gen_id = random_string()
        return self.load_html("../static/index.html", embedding_dict={"id": gen_id})