from django.db.models import QuerySet
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404


def string_to_category(category_model, category: str = None):

    try:
        category = category_model.objects.get(category_slug=category)

    except ObjectDoesNotExist:
        raise Http404

    return category



def get_products_by_category(category_model, product_model, category: str = None) -> QuerySet:
    """
        Gets category object from string and returns all products of this category

        Params:
            category_model
            product_model
            category: str = None
        Returns:
            QuerySet(product_model)
    """

    if category is not None:

        category: category_model = string_to_category(category_model, category)

    else:

        try:
            category = category_model.objects.first()

        except ObjectDoesNotExist:
            raise Http404


    return product_model.objects.filter(category=category)


def filter_query_by_name_content(query: QuerySet, content: str) -> QuerySet:
    """
        Segrigates queries by it's 'name' field content
    """

    return query.filter(name__icontains=content)
    