from django.contrib import admin
from .models import Bid, Category, Comment, Listing, User

class BidAdmin(admin.ModelAdmin):
  list_display = ('user', 'listing', 'bid', 'winning_bid')

class CategoryAdmin(admin.ModelAdmin):
  list_display = ('id', 'category')

class CommentAdmin(admin.ModelAdmin):
  list_display = ('user', 'listing', 'comment')

class ListingAdmin(admin.ModelAdmin):
  list_display = ('title', 'start_bid', 'current_price', 'category')

# Register your models here.
admin.site.register(Bid, BidAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(User)
