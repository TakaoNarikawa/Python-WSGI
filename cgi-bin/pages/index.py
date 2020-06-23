# CGIモジュールをインポート
import cgi
import cgitb
cgitb.enable()

# sqlite3（SQLサーバ）モジュールをインポート
import sqlite3

from .base import BasePage

class Index(BasePage):
    def body(self, env):
        form = cgi.FieldStorage(environ=env,keep_blank_values=True)
        if ('v1' not in form) or ('v2' not in form):
            # 入力フォームの内容が空の場合（初めてページを開いた場合も含む）
            # HTML（入力フォーム部分）
            login_form = '''
            <div class="form1">
                <form>
                    学生番号（整数） <input type="text" name="v1"><br>
                    氏名　（文字列） <input type="text" name="v2"><br>
                    <input type="submit" value="登録" />
                </form>
            </div>
            '''
        else:
            # 入力フォームの内容が空でない場合
            # フォームデータから各フィールド値を取得
            v1 = form.getvalue("v1", "0")
            v2 = form.getvalue("v2", "0")

            # データベース接続とカーソル生成
            con = sqlite3.connect(self.dbname)
            cur = con.cursor()
            con.text_factory = str

            # SQL文（insert）の作成と実行
            sql = 'insert into users (id, name) values (?,?)'
            cur.execute(sql, (int(v1),v2))
            con.commit()

            # SQL文（select）の作成
            sql = 'select * from users'

            # SQL文の実行とその結果のHTML形式への変換
            login_form = '''
                <div class="ol1">
                    <ol>
            '''
            for row in cur.execute(sql):
                login_form += '<li>' + str(row[0]) + ',' + row[1] + '</li>\n'
            login_form += '''
                    </ol>
                </div>
                <a href="/">登録ページに戻る</a>
            '''

            # カーソルと接続を閉じる
            cur.close()
            con.close()

        return self.load_html("../static/index.html", embedding_dict={"login_form": login_form})