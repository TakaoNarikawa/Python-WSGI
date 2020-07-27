#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import zipfile
import argparse
from wsgiref import simple_server

from app import Application
import utils

def run(args):
    app = Application(args)
    app.init_db(dummy=not args.without_dummy)

    application = lambda env, start_response: app(env, start_response)
    ip_addr = utils.get_local_ip_addr()

    print(f"\nStarting Python WSGI Server ...")
    print(f"addresss: http://localhost:{args.port}")
    print(f"local address: http://{ip_addr}:{args.port}/\n\n")

    server = simple_server.make_server('', args.port, application)
    server.serve_forever()

def prepare_imgs():
    if not os.path.isdir("imgs_real"):
        with zipfile.ZipFile('imgs_real.zip') as existing_zip:
            existing_zip.extractall('./')
    if not os.path.isdir("imgs_fake"):
        with zipfile.ZipFile('imgs_fake.zip') as existing_zip:
            existing_zip.extractall('./')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='2020春学期 コンピュータ科学科実験 WSGI 課題')
    parser.add_argument('--port', type=int, default=8080,
                        help='WSGIサーバーで使用するポート')
    parser.add_argument('--dbname', type=str, default='database.db',
                        help='データベースのファイル名')
    parser.add_argument('--without-dummy', action='store_true',
                        help='ダミーデータを使用しない')

    args = parser.parse_args()

    prepare_imgs()
    run(args)

