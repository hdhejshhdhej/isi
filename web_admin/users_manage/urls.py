from django.urls import path
from .views import CartItemViews

urlpatterns = [
    path('pay/', CartItemViews.as_view())
]


# python manage.py runserver 194.180.191.40:8005