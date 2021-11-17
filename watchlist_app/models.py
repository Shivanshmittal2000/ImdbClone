from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator
from django.contrib.auth.models import User
# Create your models here.

class StreamPlatform(models.Model):
    name=models.CharField(max_length=100)
    about=models.CharField(max_length=1000)
    website=models.URLField(max_length=100)
    def __str__(self):
        return self.name


class WatchList(models.Model):
    title=models.CharField(max_length=100)
    storyline=models.CharField(max_length=1000)
    platform=models.ForeignKey(StreamPlatform,on_delete=models.CASCADE,related_name='watchlist') # this related name helps for getting all movies of a platform like all movies belongs to Amazon prime video
    avg_rating=models.FloatField(default=0)
    number_rating=models.IntegerField(default=0)
    active=models.BooleanField(default=False)
    created=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

class Review(models.Model):
    review_user=models.ForeignKey(User,on_delete=models.CASCADE)
    rating=models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description=models.CharField(max_length=200, null=True)
    watchlist=models.ForeignKey(WatchList,on_delete=models.CASCADE,related_name='reviews')
    active=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.rating) + " | " +self.watchlist.title + " | " + str(self.review_user)