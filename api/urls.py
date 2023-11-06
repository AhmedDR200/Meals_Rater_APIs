from django.urls import path
from rest_framework import routers
from django.conf.urls import include
from .views import MealView, RatingView, UserView

router = routers.DefaultRouter()
router.register('meals', MealView)
router.register('ratings', RatingView)
router.register('users', UserView)

urlpatterns = [
    path('', include(router.urls)),
]