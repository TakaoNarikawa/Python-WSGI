#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from app import Router
from wsgiref import simple_server

app = Router()
app.init_db()

def application(env,start_response):
    return app(env, start_response)

if __name__ == '__main__':
    port = 8080
    if len(sys.argv) == 2:
        port = int(sys.argv[1])

    print(f"Python WSGI Server starting...\naddresss: http://localhost:{port}/\n\n")
    server = simple_server.make_server('', port, application)
    server.serve_forever()
