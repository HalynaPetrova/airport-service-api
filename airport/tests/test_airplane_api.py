from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from airport.models import AirplaneType, Airplane, Facility
from airport.serializers import AirplaneListSerializer, AirplaneDetailSerializer


AIRPLANE_URL = reverse("airport:airplane-list")


def detail_url(airplane_id: int):
    return reverse("airport:airplane-detail", args=[airplane_id])


def sample_airplane(**params):
    airplane_type = AirplaneType.objects.create(name="Test")

    defaults = {
        "name": "Test",
        "rows": 10,
        "seats_in_row": 10,
        "airplane_type": airplane_type,
    }
    defaults.update(params)

    return Airplane.objects.create(**defaults)


class UnauthenticatedAirplaneApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(AIRPLANE_URL)
        self.assertEquals(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAirplaneApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "test12345",
        )
        self.client.force_authenticate(self.user)

    def test_list_airplanes(self):
        sample_airplane()
        airplane_with_facilities=sample_airplane()

        facility1 = Facility.objects.create(name="wifi")
        facility2 = Facility.objects.create(name="WC")

        airplane_with_facilities.facilities.add(facility1, facility2)

        res = self.client.get(AIRPLANE_URL)

        airplanes = Airplane.objects.all()
        serializer = AirplaneListSerializer(airplanes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_filter_buses_by_facilities(self):
        airplane1 = sample_airplane()
        airplane2 = sample_airplane()

        facilities1 = Facility.objects.create(name="wifi")
        facilities2 = Facility.objects.create(name="WC")

        airplane1.facilities.add(facilities1)
        airplane2.facilities.add(facilities2)

        airplane3 = sample_airplane(name="Airplane without facilities")

        res = self.client.get(AIRPLANE_URL, {"facilities": f"{facilities1.id}, {facilities2.id}"})

        serializer1 = AirplaneListSerializer(airplane1)
        serializer2 = AirplaneListSerializer(airplane2)
        serializer3 = AirplaneListSerializer(airplane3)

        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)

    def test_retrieve_airplane_detail(self):
        airplane = sample_airplane()
        airplane.facilities.add(Facility.objects.create(name="wifi"))

        url = detail_url(airplane.id)
        res = self.client.get(url)

        serializer = AirplaneDetailSerializer(airplane)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_airplane_forbidden(self):
        airplane_type = AirplaneType.objects.create(name="Test")

        defaults = {
            "name": "Test",
            "rows": 10,
            "seats_in_row": 10,
            "airplane_type": airplane_type,
        }

        res = self.client.post(AIRPLANE_URL, defaults)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminAirplaneTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "test12345",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_airplane(self):
        airplane_type = AirplaneType.objects.create(name="1")

        payload = {
            "name": "Test",
            "rows": 10,
            "seats_in_row": 10,
            "airplane_type": airplane_type,
        }

        res = self.client.post(AIRPLANE_URL, payload)
        airplane = Airplane.objects.get(id=res.data["id"])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        for key in payload:
            self.assertEqual(payload[key], getattr(airplane, key))

    def test_create_airplane_with_facilities(self):
        facility1 = Facility.objects.create(name="wifi")
        facility2 = Facility.objects.create(name="WC")
        airplane_type = AirplaneType.objects.create(name="1")

        payload = {
            "name": "Test",
            "rows": 10,
            "seats_in_row": 10,
            "airplane_type": airplane_type,
            "facilities": [facility1.id, facility2.id]
        }

        res = self.client.post(AIRPLANE_URL, payload)
        airplane = Airplane.objects.get(id=res.data["id"])
        facilities = airplane.facilities.all()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        self.assertEqual(facilities.count(), 2)
        self.assertIn(facility1, facilities)
        self.assertIn(facility2, facilities)

    def test_update_airplane(self):
        airplane = sample_airplane()
        payload = {
            "name": "Test",
        }
        url = detail_url(airplane.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_airplane(self):
        airplane = sample_airplane()
        url = detail_url(airplane.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
