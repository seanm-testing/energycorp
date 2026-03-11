from django.test import TestCase
from rest_framework.test import APIClient
from energytransfers.models import Substation, Transformator, Counter
from tests.helpers import (
    create_substation, create_transformator, create_counter, create_history
)


# ====================== Model Tests ======================

class SubstationModelTests(TestCase):

    def test_create(self):
        sub = create_substation('1.0', '2.0')
        self.assertEqual(sub.latitudeSubstation, '1.0')

    def test_default_is_active(self):
        sub = Substation.objects.create(
            latitudeSubstation='1.0', lengthSubstation='2.0')
        self.assertTrue(sub.is_active)

    def test_str(self):
        sub = create_substation('1.0', '2.0')
        self.assertIn('1.0', str(sub))


class TransformatorModelTests(TestCase):

    def test_create_with_fk(self):
        sub = create_substation()
        trans = create_transformator(sub)
        self.assertEqual(trans.substationTransformator, sub)

    def test_cascade_delete(self):
        sub = create_substation()
        create_transformator(sub)
        sub.delete()
        self.assertEqual(Transformator.objects.count(), 0)

    def test_str(self):
        sub = create_substation()
        trans = create_transformator(sub, '5.0', '6.0')
        self.assertIn('5.0', str(trans))


class CounterModelTests(TestCase):

    def test_create(self):
        sub = create_substation()
        trans = create_transformator(sub)
        counter = create_counter(trans, value=100, stratum=2)
        self.assertEqual(counter.value, 100)
        self.assertEqual(counter.stratum, 2)

    def test_fk_to_transformator(self):
        sub = create_substation()
        trans = create_transformator(sub)
        counter = create_counter(trans)
        self.assertEqual(counter.transformatorCounter, trans)

    def test_cascade_from_transformator(self):
        sub = create_substation()
        trans = create_transformator(sub)
        create_counter(trans)
        trans.delete()
        self.assertEqual(Counter.objects.count(), 0)


class HistoryModelTests(TestCase):

    def test_create(self):
        sub = create_substation()
        trans = create_transformator(sub)
        counter = create_counter(trans)
        h = create_history(counter, 200, 100)
        self.assertEqual(h.current, 200)
        self.assertIsNotNone(h.registryHistory)

    def test_fk_to_counter(self):
        sub = create_substation()
        trans = create_transformator(sub)
        counter = create_counter(trans)
        h = create_history(counter)
        self.assertEqual(h.counter, counter)


# ====================== API Tests ======================

class SubstationAPITests(TestCase):

    def setUp(self):
        self.api = APIClient()
        self.sub = create_substation('10.0', '20.0')

    def test_list(self):
        resp = self.api.get('/api/energytransfers/substation/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data), 1)

    def test_create(self):
        resp = self.api.post('/api/energytransfers/substation/create/', {
            'latitudeSubstation': '3.0',
            'lengthSubstation': '4.0',
            'is_active': True
        })
        self.assertEqual(resp.status_code, 201)

    def test_detail(self):
        resp = self.api.get(f'/api/energytransfers/substation/{self.sub.pk}/')
        self.assertEqual(resp.status_code, 200)

    def test_update(self):
        resp = self.api.put(
            f'/api/energytransfers/substation/update/{self.sub.pk}/',
            {'latitudeSubstation': '99.0', 'lengthSubstation': '88.0'}
        )
        self.assertEqual(resp.status_code, 200)
        self.sub.refresh_from_db()
        self.assertEqual(self.sub.latitudeSubstation, '99.0')

    def test_inactivate(self):
        resp = self.api.patch(
            f'/api/energytransfers/substation/inactivate/{self.sub.pk}/',
            {'is_active': False}
        )
        self.assertEqual(resp.status_code, 200)
        self.sub.refresh_from_db()
        self.assertFalse(self.sub.is_active)

    def test_delete(self):
        resp = self.api.delete(f'/api/energytransfers/substation/delete/{self.sub.pk}')
        self.assertEqual(resp.status_code, 204)


class TransformatorAPITests(TestCase):

    def setUp(self):
        self.api = APIClient()
        self.sub = create_substation()
        self.trans = create_transformator(self.sub)

    def test_list(self):
        resp = self.api.get('/api/energytransfers/transformator/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data), 1)

    def test_create(self):
        resp = self.api.post('/api/energytransfers/transformator/create/', {
            'latitudeTransformator': '1.0',
            'lengthTransformator': '2.0',
            'is_active': True,
            'substationTransformator': self.sub.pk
        })
        self.assertEqual(resp.status_code, 201)

    def test_detail(self):
        resp = self.api.get(f'/api/energytransfers/transformator/{self.trans.pk}')
        self.assertEqual(resp.status_code, 200)

    def test_update(self):
        resp = self.api.put(
            f'/api/energytransfers/transformator/update/{self.trans.pk}',
            {
                'latitudeTransformator': '50.0',
                'lengthTransformator': '60.0',
                'substationTransformator': self.sub.pk
            }
        )
        self.assertEqual(resp.status_code, 200)

    def test_delete(self):
        resp = self.api.delete(f'/api/energytransfers/transformator/delete/{self.trans.pk}')
        self.assertEqual(resp.status_code, 204)


class CounterAPITests(TestCase):

    def setUp(self):
        self.api = APIClient()
        self.sub = create_substation()
        self.trans = create_transformator(self.sub)
        self.counter = create_counter(self.trans)

    def test_list(self):
        resp = self.api.get('/api/energytransfers/counter/')
        self.assertEqual(resp.status_code, 200)

    def test_create(self):
        resp = self.api.post('/api/energytransfers/counter/create/', {
            'latitudeCounter': '1.0', 'lengthCounter': '2.0',
            'value': 100, 'is_active': True, 'addressCounter': 'Calle X',
            'stratum': 1, 'transformatorCounter': self.trans.pk
        })
        self.assertEqual(resp.status_code, 201)

    def test_detail(self):
        resp = self.api.get(f'/api/energytransfers/counter/{self.counter.pk}')
        self.assertEqual(resp.status_code, 200)

    def test_update(self):
        resp = self.api.put(f'/api/energytransfers/counter/update/{self.counter.pk}', {
            'latitudeCounter': '9.0', 'lengthCounter': '9.0',
            'value': 999, 'addressCounter': 'New',
            'stratum': 4, 'transformatorCounter': self.trans.pk
        })
        self.assertEqual(resp.status_code, 200)

    def test_delete(self):
        resp = self.api.delete(f'/api/energytransfers/counter/delete/{self.counter.pk}')
        self.assertEqual(resp.status_code, 204)


class HistoryAPITests(TestCase):

    def setUp(self):
        self.api = APIClient()
        sub = create_substation()
        trans = create_transformator(sub)
        self.counter = create_counter(trans)
        self.history = create_history(self.counter, 300, 150)

    def test_list(self):
        resp = self.api.get('/api/energytransfers/history/')
        self.assertEqual(resp.status_code, 200)

    def test_create(self):
        resp = self.api.post('/api/energytransfers/history/create/', {
            'counter': self.counter.pk, 'current': 400, 'consumption': 100
        })
        self.assertEqual(resp.status_code, 201)

    def test_detail(self):
        resp = self.api.get(f'/api/energytransfers/history/{self.history.pk}/')
        self.assertEqual(resp.status_code, 200)

    def test_update(self):
        resp = self.api.patch(
            f'/api/energytransfers/history/update/{self.history.pk}/',
            {'consumption': 999}
        )
        self.assertEqual(resp.status_code, 200)

    def test_delete(self):
        resp = self.api.delete(f'/api/energytransfers/history/delete/{self.history.pk}')
        self.assertEqual(resp.status_code, 204)


class HistoryLastFiveTests(TestCase):

    def setUp(self):
        self.api = APIClient()
        sub = create_substation()
        trans = create_transformator(sub)
        self.counter = create_counter(trans)
        for i in range(7):
            create_history(self.counter, current=100 + i * 10, consumption=10)

    def test_returns_max_five(self):
        resp = self.api.get(f'/api/energytransfers/history/last/{self.counter.pk}')
        self.assertEqual(resp.status_code, 200)
        self.assertLessEqual(len(resp.data), 5)

    def test_empty_counter(self):
        sub = create_substation('9.0', '9.0')
        trans = create_transformator(sub, '9.0', '9.0')
        empty_counter = create_counter(trans, value=0, stratum=1, address='Empty')
        resp = self.api.get(f'/api/energytransfers/history/last/{empty_counter.pk}')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data), 0)
