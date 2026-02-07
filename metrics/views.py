from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from datetime import date
from accounts.permissions import IsAdmin
from .services import week_range, month_range, roi_summary

class WeeklySummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        merch_id = request.query_params.get("merchandiser_id")
        anchor = request.query_params.get("anchor")  # YYYY-MM-DD

        if request.user.role != "ADMIN":
            merch_id = request.user.id

        if not merch_id:
            return Response({"detail": "merchandiser_id required (admin only)."}, status=400)

        anchor_date = date.fromisoformat(anchor) if anchor else date.today()
        start, end = week_range(anchor_date)

        return Response({
            "period": "WEEKLY",
            "start": start,
            "end": end,
            "merchandiser_id": int(merch_id),
            "metrics": roi_summary(int(merch_id), start, end),
        })

class MonthlySummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        merch_id = request.query_params.get("merchandiser_id")
        anchor = request.query_params.get("anchor")

        if request.user.role != "ADMIN":
            merch_id = request.user.id

        if not merch_id:
            return Response({"detail": "merchandiser_id required (admin only)."}, status=400)

        anchor_date = date.fromisoformat(anchor) if anchor else date.today()
        start, end = month_range(anchor_date)

        return Response({
            "period": "MONTHLY",
            "start": start,
            "end": end,
            "merchandiser_id": int(merch_id),
            "metrics": roi_summary(int(merch_id), start, end),
        })
