import datetime
from users.models import CustomUser, Client, Worker
from energytransfers.models import Substation, Transformator, Counter, History
from commercial.models import Commercial
from contract.models import Contract, Invoice
from bancks.models import Banck


def create_custom_user(id_user, name, email, phone, password='testpass123',
                       address='Calle 1', neighborhood='Centro', **kwargs):
    return CustomUser.objects.create_user(
        email=email,
        password=password,
        id_user=id_user,
        name=name,
        phone=phone,
        address=address,
        neighborhood=neighborhood,
        **kwargs
    )


def create_client(user, type_client=1):
    return Client.objects.create(user=user, type_client=type_client)


def create_worker(user, user_type=1):
    return Worker.objects.create(user=user, user_type=user_type)


def create_substation(lat='4.123', lng='-74.456'):
    return Substation.objects.create(
        latitudeSubstation=lat,
        lengthSubstation=lng,
        is_active=True
    )


def create_transformator(substation, lat='4.200', lng='-74.500'):
    return Transformator.objects.create(
        latitudeTransformator=lat,
        lengthTransformator=lng,
        is_active=True,
        substationTransformator=substation
    )


def create_counter(transformator, value=500, stratum=3, address='Calle Test'):
    return Counter.objects.create(
        latitudeCounter='4.300',
        lengthCounter='-74.600',
        value=value,
        is_active=True,
        addressCounter=address,
        stratum=stratum,
        transformatorCounter=transformator
    )


def create_history(counter, current=100, consumption=50):
    return History.objects.create(
        counter=counter,
        current=current,
        consumption=consumption
    )


def create_commercial(name='TestAd', url='http://test.com',
                      contractor='TestCorp', resource='img.png'):
    return Commercial.objects.create(
        urlCommercial=url,
        nameCommercial=name,
        contractorCommercial=contractor,
        resourceCommercial=resource,
        is_active=True
    )


def create_contract(client, counter, interes_mora=0.0):
    return Contract.objects.create(
        client=client,
        counter=counter,
        interes_mora=interes_mora
    )


def create_invoice(contract, commercial=None, **kwargs):
    defaults = {
        'billingDate': datetime.date.today(),
        'deadDatePay': datetime.date.today() + datetime.timedelta(days=10),
        'counter': contract.counter.codeCounter,
        'address': contract.counter.addressCounter,
        'stratum': contract.counter.stratum,
        'currentRecord': 500,
        'pastRecord': 400,
        'basicTake': 100,
        'remainder': 0,
        'unitaryValue': 589,
        'interestMora': 0.0,
        'totalMora': 0,
        'overdue': 0,
        'intakes': '1-100',
        'referencecodeInvoice': 'REF123456',
        'total': 50065.0,
        'stateInvoice': False,
        'is_active': True,
        'contract': contract,
        'publicity': commercial or create_commercial(),
    }
    defaults.update(kwargs)
    return Invoice.objects.create(**defaults)


def create_banck(name='BancoTest', reference='REF001'):
    return Banck.objects.create(
        nameBanck=name,
        referenceBanck=reference,
        is_active=True
    )
