from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from airport.models import Airport
from airport.serializers import AirportSerializer

AIRPORT_URL = reverse("airport:airport-list")


def detail_url(airport_id: int):
    return reverse("airport:airport-detail", args=[airport_id])


def sample_airport(**params):
    defaults = {
        "name": "Test",
        "closest_big_city": "Test",
        "country": "Test",
    }
    defaults.update(params)

    return Airport.objects.create(**defaults)


class UnauthenticatedAirportApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(AIRPORT_URL)
        self.assertEquals(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAirportApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "test12345",
        )
        self.client.force_authenticate(self.user)

    def test_list_airplanes(self):
        sample_airport()

        res = self.client.get(AIRPORT_URL)

        airports = Airport.objects.all()
        serializer = AirportSerializer(airports, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_airport_forbidden(self):
        defaults = {
            "name": "Test",
            "closest_big_city": "Test",
            "country": "Test",
        }

        res = self.client.post(AIRPORT_URL, defaults)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminAirportTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com", "test12345", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_airport(self):
        payload = {
            "name": "Test",
            "closest_big_city": "Test",
            "country": "Test",
        }

        res = self.client.post(AIRPORT_URL, payload)
        airport = Airport.objects.get(id=res.data["id"])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        for key in payload:
            self.assertEqual(payload[key], getattr(airport, key))

    def test_update_airport(self):
        airport = sample_airport()
        payload = {
            "name": "Test",
        }
        url = detail_url(airport.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_airport(self):
        airport = sample_airport()
        url = detail_url(airport.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
