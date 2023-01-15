
from cart.models import ProductImage
from django.db.models import Prefetch


def prefetch_photos(query, image_model=ProductImage, nested_prefetch=''):
    """
        Prefetching query with photos
    """

    prefetch = Prefetch(nested_prefetch + 'images', queryset=image_model.objects.distinct(), to_attr='photo')
    query = query.prefetch_related(prefetch)

    return query
