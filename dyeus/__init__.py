from pyramid.config import Configurator
from .monitoring import setup_monitoring

def main(global_config, **settings):
    config = Configurator(settings=settings)
    setup_monitoring(config, settings=settings)
    return config.make_wsgi_app()
