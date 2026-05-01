from ninja_extra import api_controller,route
from ninja_extra.permissions import IsAuthenticated,AllowAny
from stock.schemas import StockProducerSchema,StockProducerCreate
from stock.models import StockProducer


@api_controller('/stock',auth=None)
class StockController:
    @route.post('/stock_producer',response=StockProducerSchema)
    def create_stock_producer(self,stock_producer:StockProducerCreate):
        return stock_producer

    @route.get('/all_stock_producer',response=list[StockProducerSchema])
    def get_all_stock_producer(self):
        return StockProducer.objects.all()
    
    