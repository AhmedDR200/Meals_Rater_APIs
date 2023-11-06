from rest_framework import viewsets
from .models import Rating, Meal
from .serializers import RatingSerializer, MealSerializer


class MealView(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    

class RatingView(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
