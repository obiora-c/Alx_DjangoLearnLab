

import django_filters as df
from .models import Product


class ProductFilter(df.FilterSet):
        min_price = df.NumberFilter(field_name="price", lookup_expr="gte")
        max_price = df.NumberFilter(field_name="price", lookup_expr="lte")
        category = df.CharFilter(field_name="category__slug", lookup_expr="iexact")
        in_stock = df.BooleanFilter(method="filter_in_stock")


        class Meta:
            model = Product
            fields = ["category", "min_price", "max_price", "in_stock"]


        def filter_in_stock(self, queryset, name, value):
            if value is True:
              return queryset.filter(stock_quantity__gt=0)
            if value is False:
              return queryset.filter(stock_quantity__lte=0)
            return queryset
