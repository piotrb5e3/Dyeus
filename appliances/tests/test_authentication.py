from django.test import TestCase

from appliances.authentication import create_authentication_value


class TestAuthentication(TestCase):
    def test_token_authentication(self):
        av = create_authentication_value('token')
        self.assertEqual(len(av), 22)

        self.assertRegex(av, b'^[a-zA-Z0-9+/]{22}$')

    def test_gcm_aes_authentication(self):
        av = create_authentication_value('gcm_aes')
        self.assertEqual(len(av), 32)

        self.assertRegex(av, b'^[a-fA-F0-9]{32}$')
