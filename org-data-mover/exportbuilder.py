import sys
import os
import logger
import logging
from string import Template
from querybuilder import QueryBuilder


class ExportBuilder(object):

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
        self.__build_command(db_name, 'componentinstances', 'versionId')
        self.__build_command(db_name, 'environments', 'projectId')
        self.__build_command(db_name, 'environments', 'projectId')
        self.__build_command(db_name, 'projects', 'projectId')
        self.__build_command(db_name, 'testdatas', 'versionId')
        self.__build_command(db_name, 'tests', 'versionId')
        self.__build_command(db_name, 'testsuites', 'versionId')
        self.__build_command(db_name, 'usecases', 'versionId')
        self.__build_command(db_name, 'versions', 'projectId')

        self.__save_script()

    # endregion

    # region Private
    def __build_command(self, db_name, collection_name, field):
        #mongoexport --db test --collection traffic --out traffic.json --query '{ a: { $gte: 3 } }'
        in_clause = self.__get_in_clause(field)
        out_file = self.__get_out_file(collection_name)
        export_command_template = Template("mongoexport --db $db_name  --collection $collection_name --out $out_file --query \"{'$field': {'$$in' : [$in_clause]} }\"")
        export_command = export_command_template.substitute(db_name=db_name, out_file=out_file, field=field, in_clause=in_clause, collection_name=collection_name)
        self.__commands.append(export_command)

    def __save_script(self):

        dir = os.path.dirname(__file__)
        script = os.path.join(dir, 'output', 'export_org.sh')
        with open(script, "w") as f:
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

    def __get_out_file(self, collection_name):

        dir = os.path.dirname(__file__)
        file_name = collection_name + ".out"
        out_file = os.path.join(dir, 'output', file_name)
        return out_file

    # endregion


def main(argv=[]):

    logger.configure(__file__)
    logging.info("starting exportbuilder")
    db_name = argv[1]
    org_id = argv[2]
    mongo_uri = argv[3]
    query_builder = QueryBuilder(db_name, org_id, mongo_uri)
    query_builder.set_projects()
    query_builder.set_versions()
    exportbuilder = ExportBuilder(query_builder)
    exportbuilder.build_script(db_name)

if __name__ == "__main__":
    main(sys.argv)