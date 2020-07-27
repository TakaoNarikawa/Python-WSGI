import os
import glob
import random
import cgi
import cgitb
import sqlite3

from pages.base import BasePage

cgitb.enable()

imgs_real = [
    f"../cgi-bin/imgs_real/{os.path.basename(f)}"
    for f in glob.glob("./imgs_real/*.jpg")
]
imgs_fake = [
    f"../cgi-bin/imgs_fake/{os.path.basename(f)}"
    for f in glob.glob("./imgs_fake/*.jpg")
]

def optional_parse(s, optional=0):
    if s == None:
        return optional
    try:
        return int(s)
    except ValueError:
        return optional

class Challenge(BasePage):
    def parse(self, env):
        request_path = env.get("PATH_INFO")
        store = cgi.FieldStorage(environ=env, keep_blank_values=True)

        ans     = store.getvalue("ans") if "ans" in store else None
        user_id = store.getvalue("id")  if "id"  in store else None
        n       = store.getvalue("n")   if "n"   in store else None
        i       = store.getvalue("i")   if "i"   in store else None

        n = optional_parse(n, optional=None)
        i = optional_parse(i, optional=0)

        return ans, user_id, n, i

    # i      : 問題のインデックス, i=0->回答0, i=3->回答3
    # n      : 全問題数, n=5,10,50
    # ans    : i-1における回答, ans="A", "B"
    # user_id: 回答者に毎回ランダムに割り当てられるid
    def body(self, env):
        ans, user_id, n, i = self.parse(env)

        if (not (user_id != None and n != None and i < n)) or (i > 0 and ans == None):
            return self.bad_request("エラー：指定されたパラメータが無効です。")

        a_selected = ans == "A"

        con = sqlite3.connect(self.dbname)
        cur = con.cursor()
        con.text_factory = str

        # 初回時、回答結果を保持するためのデータベースを作成する
        # 予め回答結果を初期化しておく
        if i == 0:
            try:
                create_table = f'''
                    create table
                    if not exists {user_id}
                    (i int, pred int, true int, img_a varchar(30), img_b varchar(30));
                '''
                cur.execute(create_table)
                con.commit()

                for j, (real_img, fake_img) in enumerate(zip(random.sample(imgs_real, n), random.sample(imgs_fake, n))):
                    true_v = 1 if random.random() > .5 else 0
                    insert_value = f'''
                        insert into {user_id} values
                        (
                            {j+1},
                            0,
                            {true_v},
                            "{real_img if true_v == 0 else fake_img}",
                            "{real_img if true_v == 1 else fake_img}"
                        );
                    '''
                    cur.execute(insert_value)
                    con.commit()
            except sqlite3.OperationalError:
                pass

        # i > 0 の時、URLパラメータで前回の回答が含まれるはずなので、その内容をデータベースに書き込む
        else:
            update_value = f'update {user_id} set pred = {0 if a_selected else 1} where i = {i};'
            try:
                cur.execute(update_value)
                con.commit()
            except sqlite3.OperationalError(e):
                return self.bad_request("エラー：指定IDのデータベースが見つかりませんでした。")

            con.commit()

        next_href_a = f"{'challenge' if i < n-1 else 'result'}?n={n}&i={i+1}&id={user_id}&ans=A"
        next_href_b = f"{'challenge' if i < n-1 else 'result'}?n={n}&i={i+1}&id={user_id}&ans=B"

        # 表示する画像の指定
        get_view_info = f'select * from {user_id} where i = {i+1}'
        cur.execute(get_view_info)
        [i, pred, true, img_a, img_b] = cur.fetchall()[0]

        cur.close()
        con.close()

        return self.load_html("../static/challenge.html", embedding_dict={
            "img_a"      : img_a,
            "img_b"      : img_b,
            "next_href_a": next_href_a,
            "next_href_b": next_href_b,
            "i"          : i,
            "n"          : n
        })

class Result(Challenge):
    def create_row(self, pred, true, img_a, img_b):
        a_class_name = "selected-img" if pred == 0 else ""
        b_class_name = "selected-img" if pred == 1 else ""
        a_mark       = '◯'            if true == 0 else '×'
        b_mark       = '◯'            if true == 1 else '×'

        result_text  = '正解'          if true == pred else '不正解'

        return f'''
        <div class="row">
          <div class="col-xs-12 col-sm-12 col-md-6 col-lg-6 col-xl-6">
            <div class="each-services">
              <img class="{a_class_name}" src="{img_a}" />
            </div>
            <h2>{a_mark}</h2>
          </div>
          <div class="col-xs-12 col-sm-12 col-md-6 col-lg-6 col-xl-6">
            <div class="each-services">
              <img class="{b_class_name}" src="{img_b}" />
            </div>
            <h2>{b_mark}</h2>
          </div>
        </div>
        <h3>{result_text}</h3>
        '''

    # FIXME: ページを読み込み治すと新たに結果が追加されてしまう
    def update_fake_img_leader_board(self, fake_img_res, cur, con):
        update_leader_board = ''
        for img_path, correct in fake_img_res:
            img_id = os.path.splitext(os.path.basename(img_path))[0]
            update_leader_board += f'''
                UPDATE images SET try_count=try_count+1
                where images.id == "{img_id}";
            '''
            # 正しくない場合は decieve_count も増やす
            if not correct:
                update_leader_board += f'''
                UPDATE images SET decieve_count=decieve_count+1
                where images.id == "{img_id}";
                '''
        cur.executescript(update_leader_board)
        con.commit()

    def body(self, env):
        ans, user_id, n, i = self.parse(env)

        if (not (user_id != None and n != None and i == n)) or (i > 0 and ans == None):
            return self.bad_request("エラー：指定されたパラメータが無効です。")

        a_selected = ans == "A"

        con = sqlite3.connect(self.dbname)
        cur = con.cursor()
        con.text_factory = str

        sql = f'update {user_id} set pred = {0 if a_selected else 1} where i = {i};'
        try:
            cur.execute(sql)
            con.commit()
        except sqlite3.OperationalError:
            return self.bad_request("エラー：指定IDのデータベースが見つかりませんでした。")
        con.commit()

        # DBから読み込んで、結果を表示
        sql = f'select * from {user_id}'
        cur.execute(sql)
        res = cur.fetchall()

        # 生成画像のリーダーボードで使用するためのデータを用意
        # (画像のパス, 正誤)
        fake_image_res = [
            (
                img_b if true == 0 else img_a,
                pred == true
            )
            for _, pred, true, img_a, img_b in res
        ]
        self.update_fake_img_leader_board(fake_image_res, cur, con)

        # 結果画面で表示する テーブル を作成
        # HTML のリストを作成 → joinで結合
        result_list = [
            self.create_row(pred=pred, true=true, img_a=img_a, img_b=img_b)
            for _, pred, true, img_a, img_b in res
        ]
        result_list = ''.join(result_list)

        correct_n = len([0 for row in res if row[1] == row[2]])
        all_n     = len(res)
        acc       = correct_n / all_n

        return self.load_html("../static/result.html", embedding_dict={
            "result_list": result_list,
            "acc"        : acc * 100,
            "correct"    : correct_n,
            "n"          : n,
        })



