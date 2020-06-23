class BasePage:
    def __init__(self, config):
        self.dbname = config.dbname

    def __call__(self, env):
        body = self.body(env)
        status = self.status()
        header = self.header(content_length=len(body))
        print(status)
        return status, header, body

    def body(self):
        pass

    def status(self):
        return '200 OK'

    def header(self, content_length):
        return [('Content-Type', 'text/html; charset=utf-8'), ('Content-Length', str(content_length))]

    def load_html(self, path, embedding_dict={}):
        with open(path) as f:
            lines = f.readlines()

        html_text = "".join(lines)

        for key, value in embedding_dict.items():
            html_text = html_text.replace(f"%{key}%", value)

        return html_text.encode('utf-8')