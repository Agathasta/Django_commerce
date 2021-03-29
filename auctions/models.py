from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watching = models.ManyToManyField('Listing', blank=True, related_name='watchers')


class Bid(models.Model):
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE, related_name='bids')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    bid = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f"Bid of {self.bid}€ on {self.listing} by {self.user}"


class Category(models.Model):
    category = models.CharField(max_length=32)

    def __str__(self):
        return self.category


class Comment(models.Model):
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()


class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='listings', default=1)
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=640, blank=True)
    image_url = models.URLField(max_length=200, blank=True)
    start_bid = models.DecimalField(max_digits=7, decimal_places=2)
    current_price = models.DecimalField(max_digits=7, decimal_places=2)
    closed = models.BooleanField(default=False)

    # https://stackoverflow.com/questions/4380879/django-model-field-default-based-off-another-field-in-same-model
    def save(self, *args, **kwargs):
        if self.current_price is None:
            self.current_price = self.start_bid
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}: listed by {self.user}, current price is {self.start_bid}"
