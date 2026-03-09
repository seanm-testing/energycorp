import datetime
from django.test import TestCase
from rest_framework.test import APIClient
from payments.models import Payment, DirectPayment, BanckPayment
from tests.helpers import (
    create_custom_user, create_client, create_worker,
    create_substation, create_transformator, create_counter,
    create_contract, create_invoice, create_banck, create_commercial
)


class PaymentModelTests(TestCase):

    def setUp(self):
        user = create_custom_user('1111111', 'PM', 'pm@t.com', '1111111')
        cl = create_client(user)
        sub = create_substation()
        trans = create_transformator(sub)
        counter = create_counter(trans)
        self.contract = create_contract(cl, counter)
        self.commercial = create_commercial()
        self.invoice = create_invoice(self.contract, self.commercial)

    def test_create_payment(self):
        p = Payment.objects.create(
            valuePayment=50000,
            facturaPayment=self.invoice
        )
        self.assertEqual(p.valuePayment, 50000)
        self.assertIsNotNone(p.datePayment)

    def test_create_direct_payment(self):
        user_w = create_custom_user('2222222', 'WK', 'wk@t.com', '2222222')
        worker = create_worker(user_w, user_type=3)
        p = Payment.objects.create(valuePayment=50000, facturaPayment=self.invoice)
        dp = DirectPayment.objects.create(payment=p, workerPayment=worker)
        self.assertEqual(dp.payment, p)
        self.assertEqual(dp.workerPayment, worker)

    def test_create_banck_payment(self):
        banck = create_banck()
        p = Payment.objects.create(valuePayment=50000, facturaPayment=self.invoice)
        bp = BanckPayment.objects.create(payment=p, banckPayment=banck)
        self.assertEqual(bp.banckPayment, banck)


class PaymentAPITests(TestCase):

    def setUp(self):
        self.api = APIClient()
        user = create_custom_user('1111111', 'PA', 'pa@t.com', '1111111')
        cl = create_client(user)
        sub = create_substation()
        trans = create_transformator(sub)
        counter = create_counter(trans)
        self.contract = create_contract(cl, counter)
        self.commercial = create_commercial()
        self.invoice = create_invoice(self.contract, self.commercial)

    def test_list(self):
        resp = self.api.get('/api/pay/payment/')
        self.assertEqual(resp.status_code, 200)

    def test_create(self):
        resp = self.api.post('/api/pay/payment/create/', {
            'valuePayment': 50000,
            'facturaPayment': self.invoice.pk
        })
        self.assertEqual(resp.status_code, 201)

    def test_detail(self):
        p = Payment.objects.create(valuePayment=50000, facturaPayment=self.invoice)
        resp = self.api.get(f'/api/pay/payment/{p.pk}/')
        self.assertEqual(resp.status_code, 200)

    def test_by_contract(self):
        Payment.objects.create(valuePayment=50000, facturaPayment=self.invoice)
        resp = self.api.get(f'/api/pay/payment/bycontract/{self.contract.pk}')
        self.assertEqual(resp.status_code, 200)


class DirectPaymentAPITests(TestCase):

    def setUp(self):
        self.api = APIClient()
        user = create_custom_user('1111111', 'DP', 'dp@t.com', '1111111')
        cl = create_client(user)
        sub = create_substation()
        trans = create_transformator(sub)
        counter = create_counter(trans)
        self.contract = create_contract(cl, counter)
        self.commercial = create_commercial()
        # Make invoice with a past deadline so mora calc is predictable
        self.invoice = create_invoice(
            self.contract, self.commercial,
            deadDatePay=datetime.date.today() - datetime.timedelta(days=5)
        )
        user_w = create_custom_user('2222222', 'WK', 'wk@t.com', '2222222')
        self.worker = create_worker(user_w, user_type=3)

    def test_create(self):
        resp = self.api.post('/api/pay/directpayment/create/', {
            'payment': {
                'valuePayment': 50000,
                'facturaPayment': self.invoice.pk
            },
            'workerPayment': self.worker.pk
        }, format='json')
        self.assertEqual(resp.status_code, 201)
        # Invoice should be marked as paid
        self.invoice.refresh_from_db()
        self.assertTrue(self.invoice.stateInvoice)

    def test_list(self):
        resp = self.api.get('/api/pay/directpayment/')
        self.assertEqual(resp.status_code, 200)

    def test_by_worker(self):
        resp = self.api.get(f'/api/pay/directpayment/byworker/{self.worker.pk}')
        self.assertEqual(resp.status_code, 200)


class BanckPaymentAPITests(TestCase):

    def setUp(self):
        self.api = APIClient()
        user = create_custom_user('1111111', 'BP', 'bp@t.com', '1111111')
        cl = create_client(user)
        sub = create_substation()
        trans = create_transformator(sub)
        counter = create_counter(trans)
        self.contract = create_contract(cl, counter)
        self.commercial = create_commercial()
        self.invoice = create_invoice(
            self.contract, self.commercial,
            deadDatePay=datetime.date.today() - datetime.timedelta(days=3)
        )
        self.banck = create_banck()

    def test_create(self):
        resp = self.api.post('/api/pay/banckpayment/create/', {
            'payment': {
                'valuePayment': 50000,
                'facturaPayment': self.invoice.pk
            },
            'banckPayment': self.banck.pk
        }, format='json')
        self.assertEqual(resp.status_code, 201)
        self.invoice.refresh_from_db()
        self.assertTrue(self.invoice.stateInvoice)

    def test_list(self):
        resp = self.api.get('/api/pay/banckpayment/')
        self.assertEqual(resp.status_code, 200)
