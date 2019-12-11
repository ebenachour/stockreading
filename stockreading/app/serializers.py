from rest_framework import serializers

from .models import StockReading, StockReadingHistory


class StockReadingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StockReading
        fields = ("ref_id", "expiration_date", "stock_history")
