#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from app import Application
from wsgiref import simple_server

import utils

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='2020春学期 コンピュータ科学科実験 WSGI 課題')
    parser.add_argument('--port', type=int, default=8080,
                        help='WSGIサーバーで使用するポート')
    parser.add_argument('--dbname', type=str, default='database.db',
                        help='データベースのファイル名')
    args = parser.parse_args()

    app = Application(args)
    app.init_db()

    application = lambda env, start_response: app(env, start_response)
    ip_addr = utils.get_local_ip_addr()

    print(f"\nStarting Python WSGI Server ...")
    print(f"addresss: http://localhost:{args.port}")
    print(f"local address: http://{ip_addr}:{args.port}/\n\n")

    server = simple_server.make_server('', args.port, application)
    server.serve_forever()
