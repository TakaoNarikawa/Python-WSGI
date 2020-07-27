import sys
import glob
import os
from collections import namedtuple

import pages
import resource
import utils

class Application:
    def __init__(self, args):
        self.router = {
            r'^/$'           : pages.Index,
            r'^/challenge.*$': pages.Challenge,
            r'^/result.*$'   : pages.Result,
            r'^/image.*$'    : pages.FakeImageRecord,

            r'.*\.css': resource.Css,
            r'.*\.js' : resource.Js,
            r'.*\.png': resource.Image,
            r'.*\.jpg': resource.Image,
        }
        self.config = args
        self.router = {
            key: cls(config=self.config)
            for key, cls in self.router.items()
        }
        # 正規表現に対応させる
        self.router      = utils.RegexDict(self.router)
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
        imgs_fake = [
            f"../cgi-bin/imgs_fake/{os.path.basename(f)}"
            for f in glob.glob("./imgs_fake/*.jpg")
        ]
        utils.init_db(config=self.config, imgs_fake=imgs_fake, dummy=dummy)

