from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Meal(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField(max_length=360)

    def no_of_ratings(self):
        ratings = Rating.objects.filter(meal=self)
        return len(list(ratings))
    
    def avg_rating(self):
        ratings = Rating.objects.filter(meal=self).values('stars')
        if not ratings:  # If there are no ratings yet
            return None
        total = sum([r['stars'] for r in list(ratings)])
        count = len(list(ratings))
        return round(total / count, 1)


    def __str__(self):
        return self.title


class Rating(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])

    def __str__(self):
        return str(self.meal)

    class Meta:
        unique_together = (('user', 'meal'),)
        index_together = (('user', 'meal'),)