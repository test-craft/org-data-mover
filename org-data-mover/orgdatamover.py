import sys
import logger
import logging
import argparse
from querybuilder import QueryBuilder
from exportbuilder import ExportBuilder
from importbuilder import ImportBuilder
from deletebuilder import DeleteBuilder


def main(argv=[]):

    logger.configure(__file__)
    logging.info("starting the orgdatamover")
    parser = argparse.ArgumentParser(prog='orgdatamover')
    parser.add_argument('--source-db-name', dest='source_db_name', help='source DB Name')
    parser.add_argument('--source-mongo-uri', dest='source_mongo_uri', help='source Mongo URI of the following form: <server>:port -> localhost:27017')
    parser.add_argument('--target-db-name', dest='target_db_name', help='target DB Name')
    parser.add_argument('--org-id', dest='org_id', help='organization id')

    args = parser.parse_args()
    source_db_name = args.source_db_name
    source_mongo_uri = 'mongodb://{0}/'.format(args.source_mongo_uri)
    target_db_name = args.target_db_name
    org_id = args.org_id

    query_builder = QueryBuilder(source_db_name, org_id, source_mongo_uri)
    query_builder.set_projects()
    query_builder.set_versions()
    deletebuilder = DeleteBuilder(query_builder)
    deletebuilder.build_script(target_db_name)

    exportbuilder = ExportBuilder(query_builder)
    exportbuilder.build_script(source_db_name)

    importbuilder = ImportBuilder()
    importbuilder.build_script(target_db_name)

if __name__ == "__main__":
    main(sys.argv)
