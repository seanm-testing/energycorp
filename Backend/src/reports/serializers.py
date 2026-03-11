from rest_framework import serializers
from users.models import (
    CustomUser,
    Client
    )
from energytransfers.models import Counter
from contract.models import Contract


class OverdueClientSerializer(serializers.Serializer):
    client_name = serializers.CharField()
    contract_number = serializers.IntegerField()
    invoice_date = serializers.DateField()
    amount_owed = serializers.FloatField()
    days_overdue = serializers.IntegerField()

class getNameUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = [
            'name', 
        ]


class MoraSerializer(serializers.ModelSerializer):
    
    user = getNameUserSerializer()
    class Meta:
        model = Client
        fields = [
            'id',    
            'user',
        ]
class ReportsCounterSerializer(serializers.ModelSerializer):
    """Counter para las operaciones Retrive"""    
    class Meta:
        model = Counter
        fields = [
            'codeCounter',
            'is_active'
            ]
class ServiceSuspendedSerializer(serializers.ModelSerializer):
    
    
    client = MoraSerializer()
    counter = ReportsCounterSerializer()
    class Meta:
        model = Contract
        fields = [
          #  'contractNumber',
            'client',
            'counter'          
            ]

"""
COMENT
COMENT
COMENT
COMENT
COMENT
COMENT
COMENT
COMENT

COMENT
COMENT
COMENT

COMENT
COMENT
COMENT
COMENT

COMENT
COMENT
COMENT
COMENT

COMENT
COMENT
COMENT
COMENT

COMENT
COMENT
COMENT
COMENT
COMENT
COMENT

COMENT
COMENT
COMENT
COMENT

COMENT
COMENT
COMENT
COMENT
COMENT
COMENT

COMENT
COMENT
COMENT

COMENT
COMENT

COMENT
COMENT

COMENT
COMENT
COMENT
COMENT

COMENT
COMENT

COMENT
COMENT
COMENT
COMENT

COMENT
COMENT

COMENT
COMENT
COMENT

COMENT
COMENT

COMENT
COMENT
COMENT
COMENT

COMENT
COMENT
COMENT
COMENT
COMENT

COMENT
COMENT
COMENT
COMENT
COMENT
COMENT

COMENT
COMENT
COMENT
COMENT
COMENT

COMENT
COMENT
COMENT
COMENT
COMENT
COMENT

COMENT
COMENT
COMENT
COMENT
COMENT
COMENT
COMENT
COMENT
COMENT
COMENT
COMENT
COMENT
COMENT
COMENT
COMENT
COMENT
COMENT
COMENT
COMENT
COMENT
COMENT
COMENT
COMENT
COMENT
COMENT
COMENT
COMENT

COMENT
COMENT
COMENT
COMENT
COMENT

COMENT
COMENT
COMENT
COMENT
COMENT

COMENT
COMENT
COMENT

COMENT
COMENT

COMENT

COMENT
COMENT

COMENT

COMENT
COMENT

COMENT
COMENT

COMENT
COMENT

COMENT
COMENT
COMENT

COMENT
COMENT
COMENT
COMENT

COMENT
COMENT
COMENT

COMENT
COMENT
"""