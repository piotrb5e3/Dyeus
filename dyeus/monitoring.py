from pyramid.response import Response
from version import VERSION


def setup_monitoring(config):
    config.add_route('version', '/version')
    config.add_view(version, route_name='version')


def version(request):
    return Response('Dyeus v{}'.format(VERSION))
