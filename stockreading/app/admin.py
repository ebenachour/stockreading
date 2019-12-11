from django.contrib import admin

# Register your models here.
from .models import StockReading, StockReadingHistory

admin.site.register(StockReading)
admin.site.register(StockReadingHistory)
