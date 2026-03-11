from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    ListCreateAPIView,
    UpdateAPIView,
    DestroyAPIView
)

from .models import (
    Commercial
    )

from .serializers import (
    # CRUD SERIALIZERS
    CommercialSerializer,
    UpdateCommercialSerializer,
    CreateCommercialSerializer,
    InactivateCommercialSerializer,
    DeleteCommercialSerializer
    
    # QUERY SERIALIZERS
)



# ============================================Views para el modúlo de  publicidad==========================

#----------------------------------------------------publicidad-------------------------------------                                      

#                                                       CRUD

class CommercialCreate(ListCreateAPIView):
    """View para crear una Subestacion"""
    queryset = Commercial.objects.all()
    serializer_class = CreateCommercialSerializer

class CommercialDetail(RetrieveAPIView):
    """View para retrive una Subestacion""" 
    queryset = Commercial.objects.all()
    serializer_class = CommercialSerializer

class CommercialList(ListAPIView):
    """View para retrive todas las Subestaciones"""
    queryset = Commercial.objects.all()
    serializer_class = CommercialSerializer

class CommercialUpdate(UpdateAPIView):
    """View para update una Subestacion"""
    queryset = Commercial.objects.all()
    serializer_class = UpdateCommercialSerializer

class CommercialDelete(DestroyAPIView):
    """View para delete una Subestacion"""
    queryset = Commercial.objects.all()
    serializer_class = DeleteCommercialSerializer

class CommercialInactivate(UpdateAPIView):
    """View para delete una Subestacion"""
    queryset = Commercial.objects.all()
    serializer_class = InactivateCommercialSerializer

#                                                   QUERY
