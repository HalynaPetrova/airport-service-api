from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from airport.models import Airport, Route
from airport.serializers import RouteListSerializer, RouteDetailSerializer

ROUTE_URL = reverse("airport:route-list")


def detail_url(route_id: int):
    return reverse("airport:route-detail", args=[route_id])


def sample_route(**params):
    airport1 = Airport.objects.create(
        name="Test",
        closest_big_city="Test",
        country="Test",
    )

    airport2 = Airport.objects.create(
        name="Test",
        closest_big_city="Test",
        country="Test",
    )

    defaults = {
        "source": airport1,
        "destination": airport2,
        "distance": 1000,
    }
    defaults.update(params)

    return Route.objects.create(**defaults)


class UnauthenticatedRouteApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(ROUTE_URL)
        self.assertEquals(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedRouteApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "test12345",
        )
        self.client.force_authenticate(self.user)

    def test_list_routes(self):
        sample_route()

        res = self.client.get(ROUTE_URL)

        routes = Route.objects.all()
        serializer = RouteListSerializer(routes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_route_detail(self):
        route = sample_route()

        url = detail_url(route.id)
        res = self.client.get(url)

        serializer = RouteDetailSerializer(route)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_route_forbidden(self):
        airport1 = Airport.objects.create(
            name="Test",
            closest_big_city="Test",
            country="Test",
        )

        airport2 = Airport.objects.create(
            name="Test",
            closest_big_city="Test",
            country="Test",
        )

        defaults = {
            "source": airport1,
            "destination": airport2,
            "distance": 1000,
        }

        res = self.client.post(ROUTE_URL, defaults)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminRouteTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "test12345",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_route(self):
        airport1 = Airport.objects.create(
            name="1",
            closest_big_city="Test",
            country="Test",
        )
        airport2 = Airport.objects.create(
            name="2",
            closest_big_city="Test",
            country="Test",
        )

        payload = {
            "source": airport1,
            "destination": airport2,
            "distance": 1000,
        }

        res = self.client.post(ROUTE_URL, payload)
        rout = Route.objects.get(id=res.data["id"])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        for key in payload:
            self.assertEqual(payload[key], getattr(rout, key))

    def test_update_route(self):
        route = sample_route()
        payload = {
            "distance": "1000",
        }
        url = detail_url(route.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
