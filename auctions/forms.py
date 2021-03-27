from django import forms

class NewListing(forms.Form):
  title = forms.CharField(label="Title", max_length=32)
  description = forms.CharField(label="Description", max_length=640)
  start_bid = forms.DecimalField(label="Starting bid", max_digits=7, decimal_places=2)
  # image_url = forms.URLField(label="Image URL", max_length=200)
