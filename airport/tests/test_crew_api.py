from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from airport.models import Crew, Airplane, AirplaneType
from airport.serializers import CrewListSerializer, CrewDetailSerializer

CREW_URL = reverse("airport:crew-list")


def detail_url(crew_id: int):
    return reverse("airport:crew-detail", args=[crew_id])


def sample_crew(**params):
    defaults = {
        "first_name": "Test",
        "last_name": "Test",
        "position": "Test",
    }
    defaults.update(params)

    return Crew.objects.create(**defaults)


class UnauthenticatedCrewApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(CREW_URL)
        self.assertEquals(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedCrewApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "test12345",
        )
        self.client.force_authenticate(self.user)

    def test_list_crew(self):
        sample_crew()
        crew_with_airplanes = sample_crew()

        airplane_type = AirplaneType.objects.create(name="Test")
        airplane1 = Airplane.objects.create(
            name="Test", rows=10, seats_in_row=10, airplane_type=airplane_type
        )
        airplane2 = Airplane.objects.create(
            name="Test", rows=10, seats_in_row=10, airplane_type=airplane_type
        )

        crew_with_airplanes.airplanes.add(airplane1, airplane2)

        res = self.client.get(CREW_URL)

        crew = Crew.objects.all()
        serializer = CrewListSerializer(crew, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_crew_detail(self):
        crew = sample_crew()
        airplane_type = AirplaneType.objects.create(name="Test")
        crew.airplanes.add(
            Airplane.objects.create(
                name="Test", rows=10, seats_in_row=10, airplane_type=airplane_type
            )
        )

        url = detail_url(crew.id)
        res = self.client.get(url)

        serializer = CrewDetailSerializer(crew)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_crew_forbidden(self):
        defaults = {
            "first_name": "Test",
            "last_name": "Test",
            "position": "Test",
        }

        res = self.client.post(CREW_URL, defaults)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminCrewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com", "test12345", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_airport(self):
        payload = {
            "first_name": "Test",
            "last_name": "Test",
            "position": "pilot",
        }

        res = self.client.post(CREW_URL, payload)
        crew = Crew.objects.get(id=res.data["id"])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        for key in payload:
            self.assertEqual(payload[key], getattr(crew, key))

    def test_update_crew(self):
        crew = sample_crew()
        payload = {
            "first_name": "Test",
        }
        url = detail_url(crew.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_airplane(self):
        crew = sample_crew()
        url = detail_url(crew.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
