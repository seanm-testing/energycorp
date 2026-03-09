import json
from django.test import TestCase, Client as DjangoClient
from tests.helpers import (
    create_custom_user, create_client, create_substation,
    create_transformator, create_counter, create_contract,
    create_invoice, create_commercial
)


class MoraAndSuspendedTests(TestCase):

    def setUp(self):
        self.http = DjangoClient()

    def test_returns_mora_clients(self):
        user = create_custom_user('1111111', 'M1', 'm1@t.com', '1111111')
        cl = create_client(user)
        sub = create_substation()
        trans = create_transformator(sub)
        counter = create_counter(trans)
        create_contract(cl, counter, interes_mora=0.3)
        resp = self.http.get('/api/reports/moraandsuspended/')
        data = json.loads(resp.content)
        self.assertEqual(resp.status_code, 200)
        self.assertGreaterEqual(data['numclientsmora'], 1)

    def test_returns_suspended_clients(self):
        user = create_custom_user('2222222', 'M2', 'm2@t.com', '2222222')
        cl = create_client(user)
        sub = create_substation('50.0', '50.0')
        trans = create_transformator(sub, '50.0', '50.0')
        counter = create_counter(trans, address='Susp')
        counter.is_active = False
        counter.save()
        create_contract(cl, counter)
        resp = self.http.get('/api/reports/moraandsuspended/')
        data = json.loads(resp.content)
        self.assertGreaterEqual(data['numclientsuspended'], 1)

    def test_empty_data(self):
        resp = self.http.get('/api/reports/moraandsuspended/')
        data = json.loads(resp.content)
        self.assertEqual(data['numclientsmora'], 0)
        self.assertEqual(data['numclientsuspended'], 0)


class TopFiveCountersTests(TestCase):

    def setUp(self):
        self.http = DjangoClient()
        sub = create_substation()
        trans = create_transformator(sub)
        for i in range(6):
            create_counter(trans, value=(i + 1) * 100, stratum=1,
                           address=f'Addr{i}')

    def test_top_five_highest(self):
        resp = self.http.get('/api/reports/topfive/')
        data = json.loads(resp.content)
        self.assertEqual(len(data['topfiveplus']), 5)
        values = [c['value'] for c in data['topfiveplus']]
        self.assertEqual(values, sorted(values, reverse=True))

    def test_top_five_lowest(self):
        resp = self.http.get('/api/reports/topfive/')
        data = json.loads(resp.content)
        self.assertEqual(len(data['topfiveminus']), 5)
        values = [c['value'] for c in data['topfiveminus']]
        self.assertEqual(values, sorted(values))


class QuantityCounterTransformatorTests(TestCase):

    def setUp(self):
        self.http = DjangoClient()
        sub = create_substation()
        self.trans1 = create_transformator(sub, '1.0', '1.0')
        self.trans2 = create_transformator(sub, '2.0', '2.0')
        create_counter(self.trans1, value=100, stratum=1, address='A1')
        create_counter(self.trans1, value=200, stratum=1, address='A2')
        create_counter(self.trans2, value=300, stratum=1, address='A3')

    def test_returns_counts(self):
        resp = self.http.get('/api/reports/quantitycounterfortransformator/')
        data = json.loads(resp.content)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(data), 2)

    def test_correct_totals(self):
        resp = self.http.get('/api/reports/quantitycounterfortransformator/')
        data = json.loads(resp.content)
        totals = {d['transformatorCounter']: d['total'] for d in data}
        self.assertEqual(totals[self.trans1.pk], 2)
        self.assertEqual(totals[self.trans2.pk], 1)
