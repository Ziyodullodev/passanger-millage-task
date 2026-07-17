import hashlib
import math

from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import MileageQuerySerializer, PassengerMileageSerializer
from .services import get_passenger_mileage, get_cache_data, set_cache_data

class PassengerMileageView(APIView):

    def get(self, request):
        query = MileageQuerySerializer(data=request.query_params)
        query.is_valid(raise_exception=True)
        filters = query.validated_data
        raw = ""
        for key in sorted(filters):
            raw += f"{key}={filters[key]}"
        filtering_key = raw.replace("=", "").replace("_", "").replace("-", "")
        cache_key = "passangers:milage:" + filtering_key
        cached = get_cache_data(cache_key)
        if cached is not None:
            return Response(cached)
        data = get_passenger_mileage(filters)
        payload = {
            "filters_applied": {
                "from_date": filters["from_date"].isoformat(),
                "to_date": filters["to_date"].isoformat(),
                "tier": filters["tier"],
                "min_flights": filters["min_flights"],
                "min_spent": filters["min_spent"],
                "sort": filters["sort"],
            },
            "pagination": {
                "page": filters["page"],
                "page_size": filters["page_size"],
                "total_count": data["total_count"],
                "total_pages": math.ceil(data["total_count"] / filters["page_size"]),
            },
            "summary": data["summary"],
            "results": PassengerMileageSerializer(data["results"], many=True).data,
        }

        set_cache_data(cache_key, payload, 300)
        return Response(payload)
