from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator
# Create your models here.

class Dishes(models.Model):
    name=models.CharField(max_length=120)
    price=models.PositiveIntegerField()
    category=models.CharField(max_length=120)

    def __str__(self):
        return self.name

    #avg of rating and reviews
    def avg_rating(self):
        all_reviews=self.reviews_set.all()
        if all_reviews:
            total=sum([review.rating for review in all_reviews])
            return total/len(all_reviews)
        else:
            return 0

    def review_count(self):
        return self.reviews_set.all().count()



class Reviews(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    dish=models.ForeignKey(Dishes,on_delete=models.CASCADE)
    review=models.CharField(max_length=200)
    rating=models.FloatField(validators=[MinValueValidator(1),MaxValueValidator(5)])
