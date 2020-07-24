from pages.base import BasePage

class BadRequest(BasePage):
    def body(self, env):
        return self.load_html("../static/bad_request.html", embedding_dict={"message": "Bad Request"})
    def status(self):
        return '400 Bad Request'