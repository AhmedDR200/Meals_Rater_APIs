from rest_framework import viewsets, status
from .models import Rating, Meal
from .serializers import RatingSerializer, MealSerializer, UserSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAdminUser]



class MealView(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def rate_meal(self, request, pk=None):
        if 'stars' in request.data:
            meal = Meal.objects.get(id=pk)
            stars = request.data['stars']
            user = request.user
            print(user) # for test

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
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        return Response({"message":"Invalid way to create or update"}, status=status.HTTP_400_BAD_REQUEST)
    
    def create(self, request, *args, **kwargs):
        return Response({"message":"Invalid way to create or update"}, status=status.HTTP_400_BAD_REQUEST)