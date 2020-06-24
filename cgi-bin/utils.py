import re

class RegexDict(dict):

    # def __init__(self):
    #     super(RegexDict, self).__init__()

    def __getitem__(self, item):
        for k, v in self.items():
            if re.match(k, item):
                return v
        raise KeyError
    def get(self, item, optional):
        try:
            return self[item]
        except:
            return optional

if __name__ == "__main__":
    router = {
        r'^/$': "index",
        r'.*\.css': "Static",
        r'.*\.png': "Static",
        r'.*\.jpg': "Static",
        r'.*\.js': "Static"
    }
    router = RegexDict(router)

    print(router)
    print("/css/style.css", router.get("/css/style.css", "bad_req"))
    print("/", router.get("/", "bad_req"))