from . import views


def setup_api(config, settings):
    config.scan(views)
