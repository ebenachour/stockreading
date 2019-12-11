from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator


# Create your models here.
class StockReading(models.Model):
    id = models.AutoField(primary_key=True)
    ref_id = models.TextField(null=False,
                              validators=[MinLengthValidator(13), MaxLengthValidator(13)])
    expiration_date = models.DateTimeField()    
    modified = models.DateTimeField(auto_now=True)

    def get_from_id(self, pk):
        return StockReading.objects.get(id=pk)

    def get_from_ref_id(self, ref_id):
        return StockReading.objects.get(ref_id=ref_id)
    
    @property
    def stock_history(self):
        stock_histories = StockReadingHistory().get_all_from_ref(self.ref_id)
        return [{'id': stock_history.id,
                  'expiration_date': stock_history.expiration_date}
                  for stock_history in stock_histories]



class StockReadingHistory(models.Model):
    id = models.AutoField(primary_key=True)

    stock_reading_id = models.ForeignKey(StockReading, on_delete=models.CASCADE)
    stock_reading_ref = models.TextField()
    expiration_date = models.DateTimeField(null=False,
                              validators=[MinLengthValidator(13), MaxLengthValidator(13)])

    def get_all_from_ref(self, stock_ref):
        return StockReadingHistory.objects.filter(stock_reading_ref=stock_ref)
