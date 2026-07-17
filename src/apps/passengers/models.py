# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AirplanesData(models.Model):
    airplane_code = models.CharField(primary_key=True, max_length=3, db_comment='Airplane code, IATA')
    model = models.JSONField(db_comment='Airplane model')
    range = models.IntegerField(db_comment='Maximum flight range, km')
    speed = models.IntegerField(db_comment='Cruise speed, km/h')

    class Meta:
        managed = False
        db_table = 'airplanes_data'
        db_table_comment = 'Airplanes (internal multilingual data)'


class AirportsData(models.Model):
    airport_code = models.CharField(primary_key=True, max_length=3, db_comment='Airport code, IATA')
    airport_name = models.JSONField(db_comment='Airport name')
    city = models.JSONField(db_comment='City')
    country = models.JSONField(db_comment='Country')
    coordinates = models.TextField(db_comment='Airport coordinates (longitude and latitude)')  # This field type is a guess.
    timezone = models.TextField(db_comment='Airport time zone')

    class Meta:
        managed = False
        db_table = 'airports_data'
        db_table_comment = 'Airports (internal multilingual data)'


class BoardingPasses(models.Model):
    ticket_no = models.OneToOneField('Segments', models.DO_NOTHING, db_column='ticket_no', primary_key=True, db_comment='Ticket number')  # The composite primary key (ticket_no, flight_id) found, that is not supported. The first column is selected.
    flight_id = models.IntegerField(db_comment='Flight ID')
    seat_no = models.TextField(db_comment='Seat number')
    boarding_no = models.IntegerField(blank=True, null=True, db_comment='Boarding pass number')
    boarding_time = models.DateTimeField(blank=True, null=True, db_comment='Boarding time')

    class Meta:
        managed = False
        db_table = 'boarding_passes'
        unique_together = (('flight_id', 'boarding_no'), ('flight_id', 'seat_no'), ('ticket_no', 'flight_id'),)
        db_table_comment = 'Boarding passes'


class Bookings(models.Model):
    book_ref = models.CharField(primary_key=True, max_length=6, db_comment='Booking number')
    book_date = models.DateTimeField(db_comment='Booking date')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, db_comment='Total booking amount')

    class Meta:
        managed = False
        db_table = 'bookings'
        db_table_comment = 'Bookings'


class Flights(models.Model):
    flight_id = models.AutoField(primary_key=True, db_comment='Flight ID')
    route_no = models.TextField(db_comment='Route number')
    status = models.TextField(db_comment='Flight status')
    scheduled_departure = models.DateTimeField(db_comment='Scheduled departure time')
    scheduled_arrival = models.DateTimeField(db_comment='Scheduled arrival time')
    actual_departure = models.DateTimeField(blank=True, null=True, db_comment='Actual departure time')
    actual_arrival = models.DateTimeField(blank=True, null=True, db_comment='Actual arrival time')

    class Meta:
        managed = False
        db_table = 'flights'
        unique_together = (('route_no', 'scheduled_departure'),)
        db_table_comment = 'Flights'


class Routes(models.Model):
    route_no = models.TextField(db_comment='Route number')
    validity = models.TextField(db_comment='Period of validity')  # This field type is a guess.
    departure_airport = models.ForeignKey(AirportsData, models.DO_NOTHING, db_column='departure_airport', db_comment='Airport of departure')
    arrival_airport = models.ForeignKey(AirportsData, models.DO_NOTHING, db_column='arrival_airport', related_name='routes_arrival_airport_set', db_comment='Airport of arrival')
    airplane_code = models.ForeignKey(AirplanesData, models.DO_NOTHING, db_column='airplane_code', db_comment='Airplane code, IATA')
    days_of_week = models.TextField(db_comment='Days of week array')  # This field type is a guess.
    scheduled_time = models.TimeField(db_comment='Scheduled local time of departure')
    duration = models.DurationField(db_comment='Estimated duration')

    class Meta:
        managed = False
        db_table = 'routes'
        db_table_comment = 'Routes'


class Seats(models.Model):
    airplane_code = models.OneToOneField(AirplanesData, models.DO_NOTHING, db_column='airplane_code', primary_key=True, db_comment='Airplane code, IATA')  # The composite primary key (airplane_code, seat_no) found, that is not supported. The first column is selected.
    seat_no = models.TextField(db_comment='Seat number')
    fare_conditions = models.TextField(db_comment='Travel class')

    class Meta:
        managed = False
        db_table = 'seats'
        unique_together = (('airplane_code', 'seat_no'),)
        db_table_comment = 'Seats'


class Segments(models.Model):
    ticket_no = models.OneToOneField('Tickets', models.DO_NOTHING, db_column='ticket_no', primary_key=True, db_comment='Ticket number')  # The composite primary key (ticket_no, flight_id) found, that is not supported. The first column is selected.
    flight = models.ForeignKey(Flights, models.DO_NOTHING, db_comment='Flight ID')
    fare_conditions = models.TextField(db_comment='Travel class')
    price = models.DecimalField(max_digits=10, decimal_places=2, db_comment='Travel price')

    class Meta:
        managed = False
        db_table = 'segments'
        unique_together = (('ticket_no', 'flight'),)
        db_table_comment = 'Flight segment (leg)'


class Tickets(models.Model):
    ticket_no = models.TextField(primary_key=True, db_comment='Ticket number')
    book_ref = models.ForeignKey(Bookings, models.DO_NOTHING, db_column='book_ref', db_comment='Booking number')
    passenger_id = models.TextField(db_comment='Passenger ID')
    passenger_name = models.TextField(db_comment='Passenger name')
    outbound = models.BooleanField(db_comment='Outbound flight?')

    class Meta:
        managed = False
        db_table = 'tickets'
        unique_together = (('book_ref', 'passenger_id', 'outbound'),)
        db_table_comment = 'Tickets'


class PassengerFlightMileage(models.Model):
    ticket_no = models.TextField(primary_key=True)
    flight_id = models.IntegerField()
    passenger_id = models.TextField()
    passenger_name = models.TextField()
    flight_date = models.DateField(db_comment='Reys uchgan sana (actual_departure, UTC)')
    distance_km = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'passenger_flight_mileage'

class TierChoices(models.TextChoices):
    BRONZE = "Bronze", "Bronza daraja"
    SILVER = "Silver", "Silver daraja"
    GOLD = "Gold", "GOld daraja"
    PLATINUM = "Platinum", "Platinum daraja"

class PassengerMileageSummary(models.Model):

    passenger_id = models.TextField(primary_key=True)
    passenger_name = models.TextField()
    valid_flights = models.IntegerField()
    total_distance_km = models.DecimalField(max_digits=12, decimal_places=2)
    total_spent = models.DecimalField(max_digits=14, decimal_places=2)
    avg_segment_price = models.DecimalField(max_digits=12, decimal_places=2)
    max_segment_price = models.DecimalField(max_digits=10, decimal_places=2)
    min_segment_price = models.DecimalField(max_digits=10, decimal_places=2)
    tier = models.CharField(max_length=8)

    class Meta:
        managed = False
        db_table = 'passenger_mileage_summary'
