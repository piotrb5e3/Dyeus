from django.test import TestCase

from appliances.authentication import create_authentication_value


class TestAuthentication(TestCase):
    def test_token_authentication(self):
        av = create_authentication_value('token')
        self.assertLessEqual(len(av), 22)

        self.assertRegex(av, b'^[a-zA-Z0-9+/]{22}$')
