from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Airport (models.Model):
    name = models.CharField(max_length=255)
    closest_big_city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to="images/airport/",
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class AirplaneType (models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to="images/airplane_type/",
    )

    def __str__(self):
        return self.name


class Airplane (models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    airplane_type = models.ForeignKey(
        AirplaneType,
        on_delete=models.CASCADE,
        related_name="airplanes",
    )
    crew = models.ManyToManyField(
        "Crew",
        related_name="airplanes",
        blank=True,
    )
    facilities = models.ManyToManyField(
        "Facility",
        related_name="airplanes",
        blank=True,
    )

    @property
    def num_seats(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self):
        return self.name


class Crew (models.Model):
    POSITION = (
        ("captain", "captain"),
        ("pilot", "pilot"),
        ("navigator", "navigator"),
        ("flight_mechanic", "flight_mechanic"),
        ("flight_attendants", "flight_attendants"),
    )

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    position = models.CharField(
        max_length=255,
        choices=POSITION,
        default="flight_attendants",
    )

    class Meta:
        ordering = ["position", "first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Facility (models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Flight (models.Model):
    route = models.ForeignKey(
        "Route",
        on_delete=models.CASCADE,
        related_name="flights",
    )
    airplane = models.ForeignKey(
        Airplane,
        on_delete=models.CASCADE,
        related_name="flights",
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    class Meta:
        ordering = ["-departure_time"]


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
    )
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]


class Route (models.Model):
    source = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="routs",
    )
    destination = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
    )
    distance = models.IntegerField()

    class Meta:
        ordering = ["source"]


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    flight = models.ForeignKey(
        Flight,
        on_delete=models.CASCADE,
        related_name="tickets",
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="tickets",
    )

    class Meta:
        unique_together = ("row", "seat", "flight",)
        ordering = ["row", "seat"]

    @staticmethod
    def validate_ticket(row, seat, airplane, error_to_raise):
        for ticket_attr_value, ticket_attr_name, airplane_attr_name in [
            (row, "row", "rows"),
            (seat, "seat", "seats_in_row"),
        ]:
            count_attrs = getattr(airplane, airplane_attr_name)
            if not (1 <= ticket_attr_value <= count_attrs):
                raise error_to_raise(
                    {
                        ticket_attr_name: f"{ticket_attr_name} "
                        f"number must be in available range: "
                        f"(1, {airplane_attr_name}): "
                        f"(1, {count_attrs})"
                    }
                )

    def clean(self):
        Ticket.validate_ticket(self.row, self.seat, self.flight.airplane, ValidationError)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.full_clean()
        return super(Ticket, self).save(force_insert, force_update, using, update_fields)
