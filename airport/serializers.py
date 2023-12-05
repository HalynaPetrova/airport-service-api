from django.db import transaction
from rest_framework import serializers

from airport.models import (
    Airport,
    AirplaneType,
    Airplane,
    Crew,
    Facility,
    Flight,
    Order,
    Route,
    Ticket,
)


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = (
            "id",
            "name",
            "closest_big_city",
            "country",
            "image",
        )


class AirportImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = (
            "id",
            "image",
        )


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = (
            "id",
            "name",
            "image",
        )


class AirplaneTypeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = (
            "id",
            "image",
        )


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = (
            "id",
            "name",
            "airplane_type",
            "rows",
            "seats_in_row",
            "num_seats",
            "facilities",
            "crew",
        )


class AirplaneListSerializer(AirplaneSerializer):
    airplane_type = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="name",
    )
    facilities = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name",
    )
    crew = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="position",
    )


class CrewSerializer(serializers.ModelSerializer):
    airplanes = AirplaneListSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Crew
        fields = (
            "id",
            "position",
            "first_name",
            "last_name",
            "airplanes",
        )


class CrewListSerializer(serializers.ModelSerializer):
    airplanes = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name",
    )

    class Meta:
        model = Crew
        fields = (
            "id",
            "position",
            "first_name",
            "last_name",
            "airplanes",
        )


class CrewDetailSerializer(serializers.ModelSerializer):
    airplanes = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name",
    )

    class Meta:
        model = Crew
        fields = (
            "id",
            "position",
            "first_name",
            "last_name",
            "airplanes",
        )


class CrewAirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = (
            "id",
            "position",
            "first_name",
            "last_name",
        )


class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = (
            "id",
            "name",
        )


class AirplaneDetailSerializer(AirplaneSerializer):
    airplane_type = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="name",
    )
    facilities = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name",
    )
    crew = CrewAirplaneSerializer(
        many=True,
        read_only=True,
    )


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
        )


class FlightListSerializer(FlightSerializer):
    destination = serializers.CharField(
        source="route.destination",
        read_only=True,
    )
    airplane_name = serializers.CharField(
        source="airplane.name",
        read_only=True,
    )
    airplane_num_seats = serializers.IntegerField(
        source="airplane.capacity",
        read_only=True,
    )
    tickets_available = serializers.IntegerField(read_only=True)

    class Meta:
        model = Flight
        fields = (
            "id",
            "destination",
            "departure_time",
            "arrival_time",
            "airplane_name",
            "airplane_num_seats",
            "tickets_available",
        )


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = (
            "id",
            "source",
            "destination",
            "distance",
        )


class RouteListSerializer(RouteSerializer):
    source = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="name",
    )
    destination = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="name",
    )


class RouteDetailSerializer(RouteSerializer):
    source = AirportSerializer(
        many=False,
        read_only=True,
    )
    destination = AirportSerializer(
        many=False,
        read_only=True,
    )


class TicketSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs)
        Ticket.validate_ticket(
            attrs["row"],
            attrs["seat"],
            attrs["flight"].airplane,
            serializers.ValidationError,
        )
        return data

    class Meta:
        model = Ticket
        fields = (
            "id",
            "row",
            "seat",
            "flight",
        )


class TicketListSerializer(TicketSerializer):
    flight = FlightListSerializer(
        many=False,
        read_only=True,
    )


class TicketTakenSeatsSerializer(TicketSerializer):
    class Meta:
        model = Ticket
        fields = (
            "row",
            "seat",
        )


class FlightDetailSerializer(FlightSerializer):
    airplane = AirplaneListSerializer(
        many=False,
        read_only=True,
    )
    route = RouteDetailSerializer(
        many=False,
        read_only=True,
    )
    taken_seats = TicketTakenSeatsSerializer(
        source="tickets",
        many=True,
        read_only=True,
    )

    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "departure_time",
            "arrival_time",
            "airplane",
            "taken_seats",
        )


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(
        many=True,
        read_only=False,
        allow_empty=False,
    )

    class Meta:
        model = Order
        fields = (
            "id",
            "created_at",
            "paid",
            "tickets",
        )

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(order=order, **ticket_data)
            return order


class OrderListSerializer(OrderSerializer):
    tickets = TicketListSerializer(
        many=True,
        read_only=True,
    )


class OrderDetailSerializer(OrderSerializer):
    tickets = TicketListSerializer(
        many=True,
        read_only=True,
    )
