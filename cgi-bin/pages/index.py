# CGIモジュールをインポート
import cgi
import cgitb
cgitb.enable()

# sqlite3（SQLサーバ）モジュールをインポート
import sqlite3

from .base import BasePage

class Index(BasePage):
    def body(self, env):
        return self.load_html("../static/index.html")