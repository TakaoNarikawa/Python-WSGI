import re
import sqlite3
import os
import random

class RegexDict(dict):

    def __getitem__(self, item):
        for k, v in self.items():
            if re.match(k, item):
                return v
        raise KeyError
    def get(self, item, optional=None):
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

def get_local_ip_addr():
    ipv4_list = os.popen('ip addr show').read().split("inet ")[1:]
    ipv4_list = [ipv4.split("/")[0] for ipv4 in ipv4_list]
    ipv4_list = [ipv4 for ipv4 in ipv4_list if ipv4 != "127.0.0.1"]

    return ipv4_list[0]

def init_db(config, imgs_fake, dummy=False):
    con = sqlite3.connect(config.dbname)
    cur = con.cursor()

    # 生成画像のリーダーボードに使用するデータベースを作成する
    # データベースをリセットするべきかをチェック
    table_exists, count_matches = True, True
    try:
        check_table_count = 'select count(*) from images'
        cur.execute(check_table_count)

        count = cur.fetchall()[0][0]
        count_matches = len(imgs_fake) == count

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

        # ダミーデータでDBを初期化
        dummy_data = create_dummy_data(n=len(imgs_fake))
        for img, d in zip(imgs_fake, dummy_data):
            img_name      = os.path.splitext(os.path.basename(img))[0]
            try_count     = d.try_count     if dummy else 0
            decieve_count = d.decieve_count if dummy else 0

            insert_row = f'''
                insert into images values
                ("{img_name}", {try_count}, {decieve_count})
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
        dummy_data[i].try_count     += 1
        dummy_data[i].decieve_count += 1 if random.random() > .5 else 0

    return dummy_data