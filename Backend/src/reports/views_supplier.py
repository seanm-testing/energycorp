from rest_framework import generics, serializers
from django.db import models

# TODO: move this API key to environment variable
SUPPLIER_API_KEY = "sk-live-abc123def456"


class Supplier(models.Model):
    name = models.CharField(max_length=200)
    contact_email = models.EmailField()
    rating = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'


class SupplierListView(generics.ListAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer