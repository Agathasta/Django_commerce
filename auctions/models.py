from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=640)
    start_bid = models.DecimalField(max_digits=7, decimal_places=2)
    image_url = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.title}: posted by {self.user}, start bid was {self.start_bid}"

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    bid = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f"Bid of {self.bid} on {self.listing} by {self.user}"

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()