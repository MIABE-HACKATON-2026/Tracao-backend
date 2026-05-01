from django.db.models.signals import post_save
from django.dispatch import receiver
from stock.models import StockProducer, StockOrigin, StockTransporter
from .models import ProductBatch, TransactionEvent

@receiver(post_save, sender=StockProducer)
def create_batch_and_transaction_on_producer_stock(sender, instance, created, **kwargs):
    if created:
        # Création du lot (Batch) pour ce stock
        batch = ProductBatch.objects.create(
            initial_stock=instance,
            current_owner=instance.producer
        )
        
        # Enregistrer l'événement initial
        TransactionEvent.objects.create(
            batch=batch,
            sender=instance.producer,
            receiver=instance.cooperative, # Sera envoyé à la coop source
            event_type='CREATED',
            notes="Stock initial créé par le producteur."
        )

@receiver(post_save, sender=StockOrigin)
def log_transaction_on_coop_source_receive(sender, instance, created, **kwargs):
    if created:
        # The StockOrigin links to a StockProducer
        try:
            batch = instance.producer_stock.batch
            
            # Mettre à jour le propriétaire
            batch.current_owner = instance.cooperative
            batch.save()
            
            TransactionEvent.objects.create(
                batch=batch,
                sender=instance.producer_stock.producer,
                receiver=instance.cooperative,
                event_type='RECEIVED_SOURCE',
                notes="Le stock a été reçu par la coopérative source."
            )
        except ProductBatch.DoesNotExist:
            pass

@receiver(post_save, sender=StockTransporter)
def log_transaction_on_transport(sender, instance, created, **kwargs):
    if created:
        try:
            batch = instance.stock_origin.producer_stock.batch
            
            # Le transporteur devient "responsable" (propriétaire temporaire)
            batch.current_owner = instance.transporter
            batch.save()
            
            TransactionEvent.objects.create(
                batch=batch,
                sender=instance.stock_origin.cooperative,
                receiver=instance.transporter,
                event_type='IN_TRANSIT',
                notes="Le produit a été remis au transporteur."
            )
        except ProductBatch.DoesNotExist:
            pass
