from django import forms

from .models import Category

class NewListing(forms.Form):
  title = forms.CharField(label="Title", max_length=32)
  description = forms.CharField(label="Description", max_length=640, required=False)
  category = forms.ModelChoiceField(label="Category", queryset=Category.objects.all(), to_field_name="category")
  start_bid = forms.DecimalField(label="Starting bid", max_digits=7, decimal_places=2)
  image_url = forms.URLField(label="Image URL", max_length=200, required=False)

class NewBid(forms.Form):
  bid = forms.DecimalField(label="Your bid", max_digits=7, decimal_places=2, required=False)

class NewComment(forms.Form):
  comment = forms.CharField(max_length=550, required=False)