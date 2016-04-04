from customexceptions import *
import logging
from singleton import *
from pymongo import MongoClient


class MongoClientWrapper:
    __metaclass__ = Singleton

    # C'tor
    def __init__(self, mongo_uri):
        self.__mongo_uri = mongo_uri
        self.__client = None
        logging.debug("Constructing MongoClient")

    # Destructor
    def __del__(self):
        logging.debug("Destructing MongoClient")

    # Public

    def get_client(self):
        if self.__client is None:
            self.__init_client()
        return self.__client

    # Private
    def __init_client(self):

        try:
            self.__client = MongoClient(self.__mongo_uri)
        except Exception, ex:
            logging.debug(str(ex))
            raise UnableToCreateMongoClient(str(ex))


if __name__ == "__main__":
    mongoclientwrapper = MongoClientWrapper('mongodb://localhost:27017/')
    client = mongoclientwrapper.get_client()
    db = client['testcraft-dev']
    print db