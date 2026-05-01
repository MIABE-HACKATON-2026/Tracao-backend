from ninja_extra import api_controller, route
from tracability.models import ProductBatch
from tracability.schemas import ProductBatchSchema, ProductJourneySchema
from django.shortcuts import get_object_or_404

@api_controller('/tracability', auth=None)
class TracabilityController:
    
    @route.get('/batches', response=list[ProductBatchSchema])
    def get_all_batches(self):
        """Retourne la liste de tous les lots (batches) enregistrés."""
        return ProductBatch.objects.all().select_related('initial_stock')

    @route.get('/journey/{batch_number}', response=ProductJourneySchema)
    def get_product_journey(self, batch_number: str):
        """Retourne l'historique complet (la timeline) d'un lot spécifique en utilisant son UUID."""
        batch = get_object_or_404(
            ProductBatch.objects.prefetch_related('events', 'events__sender', 'events__receiver'),
            batch_number=batch_number
        )
        return batch
