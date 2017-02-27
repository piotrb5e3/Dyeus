from pyramid.response import Response


def setup_monitoring(config, settings):
    config.add_route('version', '/version')
    config.add_view(version_factory(settings['version']), route_name='version')


def version_factory(version):
    return lambda request: Response('Dyeus v{}'.format(version))
