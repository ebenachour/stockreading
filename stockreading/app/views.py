from django.shortcuts import render
from django.http import HttpResponse
from .serializers import StockReadingSerializer
from .models import StockReading, StockReadingHistory
from rest_framework import viewsets
from django.utils.timezone import make_aware
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from django.views.decorators.http import require_http_methods


class StockReadingViewSet(viewsets.ModelViewSet):
    queryset = StockReading.objects.all().order_by('id')
    serializer_class = StockReadingSerializer


    def create(self, request):
        # when we create  a new entry, we automatically add it in the history
        try:
            super().create(request)
            stockreading = StockReading().get_from_ref_id(request.data['ref_id'])
            stockistory = StockReadingHistory(
                    stock_reading_id=stockreading, 
                    stock_reading_ref=stockreading.ref_id,
                    expiration_date=request.data['expiration_date']
                    )
            stockistory.save()
            return HttpResponse(status=201)
        except ValidationError:
            return HttpResponse(status=400)
    
    def update(self, request, pk=None):
        if not pk:
            if ref_id not in request.data:
                return HttpResponse(status=401)
            stockreading = StockReading().get_from_ref_id(request.data['ref_id'])
            pk = stockreading.id
        else:
            stockreading = StockReading().get_from_id(pk)
        if not stockreading:
            return HttpResponse(status=404)
        stockreading.expiration_date = request.data['expiration_date']
        super().update(request, pk)
        stockistory = StockReadingHistory(
            stock_reading_id=stockreading, 
            stock_reading_ref=stockreading.ref_id,
            expiration_date=request.data['expiration_date']
            )
        # when we update, we add a line in history
        stockistory.save()
        return HttpResponse(status=200)
   


@require_http_methods("POST")
def synchronize(request):
    data = request.json
    for stockmobile in data['stock_reading']:
        ref_id = stockmobile['ref_id']
        expiration_date = stockmobile['expiration_date']
        modified_at = stockmobile['modified']

        stock_reading = StockReading().get_from_ref_id(ref_id)
        #  If the reference does not exist, i add
        if not stock_reading:
            stock_reading = StockReading(ref_id, expiration_date, modified_at)
        # if the mobile update is upper than the db update, we take the 
        if stock_reading.modified_at < modified_at:
            stock_reading.expiration_date = expiration_date
        # check if the expiration date exist on the history
        stock_reading.save()

        history_exist = False
        for history in stock_reading.stock_history:
            if history.expiration_date == expiration_date:
                history_exist = True
                break
        if not history_exist:
            stock_history = StockReadingHistory(stock_reading_id=stockreading, 
                stock_reading_ref=ref_id,
                expiration_date=expiration_date
                ))
            stock_history.save()
    return HttpResponse(status=200)
