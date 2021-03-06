import cgi
import cgitb
import sqlite3
import os

from pages.base import BasePage

cgitb.enable()

class Static(BasePage):
    def body(self, env):
        request_path = env.get("PATH_INFO")

        try:
            with open(f"..{request_path}") as f:
                static = f.read().encode('utf-8')
        except Exception as e:
            raise (e)

        return static

class Css(Static):
    def header(self, content_length, env):
        return [
            ('Content-Type', 'text/css; charset=utf-8'),
            ('Content-Length', str(content_length))
        ]

class Js(Static):
    def header(self, content_length, env):
        return [
            ('Content-Type', 'application/javascript; charset=utf-8'),
            ('Content-Length', str(content_length))
        ]

class Image(BasePage):
    def body(self, env):
        request_path = env.get("PATH_INFO")
        try:
            with open(f"..{request_path}", "rb") as f:
                static = f.read()
        except Exception as e:
            raise (e)

        return static

    def header(self, content_length, env):
        request_path = env.get("PATH_INFO")
        ext = os.path.splitext(request_path)[1][1:]
        return [
            ('Content-Type', f'image/{ext}'),
            ('Content-Length', str(os.stat(f"..{request_path}").st_size))
        ]