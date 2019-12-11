from django.urls import path, include
from rest_framework import routers
from . import views



router = routers.DefaultRouter()
router.register(r'stockreading', views.StockReadingViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('sync', views.synchronize, name='sync'),
]
