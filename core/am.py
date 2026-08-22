class AM:   # APP manager
    def __init__(self):
        self.apps = {}

    def register(self, app_name, app):
        self.apps[app_name] = app

    def get(self, app_name):
        return self.apps.get(app_name, object)

am = AM()