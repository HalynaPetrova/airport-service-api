from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from airport.models import Flight, Route, Airplane, AirplaneType, Airport
from airport.serializers import FlightDetailSerializer

FLIGHT_URL = reverse("airport:flight-list")


def detail_url(flight_id: int):
    return reverse("airport:flight-detail", args=[flight_id])


def sample_flight(**params):
    airport = Airport.objects.create(
        name="Test", closest_big_city="Test", country="Test"
    )
    route = Route.objects.create(
        source=airport,
        destination=airport,
        distance=1000,
    )

    airplane_type = AirplaneType.objects.create(name="Test")
    airplane = Airplane.objects.create(
        name="Test",
        rows=10,
        seats_in_row=10,
        airplane_type=airplane_type,
    )

    defaults = {
        "route": route,
        "airplane": airplane,
        "departure_time": "2023-09-05T18:00:00",
        "arrival_time": "2023-09-05T19:00:00",
    }
    defaults.update(params)

    return Flight.objects.create(**defaults)


class UnauthenticatedFlightApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(FLIGHT_URL)
        self.assertEquals(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedFlightTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "test12345",
        )
        self.client.force_authenticate(self.user)

    def test_list_flight(self):
        sample_flight()

        res = self.client.get(FLIGHT_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_retrieve_flight_detail(self):
        flight = sample_flight()

        url = detail_url(flight.id)
        res = self.client.get(url)

        serializer = FlightDetailSerializer(flight)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_flight_forbidden(self):
        airport = Airport.objects.create(
            name="Test", closest_big_city="Test", country="Test"
        )
        route = Route.objects.create(
            source=airport,
            destination=airport,
            distance=1000,
        )

        airplane_type = AirplaneType.objects.create(name="Test")
        airplane = Airplane.objects.create(
            name="Test",
            rows=10,
            seats_in_row=10,
            airplane_type=airplane_type,
        )

        defaults = {
            "route": route,
            "airplane": airplane,
            "departure_time": "2023-09-05 18:00",
            "arrival_time": "2023-09-05 19:00",
        }

        res = self.client.post(FLIGHT_URL, defaults)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminFlightTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com", "test12345", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_flight(self):
        airport = Airport.objects.create(
            name="1", closest_big_city="Test", country="Test"
        )
        route = Route.objects.create(
            source=airport,
            destination=airport,
            distance=1000,
        )

        airplane_type = AirplaneType.objects.create(name="Test")
        airplane = Airplane.objects.create(
            name="2",
            rows=10,
            seats_in_row=10,
            airplane_type=airplane_type,
        )

        payload = {
            "id": "1",
            "route": route.id,
            "airplane": airplane.id,
            "departure_time": "2023-09-05T18:00:00+03:00",
            "arrival_time": "2023-09-05T19:00:00+03:00",
        }

        res = self.client.post(FLIGHT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_update_flight(self):
        flight = sample_flight()
        payload = {
            "departure_time": "2023-09-05 20:00",
        }
        url = detail_url(flight.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_flight(self):
        flight = sample_flight()
        url = detail_url(flight.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
