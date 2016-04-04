import logging
from mongoclientwrapper import MongoClientWrapper


class QueryBuilder(object):

    # C'tor
    def __init__(self, db_name, org_id, mongo_uri):

        logging.debug("Constructing MongoClientWrapper")
        self.__db_name = db_name
        self.__org_id = org_id
        self.__projects = []
        self.__versions = []

        mongo_client_wrapper = MongoClientWrapper(mongo_uri)
        self.__mongo_client = mongo_client_wrapper.get_client()

    # Destructor
    def __del__(self):
        pass

    # region Public
    def set_projects(self):
        db = self.__mongo_client[self.__db_name]
        for project in db.projects.find({"organizationId": self.__org_id}):
            print project['projectId']
            self.__projects.append(project['projectId'])

    def set_versions(self):
        db = self.__mongo_client[self.__db_name]
        for version in db.versions.find({'projectId': {'$in': self.__projects}}):
            print version['versionId']
            self.__versions.append(version['versionId'])

    def get_projects(self):
        return self.__projects

    def get_versions(self):
        return self.__versions

    # endregion

if __name__ == "__main__":
    query_builder = QueryBuilder('testcraft-dev', '1000612', 'mongodb://localhost:27017/')
    query_builder.set_projects()
    query_builder.set_versions()
