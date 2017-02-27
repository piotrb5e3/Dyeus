import unittest
from pyramid import testing


class MonitoringViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_hello_world(self):
        from .monitoring import version_factory
        expected_body = 'Dyeus v{}'.format("TEST")

        request = testing.DummyRequest()
        response = version_factory("TEST")(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, expected_body)
