import unittest
from pyramid import testing

from version import VERSION


class MonitoringViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_hello_world(self):
        from .monitoring import version
        expected_body = 'Dyeus v{}'.format(VERSION)

        request = testing.DummyRequest()
        response = version(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, expected_body)
