import repr


class UnableToCreateMongoClient(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr.repr('Unable to create Mongo Client: {0}'.format(self.value))
