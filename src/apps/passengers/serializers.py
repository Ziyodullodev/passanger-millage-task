from datetime import date
from decimal import Decimal
from rest_framework import serializers
from .models import TierChoices
from django.db import models

class MileageQuerySerializer(serializers.Serializer):
    class SortChoices(models.TextChoices):
        DISTANCE_DESC = "distance_desc", "Masofa o'sich bo'yicha"
        DISTANCE_ASC = "distance_asc", "Masofa kamayish bo'yicha"
        SPENT_DESC = "spent_desc", "tolov bo'yicha" 
        FLIGHTS_DESC = "flights_desc", "parvoz bo'yicha"
    from_date = serializers.DateField(default=date(2000, 1, 1))
    to_date = serializers.DateField(default=date(2099, 12, 31))
    tier = serializers.ChoiceField(
        choices=TierChoices.choices,
        required=False,
        allow_null=True,
        default=None,
    )
    min_flights = serializers.IntegerField(default=0, min_value=0)
    min_spent = serializers.DecimalField(
        default=Decimal("0"), min_value=Decimal("0"), max_digits=14, decimal_places=2,
    )
    sort = serializers.ChoiceField(choices=SortChoices.choices, default=SortChoices.DISTANCE_DESC)
    page = serializers.IntegerField(default=1, min_value=1)
    page_size = serializers.IntegerField(
        default=20, min_value=1, max_value=100,
    )
    
    def validate(self, attrs):
        if attrs["from_date"] > attrs["to_date"]:
            raise serializers.ValidationError(
                {"from_date": "from_date to_date dan katta bo'lolmaydi!"}
            )
        return attrs


class PassengerMileageSerializer(serializers.Serializer):
    passenger_id = serializers.CharField()
    passenger_name = serializers.CharField()
    valid_flights = serializers.IntegerField()
    total_distance_km = serializers.DecimalField(
        max_digits=12, decimal_places=2, coerce_to_string=False,
    )
    total_spent = serializers.DecimalField(
        max_digits=14, decimal_places=2, coerce_to_string=False,
    )
    avg_segment_price = serializers.DecimalField(
        max_digits=12, decimal_places=2, coerce_to_string=False,
    )
    max_segment_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, coerce_to_string=False,
    )
    min_segment_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, coerce_to_string=False,
    )
    tier = serializers.CharField()
