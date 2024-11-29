from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token

from garlight.models import YeelightBulb


class AuthenticationTest(TestCase):
    def setUp(self):
        self.bulb = YeelightBulb.objects.create(
            bulb_id="bulb_id",
            ip="1.1.1.1.",
            name="bulb_name",
        )
        self.url = reverse("bulb-power-detail", args=[self.bulb.name])

    def tearDown(self):
        patch.stopall()

    def test_raise_error_on_missing_token(self):
        expected = (
            b'{"detail":"Authentication credentials were not provided."}'
        )
        response = self.client.get(self.url)
        assert response.status_code == 401
        assert response.content == expected

    def test_raise_error_on_empty_token(self):
        expected = (
            b'{"detail":"Invalid token header. No credentials provided."}'
        )
        headers = {"AUTHORIZATION": "Token"}
        response = self.client.get(self.url, headers=headers)
        assert response.status_code == 401
        assert response.content == expected

    def test_raise_error_on_invalid_characters(self):
        expected = b'{"detail":"Invalid token header. Token string should not contain invalid characters."}'
        headers = {"AUTHORIZATION": b"Token \xff\xff\xff\xff"}
        response = self.client.get(self.url, headers=headers)
        assert response.status_code == 401
        assert response.content == expected

    def test_raise_error_on_invalid_token(self):
        headers = {"AUTHORIZATION": "Token invalid_token"}
        response = self.client.get(self.url, headers=headers)
        assert response.status_code == 401
        assert response.content == b'{"detail":"Invalid token."}'

    def test_raise_error_on_token_with_spaces(self):
        expected = b'{"detail":"Invalid token header. Token string should not contain spaces."}'
        headers = {"AUTHORIZATION": "Token invalid token"}
        response = self.client.get(self.url, headers=headers)
        assert response.status_code == 401
        assert response.content == expected

    def test_pass_on_valid_token(self):
        patch("garlight.bulbs.SmartBulb.on_off", return_value="test").start()
        user = User.objects.create_user(username="test", password="test")
        user.token = Token.objects.create(user=user)
        token = f"Token {user.token.key}"
        headers = {"AUTHORIZATION": token}

        response = self.client.get(self.url, headers=headers)
        assert response.status_code == 200
