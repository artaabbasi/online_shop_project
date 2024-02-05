from django.db.models.query import QuerySet


def search_queryset(queryset: QuerySet, fields: list, query_params: dict):
    for field in fields:
        if (field_search_value := query_params.get(field, None)) is not None:
            queryset = queryset.filter(**{f"{field}__icontains": field_search_value})
            
    return queryset

def filter_queryset(queryset: QuerySet, fields: list, query_params: dict):
    for field in fields:
        if (field_search_value := query_params.get(field, None)) is not None:
            queryset = queryset.filter(**{field: field_search_value})
            
    return queryset