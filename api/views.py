from rest_framework import viewsets, status
from .models import Rating, Meal
from .serializers import RatingSerializer, MealSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User


class MealView(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    
    @action(detail=True, methods=['post'])
    def rate_meal(self, request, pk=None):
        if 'stars' in request.data:
            meal = Meal.objects.get(id=pk)
            stars = request.data['stars']
            username = request.data['username']
            user = User.objects.get(username=username)

            try:
                rate = Rating.objects.get(user=user, meal=meal)
                rate.stars = stars
                rate.save()
                serializer = RatingSerializer(rate, many=False)
                return Response({"message": "Rating updated", "result": serializer.data}, status=status.HTTP_200_OK)

            except Rating.DoesNotExist:
                rate = Rating.objects.create(user=user, meal=meal, stars=stars)
                serializer = RatingSerializer(rate, many=False)
                return Response({"message": "Meal Rate Created", "result": serializer.data}, status=status.HTTP_201_CREATED)

        else:
            return Response({"error": "You must specify the number of stars"}, status=status.HTTP_400_BAD_REQUEST)
   
   
    
class RatingView(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
