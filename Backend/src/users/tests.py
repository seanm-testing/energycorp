from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.hashers import check_password
from users.models import CustomUser, Client, Worker
from tests.helpers import create_custom_user, create_client, create_worker


# ====================== Model Tests ======================

class CustomUserModelTests(TestCase):

    def test_create_user(self):
        user = create_custom_user('1234567', 'Test User', 'test@test.com', '7654321')
        self.assertEqual(user.name, 'Test User')
        self.assertTrue(user.check_password('testpass123'))
        self.assertTrue(user.is_active)

    def test_create_user_no_email_raises(self):
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(email='', password='pass', id_user='111', name='X', phone='1111111')

    def test_create_staffuser(self):
        user = CustomUser.objects.create_staffuser(
            email='staff@test.com', password='pass',
            id_user='2222222', name='Staff', phone='2222222',
            address='A', neighborhood='B'
        )
        self.assertTrue(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        user = CustomUser.objects.create_superuser(
            email='super@test.com', password='pass',
            id_user='3333333', name='Super', phone='3333333',
            address='A', neighborhood='B'
        )
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_email_unique(self):
        create_custom_user('1111111', 'A', 'dup@test.com', '1111111')
        with self.assertRaises(Exception):
            create_custom_user('2222222', 'B', 'dup@test.com', '2222222')

    def test_phone_unique(self):
        create_custom_user('1111111', 'A', 'a@test.com', '1111111')
        with self.assertRaises(Exception):
            create_custom_user('2222222', 'B', 'b@test.com', '1111111')

    def test_get_full_name(self):
        user = create_custom_user('1234567', 'Full Name', 'fn@test.com', '7654321')
        self.assertEqual(user.get_full_name(), 'Full Name')

    def test_get_short_name(self):
        user = create_custom_user('1234567', 'Short', 'sn@test.com', '7654321')
        self.assertEqual(user.get_short_name(), 'Short')


class ClientModelTests(TestCase):

    def test_create_natural_client(self):
        user = create_custom_user('1111111', 'CL', 'cl@t.com', '1111111')
        client = create_client(user, type_client=1)
        self.assertEqual(client.type_client, 1)
        self.assertEqual(client.user, user)

    def test_create_juridica_client(self):
        user = create_custom_user('2222222', 'CL2', 'cl2@t.com', '2222222')
        client = create_client(user, type_client=2)
        self.assertEqual(client.type_client, 2)

    def test_cascade_delete_from_user(self):
        user = create_custom_user('3333333', 'CL3', 'cl3@t.com', '3333333')
        create_client(user)
        user.delete()
        self.assertEqual(Client.objects.count(), 0)


class WorkerModelTests(TestCase):

    def test_create_admin_worker(self):
        user = create_custom_user('1111111', 'W1', 'w1@t.com', '1111111')
        worker = create_worker(user, user_type=1)
        self.assertEqual(worker.user_type, 1)

    def test_create_manager_worker(self):
        user = create_custom_user('2222222', 'W2', 'w2@t.com', '2222222')
        worker = create_worker(user, user_type=2)
        self.assertEqual(worker.user_type, 2)

    def test_create_operator_worker(self):
        user = create_custom_user('3333333', 'W3', 'w3@t.com', '3333333')
        worker = create_worker(user, user_type=3)
        self.assertEqual(worker.user_type, 3)


# ====================== Login View Tests ======================

class LoginViewTests(TestCase):

    def setUp(self):
        self.client_api = APIClient()
        self.user = create_custom_user('1111111', 'Login User', 'login@test.com', '1111111')
        create_worker(self.user, user_type=1)

    def test_login_success(self):
        resp = self.client_api.post('/api/user/login/', {
            'id_user': 'login@test.com', 'password': 'testpass123'
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['code'], 200)
        self.assertIn('token', resp.data)

    def test_login_wrong_password(self):
        resp = self.client_api.post('/api/user/login/', {
            'id_user': 'login@test.com', 'password': 'wrong'
        })
        self.assertEqual(resp.data['code'], 204)

    def test_login_nonexistent_user(self):
        resp = self.client_api.post('/api/user/login/', {
            'id_user': 'nobody@test.com', 'password': 'testpass123'
        })
        self.assertEqual(resp.data['code'], 204)

    def test_login_inactive_user(self):
        self.user.is_active = False
        self.user.save()
        resp = self.client_api.post('/api/user/login/', {
            'id_user': 'login@test.com', 'password': 'testpass123'
        })
        self.assertEqual(resp.data['code'], 204)

    def test_login_empty_credentials(self):
        resp = self.client_api.post('/api/user/login/', {})
        self.assertEqual(resp.data['code'], 204)


# ====================== User CRUD Tests ======================

class UserCRUDTests(TestCase):

    def setUp(self):
        self.client_api = APIClient()
        self.user = create_custom_user('1111111', 'U1', 'u1@t.com', '1111111')

    def test_user_list(self):
        resp = self.client_api.get('/api/user/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data), 1)

    def test_user_detail(self):
        resp = self.client_api.get(f'/api/user/{self.user.pk}/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['name'], 'U1')

    def test_user_create_hashes_password(self):
        resp = self.client_api.post('/api/user/create/', {
            'id_user': '2222222', 'name': 'U2', 'email': 'u2@t.com',
            'password': 'mypass', 'phone': '2222222',
            'address': 'A', 'neighborhood': 'B',
            'is_active': True, 'is_staff': True, 'is_superuser': False
        })
        self.assertEqual(resp.status_code, 201)
        user = CustomUser.objects.get(email='u2@t.com')
        self.assertTrue(check_password('mypass', user.password))

    def test_user_update(self):
        resp = self.client_api.put(f'/api/user/{self.user.pk}/update/', {
            'id_user': '1111111', 'name': 'Updated', 'email': 'u1@t.com',
            'password': 'newpass', 'phone': '1111111',
            'address': 'A', 'neighborhood': 'B',
            'is_active': True, 'is_staff': True, 'is_superuser': False
        })
        self.assertEqual(resp.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, 'Updated')

    def test_user_delete(self):
        resp = self.client_api.delete(f'/api/user/{self.user.pk}/delete/')
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(CustomUser.objects.count(), 0)

    def test_user_detail_404(self):
        resp = self.client_api.get('/api/user/9999/')
        self.assertEqual(resp.status_code, 404)

    def test_duplicate_email(self):
        resp = self.client_api.post('/api/user/create/', {
            'id_user': '2222222', 'name': 'U2', 'email': 'u1@t.com',
            'password': 'pass', 'phone': '2222222',
            'address': 'A', 'neighborhood': 'B',
            'is_active': True, 'is_staff': True, 'is_superuser': False
        })
        self.assertEqual(resp.status_code, 400)

    def test_invalid_phone(self):
        resp = self.client_api.post('/api/user/create/', {
            'id_user': 'abc', 'name': 'Bad', 'email': 'bad@t.com',
            'password': 'pass', 'phone': 'abc',
            'address': 'A', 'neighborhood': 'B',
            'is_active': True, 'is_staff': True, 'is_superuser': False
        })
        self.assertEqual(resp.status_code, 400)


# ====================== Client CRUD Tests ======================

class ClientCRUDTests(TestCase):

    def setUp(self):
        self.client_api = APIClient()
        self.user = create_custom_user('1111111', 'C1', 'c1@t.com', '1111111')
        self.cl = create_client(self.user, type_client=1)

    def test_client_list(self):
        resp = self.client_api.get('/api/user/client/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data), 1)

    def test_client_detail(self):
        resp = self.client_api.get(f'/api/user/client/{self.cl.pk}/')
        self.assertEqual(resp.status_code, 200)

    def test_client_create_existing_user(self):
        user2 = create_custom_user('2222222', 'C2', 'c2@t.com', '2222222')
        resp = self.client_api.post('/api/user/client/create/', {
            'user': user2.pk, 'type_client': 2
        })
        self.assertEqual(resp.status_code, 201)

    def test_client_create_new(self):
        resp = self.client_api.post('/api/user/client/create-new/', {
            'type_client': 1,
            'user': {
                'id_user': '3333333', 'name': 'New', 'email': 'new@t.com',
                'password': 'pass', 'phone': '3333333',
                'address': 'A', 'neighborhood': 'B',
                'is_active': True, 'is_staff': True, 'is_superuser': False
            }
        }, format='json')
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(Client.objects.filter(user__email='new@t.com').exists())

    def test_client_bulk_create(self):
        data = [{
            'type_client': 1,
            'user': {
                'id_user': '4444444', 'name': 'Bulk1', 'email': 'b1@t.com',
                'password': 'pass', 'phone': '4444444',
                'address': 'A', 'neighborhood': 'B',
                'is_active': True, 'is_staff': True, 'is_superuser': False
            }
        }]
        resp = self.client_api.post('/api/user/client/create/bulk/', data, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(Client.objects.filter(user__email='b1@t.com').exists())

    def test_client_delete(self):
        resp = self.client_api.delete(f'/api/user/client/{self.cl.pk}/delete/')
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(Client.objects.count(), 0)
        self.assertTrue(CustomUser.objects.filter(pk=self.user.pk).exists())

    def test_client_detail_404(self):
        resp = self.client_api.get('/api/user/client/9999/')
        self.assertEqual(resp.status_code, 404)


# ====================== Worker CRUD Tests ======================

class WorkerCRUDTests(TestCase):

    def setUp(self):
        self.client_api = APIClient()
        self.user = create_custom_user('1111111', 'W1', 'w1@t.com', '1111111')
        self.worker = create_worker(self.user, user_type=1)

    def test_worker_list(self):
        resp = self.client_api.get('/api/user/worker/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data), 1)

    def test_worker_detail(self):
        resp = self.client_api.get(f'/api/user/worker/{self.worker.pk}')
        self.assertEqual(resp.status_code, 200)

    def test_worker_create(self):
        user2 = create_custom_user('2222222', 'W2', 'w2@t.com', '2222222')
        resp = self.client_api.post('/api/user/worker/create/', {
            'user': user2.pk, 'user_type': 2
        })
        self.assertEqual(resp.status_code, 201)

    def test_worker_create_new(self):
        resp = self.client_api.post('/api/user/worker/create-new/', {
            'user_type': 3,
            'user': {
                'id_user': '3333333', 'name': 'NewW', 'email': 'nw@t.com',
                'password': 'pass', 'phone': '3333333',
                'address': 'A', 'neighborhood': 'B',
                'is_active': True, 'is_staff': True, 'is_superuser': False
            }
        }, format='json')
        self.assertEqual(resp.status_code, 201)

    def test_worker_bulk_create(self):
        data = [{
            'user_type': 2,
            'user': {
                'id_user': '4444444', 'name': 'BW', 'email': 'bw@t.com',
                'password': 'pass', 'phone': '4444444',
                'address': 'A', 'neighborhood': 'B',
                'is_active': True, 'is_staff': True, 'is_superuser': False
            }
        }]
        resp = self.client_api.post('/api/user/worker/create/bulk/', data, format='json')
        self.assertEqual(resp.status_code, 200)

    def test_worker_delete(self):
        resp = self.client_api.delete(f'/api/user/worker/{self.worker.pk}/delete')
        self.assertEqual(resp.status_code, 204)


# ====================== Permission Tests ======================

class PermissionTests(TestCase):

    def setUp(self):
        self.client_api = APIClient()

    def test_unauthenticated_returns_false(self):
        from users.views import AllowAdmin
        from rest_framework.test import APIRequestFactory
        factory = APIRequestFactory()
        request = factory.get('/')
        from django.contrib.auth.models import AnonymousUser
        request.user = AnonymousUser()
        perm = AllowAdmin()
        self.assertFalse(perm.has_permission(request, None))

    def test_allow_admin(self):
        from users.views import AllowAdmin
        from rest_framework.test import APIRequestFactory
        factory = APIRequestFactory()
        request = factory.get('/')
        user = create_custom_user('5555555', 'Adm', 'adm@t.com', '5555555')
        create_worker(user, user_type=1)
        request.user = user
        perm = AllowAdmin()
        self.assertTrue(perm.has_permission(request, None))

    def test_allow_manager(self):
        from users.views import AllowManager
        from rest_framework.test import APIRequestFactory
        factory = APIRequestFactory()
        request = factory.get('/')
        user = create_custom_user('6666666', 'Mgr', 'mgr@t.com', '6666666')
        create_worker(user, user_type=2)
        request.user = user
        perm = AllowManager()
        self.assertTrue(perm.has_permission(request, None))

    def test_allow_operator(self):
        from users.views import AllowOperator
        from rest_framework.test import APIRequestFactory
        factory = APIRequestFactory()
        request = factory.get('/')
        user = create_custom_user('7777777', 'Op', 'op@t.com', '7777777')
        create_worker(user, user_type=3)
        request.user = user
        perm = AllowOperator()
        self.assertTrue(perm.has_permission(request, None))
