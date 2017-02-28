from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .db import Base, DBSession, load_models

from .monitoring import setup_monitoring


def main(global_config, **settings):
    load_models()
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    config = Configurator(settings=settings)
    setup_monitoring(config, settings=settings)
    return config.make_wsgi_app()
