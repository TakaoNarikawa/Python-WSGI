import re
import sqlite3
import os
import random
from pprint import pprint

class RegexDict(dict):

    def __getitem__(self, item):
        for k, v in self.items():
            if re.match(k, item):
                return v
        raise KeyError
    def get(self, item, optional):
        try:
            return self[item]
        except:
            return optional


class EasyDict(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        del self[name]

def init_db(config, fake_imgs, dummy=False):
    con = sqlite3.connect(config.dbname)
    cur = con.cursor()

    # 生成画像のリーダーボードに使用するデータベースを作成する
    # データベースをリセットするべきかをチェック
    print(f'fake image count: {len(fake_imgs)}')
    table_exists, count_matches = True, True
    try:
        check_table_count = 'select count(*) from images'
        cur.execute(check_table_count)
        count = cur.fetchall()[0][0]
        count_matches = len(fake_imgs) == count

    except sqlite3.OperationalError:
        # データベースが存在しない
        table_exists = False

    if not (table_exists and count_matches):
        print('rebuilding table ...')
        if table_exists:
            drop_table = 'drop table images'
            cur.execute(drop_table)
            con.commit()

        create_table = '''
            create table if not exists
            images (id varchar(64), try_count int, decieve_count int)
        '''
        cur.execute(create_table)
        con.commit()

        if dummy: # ダミーデータでDBを初期化
            dummy_data = create_dummy_data(n=len(fake_imgs))
            for img, d in zip(fake_imgs, dummy_data):
                img_name = os.path.splitext(os.path.basename(img))[0]
                insert_row = f'''
                    insert into images values ("{img_name}", {d.try_count}, {d.decieve_count})
                '''
                cur.execute(insert_row)
                con.commit()
        else:
            for img in fake_imgs:
                img_name = os.path.splitext(os.path.basename(img))[0]
                insert_row = f'''
                    insert into images values ("{img_name}", 0, 0)
                '''
                cur.execute(insert_row)
                con.commit()

    con.commit()
    cur.close()
    con.close()

def create_dummy_data(n, k=10000):
    dummy_data = [
        EasyDict(try_count=0, decieve_count=0)
        for i in range(n)
    ]
    for i in random.choices(range(n), k=k):
        dummy_data[i].try_count += 1
        if random.random() > .5:
            dummy_data[i].decieve_count += 1

    return dummy_data