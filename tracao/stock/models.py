from django.db import models
from user.models import TracaoUser

# Stock Management 


# Producteur

class StockProducer(models.Model):
    producer = models.ForeignKey(TracaoUser, on_delete=models.CASCADE, limit_choices_to={'is_producer': True}, related_name='producer_stocks')
    cooperative = models.ForeignKey(TracaoUser, on_delete=models.CASCADE, limit_choices_to={'is_cooperative_source': True}, related_name='cooperative_source_stocks')

    TYPE_CHOICES = [
        ('cacao', 'Cacao'),
        ('cafe', 'Cafe'),
    ]

    weight = models.FloatField(blank=True, null=True)
    date = models.DateField()
    product_type = models.CharField(max_length=100, choices=TYPE_CHOICES)
    species = models.TextField(blank=True, null=True)
    origin = models.CharField(max_length=200)
    surface_size = models.FloatField() # in hectares
    production_size = models.FloatField() # in Kg
    
    def __str__(self):
        return f"{self.producer.first_name} { self.producer.last_name} from {self.cooperative.cooperative_name}"
    

# coopérative d'origine

class StockOrigin(models.Model):
    cooperative = models.ForeignKey(TracaoUser, on_delete=models.CASCADE, limit_choices_to={'is_cooperative_source': True}, related_name='origin_stocks')
    producer_stock = models.ForeignKey(StockProducer, on_delete=models.CASCADE, related_name='origin_records')

    is_confirmed = models.BooleanField(default=False)
    
    
    def __str__(self):
        return f"{self.producer_stock.producer.first_name} { self.producer_stock.producer.last_name} from {self.cooperative.cooperative_name} with {self.producer_stock.weight}kg of {self.producer_stock.product_type}"


# Acheteur

class StockTransporter(models.Model):
    transporter = models.ForeignKey(TracaoUser, on_delete=models.CASCADE, limit_choices_to={'is_transporter': True}, related_name='transported_stocks')
    cooperative = models.ForeignKey(TracaoUser, on_delete=models.CASCADE, limit_choices_to={'is_cooperative_destination': True}, related_name='cooperative_destination_transports')
    stock_origin = models.ForeignKey(StockOrigin, on_delete=models.CASCADE, related_name='transporter_records')

    def __str__(self):
        return f"{self.transporter.first_name} { self.transporter.last_name} from {self.cooperative.cooperative_name}"


# # Coopérative d'arrivage

# class StockDestination(models.Model):
#     cooperative = models.ForeignKey(TracaoUser, on_delete=models.CASCADE, limit_choices_to={'is_cooperative_destination': True}, related_name='cooperative_destination_stocks')
#     transporter = models.ForeignKey(TracaoUser, on_delete=models.CASCADE, limit_choices_to={'is_transporter': True}, related_name='delivered_stocks')
#     stock_origin = models.ForeignKey(StockOrigin, on_delete=models.CASCADE, related_name='destination_records')

#     def __str__(self):
#         return f"{self.transporter.first_name} { self.transporter.last_name} to {self.cooperative.cooperative_name}"