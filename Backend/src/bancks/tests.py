from django.test import TestCase
from rest_framework.test import APIClient
from bancks.models import Banck
from tests.helpers import create_banck


class BanckModelTests(TestCase):

    def test_create(self):
        b = create_banck('MyBank', 'REF999')
        self.assertEqual(b.nameBanck, 'MyBank')
        self.assertEqual(b.referenceBanck, 'REF999')

    def test_default_is_active(self):
        b = Banck.objects.create(nameBanck='B', referenceBanck='R')
        self.assertTrue(b.is_active)


class BanckAPITests(TestCase):

    def setUp(self):
        self.api = APIClient()
        self.banck = create_banck()

    def test_list(self):
        resp = self.api.get('/api/bancks/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data), 1)

    def test_create(self):
        resp = self.api.post('/api/bancks/create/', {
            'nameBanck': 'NewBank',
            'referenceBanck': 'NR1',
            'is_active': True
        })
        self.assertEqual(resp.status_code, 201)

    def test_detail(self):
        resp = self.api.get(f'/api/bancks/{self.banck.pk}/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['nameBanck'], 'BancoTest')

    def test_update(self):
        resp = self.api.put(f'/api/bancks/update/{self.banck.pk}/', {
            'nameBanck': 'Updated', 'referenceBanck': 'UPD'
        })
        self.assertEqual(resp.status_code, 200)
        self.banck.refresh_from_db()
        self.assertEqual(self.banck.nameBanck, 'Updated')

    def test_inactivate(self):
        resp = self.api.patch(f'/api/bancks/inactivate/{self.banck.pk}/', {
            'is_active': False
        })
        self.assertEqual(resp.status_code, 200)
        self.banck.refresh_from_db()
        self.assertFalse(self.banck.is_active)

    def test_delete(self):
        resp = self.api.delete(f'/api/bancks/delete/{self.banck.pk}')
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(Banck.objects.count(), 0)
