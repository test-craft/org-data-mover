import os
import logging


def configure(filename):
    logfilename = os.path.splitext(filename)[0] + '.log'
    logfiledir = os.path.dirname(logfilename)
    if not os.path.exists(logfiledir):
        os.makedirs(logfiledir)
    logging.basicConfig(filename=logfilename, level=logging.DEBUG, format='%(asctime)s %(levelname)s %(funcName)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
