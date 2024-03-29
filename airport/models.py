import os
import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from django.utils.text import slugify


class AirplaneType(models.Model):
    name = models.CharField(max_length=255)


class Airplane(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    airplane_type = models.ForeignKey(
        AirplaneType, on_delete=models.CASCADE, related_name="airplanes"
    )

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self):
        return f"{self.name} - {self.airplane_type}"


class Airport(models.Model):
    name = models.CharField(max_length=255, unique=True)
    closest_big_city = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Crew(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    class Meta:
        ordering = ["last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


def movie_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.title)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads", "crew", filename)


class Route(models.Model):
    source = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="sources"
    )
    destination = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="destinations"
    )
    distance = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.source} - {self.destination}"


class Flight(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="flights")
    airplane = models.ForeignKey(
        Airplane, on_delete=models.CASCADE, related_name="flights"
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crew = models.ManyToManyField(Crew, related_name="flight_crew")

    class Meta:
        def __str__(self) -> str:
            return f"{self.route} (departure: {self.departure_time} - arrival: {self.arrival_time})"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.created_at)

    class Meta:
        ordering = ["-created_at"]


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="tickets")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="tickets")

    class Meta:
        unique_together = ("flight", "row", "seat")
        ordering = ["row", "seat"]

    def __str__(self):
        return f"{str(self.flight)} (row: {self.row}, seat: {self.seat})"

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        self.full_clean()
        super(Ticket, self).save(force_insert, force_update, using, update_fields)

    @staticmethod
    def validate_seat(
        flight, ticket_attr_value, ticket_attr_name, route_attr_name, error_to_raise
    ):
        count_attrs = getattr(flight.airplane, route_attr_name)
        if not (1 <= ticket_attr_value <= count_attrs):
            raise error_to_raise(
                {
                    ticket_attr_name: f"{ticket_attr_name} "
                    f"number must be in available range: "
                    f"(1, {route_attr_name}): "
                    f"(1, {count_attrs})"
                }
            )

    def clean(self):
        Ticket.validate_seat(self.flight, self.row, "row", "rows", ValidationError)
        Ticket.validate_seat(
            self.flight, self.seat, "seat", "seats_in_row", ValidationError
        )
