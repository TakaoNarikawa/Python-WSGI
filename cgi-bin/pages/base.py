class BasePage:
    def __init__(self, config):
        self.dbname = config.dbname

    def __call__(self, env):
        body = self.body(env)
        status = self.status()
        header = self.header(content_length=len(body), env=env)
        return status, header, body

    def body(self):
        pass

    def status(self):
        return '200 OK'

    def header(self, content_length, env):
        return [('Content-Type', 'text/html; charset=utf-8'), ('Content-Length', str(content_length))]

    def load_html(self, path, embedding_dict={}):
        with open(path) as f:
            lines = f.readlines()

        html_text = "".join(lines)

        for key, value in embedding_dict.items():
            html_text = html_text.replace(f"%{key}%", str(value))

        return html_text.encode('utf-8')

    def bad_request(self, message="Bad Request"):
        return self.load_html("../static/bad_request.html", embedding_dict={"message": message})