import django_filters
from .models import Activity

class ActivityFilter(django_filters.FilterSet):
    date_from = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name='date', lookup_expr='lte')
    sub_branch = django_filters.NumberFilter(field_name='sub_branch')
    
    class Meta:
        model = Activity
        fields = ['date', 'sub_branch']
