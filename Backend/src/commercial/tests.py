from django.test import TestCase
from rest_framework.test import APIClient
from commercial.models import Commercial
from tests.helpers import create_commercial


class CommercialModelTests(TestCase):

    def test_create(self):
        c = create_commercial('Ad1', 'http://ad.com', 'Corp', 'res.png')
        self.assertEqual(c.nameCommercial, 'Ad1')

    def test_str(self):
        c = create_commercial('Ad1')
        self.assertIn('Ad1', str(c))


class CommercialAPITests(TestCase):

    def setUp(self):
        self.api = APIClient()
        self.comm = create_commercial()

    def test_list(self):
        resp = self.api.get('/api/commercial/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data), 1)

    def test_create(self):
        resp = self.api.post('/api/commercial/create/', {
            'urlCommercial': 'http://new.com',
            'nameCommercial': 'New',
            'contractorCommercial': 'NewCorp',
            'resourceCommercial': 'new.png',
            'is_active': True
        })
        self.assertEqual(resp.status_code, 201)

    def test_detail(self):
        resp = self.api.get(f'/api/commercial/{self.comm.pk}/')
        self.assertEqual(resp.status_code, 200)

    def test_update(self):
        resp = self.api.put(f'/api/commercial/update/{self.comm.pk}/', {
            'urlCommercial': 'http://upd.com',
            'nameCommercial': 'Upd',
            'contractorCommercial': 'UpdCorp',
            'resourceCommercial': 'upd.png'
        })
        self.assertEqual(resp.status_code, 200)
        self.comm.refresh_from_db()
        self.assertEqual(self.comm.nameCommercial, 'Upd')

    def test_inactivate(self):
        resp = self.api.patch(f'/api/commercial/inactivate/{self.comm.pk}/', {
            'is_active': False
        })
        self.assertEqual(resp.status_code, 200)
        self.comm.refresh_from_db()
        self.assertFalse(self.comm.is_active)

    def test_delete(self):
        resp = self.api.delete(f'/api/commercial/delete/{self.comm.pk}')
        self.assertEqual(resp.status_code, 204)
