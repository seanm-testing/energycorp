import datetime
from django.test import TestCase
from django.db import IntegrityError
from rest_framework.test import APIClient
from contract.models import Contract, Invoice
from contract.utils import generateHistoryAndInvoices
from energytransfers.models import History
from tests.helpers import (
    create_custom_user, create_client, create_substation,
    create_transformator, create_counter, create_commercial,
    create_contract, create_invoice, create_history
)


# ====================== Model Tests ======================

class ContractModelTests(TestCase):

    def setUp(self):
        self.user = create_custom_user('1111111', 'CU', 'cu@t.com', '1111111')
        self.client_obj = create_client(self.user)
        sub = create_substation()
        trans = create_transformator(sub)
        self.counter = create_counter(trans)

    def test_create(self):
        contract = create_contract(self.client_obj, self.counter)
        self.assertEqual(contract.client, self.client_obj)
        self.assertEqual(contract.counter, self.counter)

    def test_protect_on_client_delete(self):
        create_contract(self.client_obj, self.counter)
        with self.assertRaises(Exception):
            self.client_obj.delete()

    def test_protect_on_counter_delete(self):
        create_contract(self.client_obj, self.counter)
        with self.assertRaises(Exception):
            self.counter.delete()


class InvoiceModelTests(TestCase):

    def setUp(self):
        self.user = create_custom_user('1111111', 'IU', 'iu@t.com', '1111111')
        self.client_obj = create_client(self.user)
        sub = create_substation()
        trans = create_transformator(sub)
        self.counter = create_counter(trans)
        self.contract = create_contract(self.client_obj, self.counter)
        self.commercial = create_commercial()

    def test_create_with_all_fields(self):
        inv = create_invoice(self.contract, self.commercial)
        self.assertIsNotNone(inv.codeInvoice)
        self.assertEqual(inv.contract, self.contract)
        self.assertFalse(inv.stateInvoice)

    def test_defaults(self):
        inv = create_invoice(self.contract, self.commercial)
        self.assertTrue(inv.is_active)
        self.assertEqual(inv.interestMora, 0.0)


# ====================== Business Logic Tests ======================

class GenerateHistoryAndInvoicesTests(TestCase):

    def _setup_contract(self, counter_value=500, stratum=3, interes_mora=0.0):
        user = create_custom_user(
            str(self._counter), f'U{self._counter}',
            f'u{self._counter}@t.com', str(self._counter)
        )
        self._counter += 1
        cl = create_client(user)
        sub = create_substation(str(self._counter), str(self._counter))
        trans = create_transformator(sub, str(self._counter), str(self._counter))
        self._counter += 1
        counter = create_counter(trans, value=counter_value, stratum=stratum,
                                 address=f'Addr{self._counter}')
        return create_contract(cl, counter, interes_mora=interes_mora)

    def setUp(self):
        self._counter = 1000000
        # generateHistoryAndInvoices creates invoices with default publicity_id=1
        from commercial.models import Commercial
        Commercial.objects.create(
            codeCommercial=1,
            urlCommercial='http://test.com',
            nameCommercial='Default',
            contractorCommercial='Corp',
            resourceCommercial='img.png',
            is_active=True
        )

    def test_first_invoice_no_prior_history(self):
        contract = self._setup_contract(counter_value=200, stratum=1)
        generateHistoryAndInvoices()
        self.assertEqual(History.objects.filter(counter=contract.counter).count(), 1)
        self.assertEqual(Invoice.objects.filter(contract=contract).count(), 1)
        inv = Invoice.objects.get(contract=contract)
        self.assertEqual(inv.pastRecord, 0)
        self.assertEqual(inv.currentRecord, 200)

    def test_stratum1_subsidy_60(self):
        contract = self._setup_contract(counter_value=100, stratum=1)
        generateHistoryAndInvoices()
        inv = Invoice.objects.get(contract=contract)
        basic_cost = 100 * 589
        expected = (1 - 0.6) * basic_cost
        self.assertAlmostEqual(inv.total, expected, places=0)

    def test_stratum2_subsidy_50(self):
        contract = self._setup_contract(counter_value=100, stratum=2)
        generateHistoryAndInvoices()
        inv = Invoice.objects.get(contract=contract)
        basic_cost = 100 * 589
        expected = (1 - 0.5) * basic_cost
        self.assertAlmostEqual(inv.total, expected, places=0)

    def test_stratum3_subsidy_15(self):
        contract = self._setup_contract(counter_value=100, stratum=3)
        generateHistoryAndInvoices()
        inv = Invoice.objects.get(contract=contract)
        basic_cost = 100 * 589
        expected = (1 - 0.15) * basic_cost
        self.assertAlmostEqual(inv.total, expected, places=0)

    def test_stratum4_no_subsidy(self):
        contract = self._setup_contract(counter_value=100, stratum=4)
        generateHistoryAndInvoices()
        inv = Invoice.objects.get(contract=contract)
        basic_cost = 100 * 589
        self.assertAlmostEqual(inv.total, basic_cost, places=0)

    def test_basic_take_split_at_173(self):
        contract = self._setup_contract(counter_value=200, stratum=4)
        generateHistoryAndInvoices()
        inv = Invoice.objects.get(contract=contract)
        self.assertEqual(inv.basicTake, 173)
        self.assertEqual(inv.remainder, 27)

    def test_consumption_calc(self):
        contract = self._setup_contract(counter_value=500, stratum=1)
        create_history(contract.counter, current=300, consumption=300)
        generateHistoryAndInvoices()
        inv = Invoice.objects.get(contract=contract)
        self.assertEqual(inv.currentRecord, 500)
        self.assertEqual(inv.pastRecord, 300)

    def test_inactive_counter_skipped(self):
        contract = self._setup_contract(counter_value=100, stratum=1)
        contract.counter.is_active = False
        contract.counter.save()
        generateHistoryAndInvoices()
        self.assertEqual(Invoice.objects.filter(contract=contract).count(), 0)


# ====================== API Tests ======================

class ContractAPITests(TestCase):

    def setUp(self):
        self.api = APIClient()
        user = create_custom_user('1111111', 'CA', 'ca@t.com', '1111111')
        self.client_obj = create_client(user)
        sub = create_substation()
        trans = create_transformator(sub)
        self.counter = create_counter(trans)
        self.contract = create_contract(self.client_obj, self.counter)

    def test_contract_list(self):
        resp = self.api.get('/api/invoice/contract/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data), 1)

    def test_contract_create(self):
        sub2 = create_substation('50.0', '50.0')
        trans2 = create_transformator(sub2, '50.0', '50.0')
        counter2 = create_counter(trans2, value=100, stratum=1, address='New')
        user2 = create_custom_user('2222222', 'CA2', 'ca2@t.com', '2222222')
        cl2 = create_client(user2)
        resp = self.api.post('/api/invoice/contract/create/', {
            'interes_mora': 0.0,
            'client': cl2.pk,
            'counter': counter2.pk
        })
        self.assertEqual(resp.status_code, 201)

    def test_invoice_list(self):
        create_invoice(self.contract)
        resp = self.api.get('/api/invoice/')
        self.assertEqual(resp.status_code, 200)
        self.assertGreaterEqual(len(resp.data), 1)

    def test_invoice_detail(self):
        inv = create_invoice(self.contract)
        resp = self.api.get(f'/api/invoice/{inv.pk}/')
        self.assertEqual(resp.status_code, 200)


class InvoiceQueryTests(TestCase):

    def setUp(self):
        self.api = APIClient()
        user = create_custom_user('1111111', 'IQ', 'iq@t.com', '1111111')
        cl = create_client(user)
        sub = create_substation()
        trans = create_transformator(sub)
        counter = create_counter(trans)
        self.contract = create_contract(cl, counter)
        self.invoice = create_invoice(self.contract)

    def test_get_invoice_by_contract_found(self):
        resp = self.api.post('/api/invoice/by-contract/', {
            'contractNumber': self.contract.pk
        })
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.data['find'])

    def test_get_invoice_by_contract_not_found(self):
        resp = self.api.post('/api/invoice/by-contract/', {
            'contractNumber': 99999
        })
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(resp.data['find'])

    def test_generate_invoices_endpoint(self):
        resp = self.api.get('/api/invoice/generate/')
        self.assertEqual(resp.status_code, 200)
