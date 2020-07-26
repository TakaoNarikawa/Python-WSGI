import sys
import glob
import os
from collections import namedtuple

import pages
import resource
import utils

fake_imgs = [
    f"../cgi-bin/fake_imgs/{os.path.basename(f)}"
    for f in glob.glob("./fake_imgs/*.jpg")
]

class Application:
    def __init__(self, args):
        self.router = {
            r'.*\.css': resource.Css,
            r'.*\.js' : resource.Js,
            r'.*\.png': resource.Image,
            r'.*\.jpg': resource.Image,

            r'^/$'           : pages.Index,
            r'^/challenge.*$': pages.Challenge,
            r'^/result.*$'   : pages.Result,
            r'^/image.*$'    : pages.FakeImageRecord,
        }
        self.config = args
        self.router = {
            key: cls(config=self.config)
            for key, cls in self.router.items()
        }
        # 正規表現に対応させる
        self.router = utils.RegexDict(self.router)
        self.bad_request = pages.BadRequest(config=self.config)

        print("Application initialized")

    def __call__(self, env, start_response):
        status, headers, body = self.routing(env, start_response)
        start_response(status, headers)
        return [body]

    def routing(self, env, start_response):
        request_path = env.get("PATH_INFO")
        return self.router.get(request_path, self.bad_request)(env)

    def init_db(self, dummy=False):
        utils.init_db(config=self.config, fake_imgs=fake_imgs, dummy=dummy)

