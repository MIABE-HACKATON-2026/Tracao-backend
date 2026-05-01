from ninja import Schema, ModelSchema
from stock.models import StockProducer,StockOrigin,StockTransporter


class StockProducerSchema(ModelSchema):
    class Meta:
        model = StockProducer
        fields = ['producer','cooperative','weight','date','product_type','species','origin','surface_size','production_size']

class StockOriginSchema(ModelSchema):
    class Meta:
        model = StockOrigin
        fields = ['cooperative','producer_stock','is_confirmed']

class StockTransporterSchema(ModelSchema):
    class Meta:
        model = StockTransporter
        fields = ['transporter','cooperative','stock_origin']

class StockProducerCreate(Schema):
    producer: int
    cooperative: int
    weight: float
    date: str
    product_type: str
    species: str
    origin: str
    surface_size: float
    production_size: float

