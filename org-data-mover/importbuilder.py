import sys
import os
import logging
import logger
from string import Template
from querybuilder import QueryBuilder


class ImportBuilder(object):

    # C'tor
    def __init__(self):
        logging.debug("Constructing ImportBuilder")
        self.__commands = []

    # Destructor
    def __del__(self):
        pass

    # region Public
    def build_script(self, db_name):
        self.__build_command(db_name, 'componentinstances')
        self.__build_command(db_name, 'environments')
        self.__build_command(db_name, 'environments')
        self.__build_command(db_name, 'projects')
        self.__build_command(db_name, 'testdatas')
        self.__build_command(db_name, 'tests')
        self.__build_command(db_name, 'testsuites')
        self.__build_command(db_name, 'usecases')
        self.__build_command(db_name, 'versions')

        self.__save_script()

    # endregion

    # region Private
    def __build_command(self, db_name, collection_name):
        out_file = self.__get_out_file(collection_name)
        import_command_template = Template("mongoimport --db $db_name --collection $collection_name --file $out_file")
        import_command = import_command_template.substitute(db_name=db_name, out_file=out_file, collection_name=collection_name)
        self.__commands.append(import_command)

    def __save_script(self):
        dir = os.path.dirname(__file__)
        script = os.path.join(dir, 'output', 'import_org.sh')
        with open(script, "w") as f:
            for command in self.__commands:
                f.write(command+os.linesep)

    def __get_out_file(self, collection_name):

        dir = os.path.dirname(__file__)
        file_name = collection_name + ".out"
        # out_file = os.path.join(dir, 'output', file_name)
        # return out_file
        return file_name
    # endregion


def main(argv=[]):

    logger.configure(__file__)
    logging.info("starting importbuilder")
    db_name = argv[1]
    importbuilder = ImportBuilder()
    importbuilder.build_script(db_name)

if __name__ == "__main__":
    main(sys.argv)
