from django.contrib import admin
from .models import Bid, Category, Comment, Listing, User

class CategoryAdmin(admin.ModelAdmin):
  list_display = ('id', 'category')

# Register your models here.
admin.site.register(Bid)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment)
admin.site.register(Listing)
admin.site.register(User)
