#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
# CGIモジュールをインポート
import cgi
import cgitb
cgitb.enable()

# sqlite3（SQLサーバ）モジュールをインポート
import sqlite3

# データベースファイルのパスを設定
dbname = 'database.db'
#dbname = ':memory:'

# テーブルの作成
con = sqlite3.connect(dbname)
cur = con.cursor()
create_table = 'create table if not exists users (id int, name varchar(64))'
cur.execute(create_table)
con.commit()
cur.close()
con.close()

def load_html(path, embedding_dict={}):
    with open(path) as f:
        lines = f.readlines()

    html_text = "".join(lines)

    for key, value in embedding_dict.items():
        html_text = html_text.replace(f"%{key}%", value)

    return html_text.encode('utf-8')

def render_login_form(environ):
    # フォームデータを取得
    form = cgi.FieldStorage(environ=environ,keep_blank_values=True)
    if ('v1' not in form) or ('v2' not in form):
        # 入力フォームの内容が空の場合（初めてページを開いた場合も含む）
        # HTML（入力フォーム部分）
        body = '''
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
        con = sqlite3.connect(dbname)
        cur = con.cursor()
        con.text_factory = str

        # SQL文（insert）の作成と実行
        sql = 'insert into users (id, name) values (?,?)'
        cur.execute(sql, (int(v1),v2))
        con.commit()

        # SQL文（select）の作成
        sql = 'select * from users'

        # SQL文の実行とその結果のHTML形式への変換
        body = '''
            <div class="ol1">
                <ol>
        '''
        for row in cur.execute(sql):
            body += '<li>' + str(row[0]) + ',' + row[1] + '</li>\n'
        body += '''
                </ol>
            </div>
            <a href="/">登録ページに戻る</a>
        '''

        # カーソルと接続を閉じる
        cur.close()
        con.close()

    return body

def application(environ,start_response):
    html = load_html("static/index.html", embedding_dict={
        "login_form": render_login_form(environ)
    })

    # レスポンス
    start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8'),
        ('Content-Length', str(len(html))) ])
    return [html]


# リファレンスWEBサーバを起動
#  ファイルを直接実行する（python3 test_wsgi.py）と，
#  リファレンスWEBサーバが起動し，http://localhost:8080 にアクセスすると
#  このサンプルの動作が確認できる．
#  コマンドライン引数にポート番号を指定（python3 test_wsgi.py ポート番号）した場合は，
#  http://localhost:ポート番号 にアクセスする．
from wsgiref import simple_server
if __name__ == '__main__':
    port = 8080
    if len(sys.argv) == 2:
        port = int(sys.argv[1])

    print(f"Python WSGI Server starting...\naddresss: http://localhost:{port}/\n\n")
    server = simple_server.make_server('', port, application)
    server.serve_forever()
