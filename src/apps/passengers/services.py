from django.core.cache import cache
from django.db.models import Avg, Case, CharField, Count, Max, Min, Sum, Value, When
from django.db.models.functions import Round

from .models import PassengerFlightMileage, PassengerMileageSummary


def get_cache_data(key):
    try:
        return cache.get(key)
    except Exception:
        return None


def set_cache_data(key, value, live_time):
    try:
        cache.set(key, value, live_time)
    except Exception:
        pass


def getting_data_and_set_cache(from_date, to_date):
    cached = get_cache_data("passengers:milaege:date_range")
    if cached is None:
        bounds = PassengerFlightMileage.objects.aggregate(
            min_date=Min("flight_date"), max_date=Max("flight_date"),
        )
        data1, data2 = bounds["min_date"], bounds["max_date"]
        result = (bounds["min_date"], bounds["max_date"])
        print(result)
        print("cachega saqlandi.")
        set_cache_data("passengers:milaege:date_range", result, 3600)
    else:
        data1, data2 = cached
    if data1:
        return True
    return from_date <= data1 and to_date >= data2


def getting_queryset_with_filter(filters):
    qs = (
        PassengerFlightMileage.objects.filter(
            flight_date__gte=filters["from_date"],
            flight_date__lte=filters["to_date"]).values("passenger_id")
            .annotate(
                passenger_name=Max("passenger_name"),
                valid_flights=Count("flight_id"),
                total_distance_km=Sum("distance_km"),
                total_spent=Sum("price"),
                avg_segment_price=Round(Avg("price"), 2),
                max_segment_price=Max("price"),
                min_segment_price=Min("price"),
            )
        )
    if filters["tier"]:
        filters_data_for_tier = {
            "Bronze": (None, 5000),
            "Silver": (5000, 15000),
            "Gold": (15000, 50000),
            "Platinum": (50000, None),
        }
        low, high = filters_data_for_tier[filters["tier"]]
        if low is not None and high is not None:
            qs = qs.filter(total_distance_km__gte=low, total_distance_km__lt=high)
        elif low is not None:
            qs = qs.filter(total_distance_km__gte=low)
        elif high is not None:
            qs = qs.filter(total_distance_km__lt=high)
    if filters["min_flights"] > 0:
        qs = qs.filter(valid_flights__gte=filters["min_flights"])
    if filters["min_spent"] > 0:
        qs = qs.filter(total_spent__gte=filters["min_spent"])
    result = qs.annotate(tier=Case(
        When(total_distance_km__gte=50000, then=Value("Platinum")),
        When(total_distance_km__gte=15000, then=Value("Gold")),
        When(total_distance_km__gte=5000, then=Value("Silver")),
        default=Value("Bronze"),
        output_field=CharField(),
    ))
    return result


def get_passenger_mileage_summary_data(filters):
    qs = PassengerMileageSummary.objects.all()
    if filters["tier"]:
        qs = qs.filter(tier=filters["tier"])
    if filters['min_flights'] > 0:
        qs = qs.filter(valid_flights__gte=filters["min_flights"])
    if filters["min_spent"] > 0:
        qs = qs.filter(total_spent__gte=filters["min_spent"])
    return qs

def get_passenger_mileage(filters):
    if getting_data_and_set_cache(filters["from_date"], filters["to_date"]):
        qs = get_passenger_mileage_summary_data(filters)
    else:
        qs = getting_queryset_with_filter(filters)

    agg = qs.aggregate(
        passengers=Count("passenger_id"),
        revenue=Sum("total_spent"),
        distance=Sum("total_distance_km"),
    )
    total_count = agg["passengers"] or 0
    index_range = (filters["page"] - 1) * filters["page_size"]
    sort_datas = {
        "distance_desc": ("-total_distance_km", "passenger_id"),
        "distance_asc": ("total_distance_km", "passenger_id"),
        "spent_desc": ("-total_spent", "passenger_id"),
        "flights_desc": ("-valid_flights", "passenger_id"),
    }
    results = list(qs.order_by(*sort_datas[filters["sort"]])[index_range:index_range + filters["page_size"]])
    return {
        "total_count": total_count,
        "summary": {
            "total_passengers": total_count,
            "total_revenue": agg["revenue"] or 0,
            "total_distance_km": agg["distance"] or 0,
        },
        "results": results,
    }
