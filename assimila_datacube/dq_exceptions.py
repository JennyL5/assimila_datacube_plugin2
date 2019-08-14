"""
Exception classes for the datacube
"""


class GDALError(Exception):
    def __init__(self, message):
        self.message = message

    def __del__(self):
        pass

    def __str__(self):
        return repr(self.message)


class DQError(Exception):
    def __init__(self, message):
        self.message = message

    def __del__(self):
        pass

    def __str__(self):
        return repr(self.message)


class DQServerError(Exception):
    def __init__(self, message):
        self.message = message

    def __del__(self):
        pass

    def __str__(self):
        return repr(self.message)


class DQServerFatal(Exception):
    def __init__(self, message):
        self.message = message

    def __del__(self):
        pass

    def __str__(self):
        return repr(self.message)


class DBError(Exception):
    def __init__(self, message):
        self.message = message

    def __del__(self):
        pass

    def __str__(self):
        return repr(self.message)