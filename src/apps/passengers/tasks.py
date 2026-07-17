from celery import shared_task
from django.core.cache import cache
from django.db import connection

@shared_task
def refresh_mileage_views():
    with connection.cursor() as cursor:
        cursor.execute('REFRESH MATERIALIZED VIEW CONCURRENTLY passenger_flight_mileage;')
        cursor.execute('REFRESH MATERIALIZED VIEW CONCURRENTLY passenger_mileage_summary;')

    try:
        cache.delete("passengers:milaege:date_range")
    except Exception:
        pass
