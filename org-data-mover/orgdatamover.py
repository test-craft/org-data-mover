import sys
import os
import logger
import logging
import argparse
from querybuilder import QueryBuilder
from deletebuilder import DeleteBuilder


def main(argv=[]):

    logger.configure(__file__)
    logging.info("starting the orgdatamover")
    parser = argparse.ArgumentParser(prog='orgdatamover')
    parser.add_argument('--source-db-name', help='foo of the %(prog)s program')
    parser.add_argument('--source-mongo-uri', help='foo of the %(prog)s program')
    parser.add_argument('--targetDbName', help='foo of the %(prog)s program')
    parser.add_argument('--targetMongoURI', help='foo of the %(prog)s program')
    parser.add_argument('--orgid', help='foo of the %(prog)s program')


    db_name = argv[1]
    org_id = argv[2]
    mongo_uri = argv[3]
    query_builder = QueryBuilder(db_name, org_id, mongo_uri)
    query_builder.set_projects()
    query_builder.set_versions()
    deletebuilder = DeleteBuilder(query_builder)
    deletebuilder.build_script(db_name)

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
