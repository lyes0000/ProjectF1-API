# ml_predictions/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drivers.models import Driver
from .prediction.predict_race import RacePredictor
from .serializers import RacePredictionSerializer


class RacePredictionAPIView(APIView):
    def post(self, request):
        year = int(request.data.get("year"))
        race_name = request.data.get("race_name")
        round_no = request.data.get("round")

        if not year or not (race_name or round_no):
            return Response(
                {"error": "year and race_name or round are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            predictor = RacePredictor(
                model_path="ml_predictions/ml_models/random_forest_v1_latest.joblib"
            )

            predictions_df = predictor.predict(year, race_name)

            response_data = []
            for idx, row in enumerate(predictions_df.itertuples(), start=1):
                driver = Driver.objects.get(id=row.driver_id)

                response_data.append({
                    "position": idx,
                    "driver_id": driver.id,
                    "driver_full_name": f"{driver.first_name} {driver.last_name}",
                    "team": driver.team,
                    "points": 0,
                    "win_probability": round(row.win_probability, 4),
                })

            serializer = RacePredictionSerializer(response_data, many=True)
            return Response(serializer.data)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
