import transaction
import os
import sys

from sqlalchemy import engine_from_config

from pyramid.paster import get_appsettings, setup_logging

from dyeus.db import DBSession, Base, load_models


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)

    load_models()
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    with transaction.manager:
        for tbl in reversed(Base.metadata.sorted_tables):
            tbl.drop(engine, checkfirst=True)
