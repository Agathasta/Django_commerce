from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('add', views.add, name='add'),
    path('item/<int:item_id>', views.item, name='item'),
    path('categories', views.categories, name='categories'),
    path('categories/<int:category_id>', views.category, name='category'),
    path('portfolio', views.portfolio, name='portfolio')
]
