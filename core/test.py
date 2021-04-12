import json


# from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
# from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import *
from .serializers import *
from .urls import *

class RegistrationTestCase(TestCase):

    def test_registration(self):
        data = {
            "username": "admin", "password": "1234"
        }
        response = self.client.post("/login/", data, HTTP_HOST='docs.djangoproject.dev:8000')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)