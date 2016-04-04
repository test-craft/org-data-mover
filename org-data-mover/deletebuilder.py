import sys
import os
import logger
import logging
from string import Template
from querybuilder import QueryBuilder


class DeleteBuilder(object):

    # C'tor
    def __init__(self, query_builder):
        logging.debug("Constructing DeleteBuilder")
        self.__query_builder = query_builder
        self.__commands = []

    # Destructor
    def __del__(self):
        pass

    # region Public
    def build_script(self, db_name):
        self.__build_command('componentinstances', 'versionId')
        self.__build_command('environments', 'projectId')
        self.__build_command('environments', 'projectId')
        self.__build_command('projects', 'projectId')
        self.__build_command('testdatas', 'versionId')
        self.__build_command('tests', 'versionId')
        self.__build_command('testsuites', 'versionId')
        self.__build_command('usecases', 'versionId')
        self.__build_command('versions', 'projectId')

        self.__save_script(db_name)

    # endregion

    # region Private
    def __build_command(self, collection_name, field):
        in_clause = self.__get_in_clause(field)
        delete_command_template = Template("db.$collection_name.remove({'$field': {'$$in' : [$in_clause]} })")
        delete_command = delete_command_template.substitute(field=field, in_clause=in_clause, collection_name=collection_name)
        self.__commands.append(delete_command)

    def __save_script(self, db_name):

        dir = os.path.dirname(__file__)
        script = os.path.join(dir, 'output', 'delete_org.js')
        with open(script, "w") as f:
            f.write('db = db.getSiblingDB(\'' + db_name + '\')' + os.linesep)
            for command in self.__commands:
                f.write(command+os.linesep)

    def __get_in_clause(self, in_clause_field):

        in_arr = []
        if in_clause_field == 'versionId':
            in_arr = self.__query_builder.get_versions()
        if in_clause_field == 'projectId':
            in_arr = self.__query_builder.get_projects()
        in_clause = ','.join('\'{0}\''.format(w) for w in in_arr)
        return in_clause

    # endregion

def main(argv=[]):

    logger.configure(__file__)
    logging.info("starting deletebuilder")
    db_name = argv[1]
    org_id = argv[2]
    mongo_uri = argv[3]
    query_builder = QueryBuilder(db_name, org_id, mongo_uri)
    query_builder.set_projects()
    query_builder.set_versions()
    deletebuilder = DeleteBuilder(query_builder)
    deletebuilder.build_script(db_name)

if __name__ == "__main__":
    main(sys.argv)
