from .base import BasePage

class BadRequest(BasePage):
    def body(self, env):
        return self.load_html("../static/bad_request.html")
    def status(self):
        return '400 Bad Request'