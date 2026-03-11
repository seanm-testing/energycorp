from rest_framework.views import View, APIView

from energytransfers.models import Counter
from contract.models import Contract, Invoice
from payments.models import Payment
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

import json
import datetime
from django.db.models import F, Sum

from django.http import HttpResponse

from .serializers import (
    ServiceSuspendedSerializer,
    OverdueClientSerializer,
)

from .permissions import AllowManager
from users.models import Client

from django.db.models import Count
# Create your views here.


def get_active_client_count():
    return Client.objects.filter(user__is_active=True).count()

class MoraAndSuspended(View):
    def get(self, request):
        queryset1 =  Contract.objects.exclude(
            interes_mora__iexact=0.0).exclude(counter__is_active=False).filter(
                client__user__is_active=True).annotate(
                        id=F( 'client__id'),
                        name= F('client__user__name')

                ).values('id','interes_mora', 'name')

        queryset = Contract.objects.exclude(counter__is_active=True).filter(
                client__user__is_active=True)

        query = ServiceSuspendedSerializer(
            queryset,many=True
        ).data





        dicc= []
        for i in range(len(query)):
            datos = {

                "id": "",
                "name":"",
                "codeCounter": "",
                "is_active":""
            }
            datos['id']= query[i]['client']['id']
            datos['name']= query[i]['client']['user']['name']
            datos['codeCounter']= query[i]['counter']['codeCounter']
            datos['is_active']= query[i]['counter']['is_active']

            dicc.append(datos)

        response={
            "mora":"",
            "suspended":"",
            "numclientsmora":"",
            "numclientsuspended":""
        }
        response['mora']=list(queryset1)
        response['suspended']=dicc
        response['numclientsmora']=len(queryset1)
        response['numclientsuspended']=len(dicc)



        return HttpResponse(json.dumps(response))

class TopFiveCounters(View):
     def get(self, request):
        queryset1 =   Counter.objects.all(

        ).order_by('-value')[:5].values('codeCounter',
            'latitudeCounter',
            'lengthCounter',
            'value',
            'addressCounter',
            'stratum',
            'transformatorCounter')
        queryset2 =   Counter.objects.all(
        ).order_by('value')[:5].values('codeCounter',
            'latitudeCounter',
            'lengthCounter',
            'value',
            'addressCounter',
            'stratum',
            'transformatorCounter')

        response={
            "topfiveplus":"" ,
            "topfiveminus":""
        }
        response['topfiveplus']=list(queryset1)
        response['topfiveminus']=list(queryset2)


        return HttpResponse(json.dumps(response))

class QuantityCounterTransformator(View):
    def get(self, request):
        queryset=Counter.objects.values(
            'transformatorCounter').annotate(
                total=Count('codeCounter')).filter(
                    transformatorCounter__is_active=True
                )



        return HttpResponse(json.dumps(list(queryset)))


class OverdueClients(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowManager]

    def get(self, request):
        threshold_date = datetime.date.today() - datetime.timedelta(days=30)
        invoices = Invoice.objects.filter(
            stateInvoice=False,
            billingDate__lte=threshold_date
        ).select_related('contract__client__user')

        results = []
        for invoice in invoices:
            contract = invoice.contract
            client = contract.client
            days_overdue = (datetime.date.today() - invoice.billingDate).days
            results.append({
                'client_name': client.user.name,
                'contract_number': contract.contractNumber,
                'invoice_date': invoice.billingDate,
                'amount_owed': invoice.total,
                'days_overdue': days_overdue,
            })

        serializer = OverdueClientSerializer(results, many=True)
        return Response(serializer.data)


class PaymentSummary(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowManager]

    def get(self, request):
        summary = Payment.objects.aggregate(
            total_payments=Count('codePayment'),
            total_value=Sum('valuePayment'),
        )
        summary['total_value'] = summary['total_value'] or 0
        return Response(summary)


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
COMENT"""    
