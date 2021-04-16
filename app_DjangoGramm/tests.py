from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse

from .models import User, Profile, Follower, Post


class BasicTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user_1 = User.objects.create(username='test_user_1', email='testemail_1@test.com', password='password_1')
        self.user_2 = User.objects.create(username='test_user_2', email='testemail_2@test.com', password='password_2')
        self.profile_1 = Profile.objects.filter(user=self.user_1).update(full_name='Test User 1', bio='Hi!I\'m test user 1')
        self.profile_2 = Profile.objects.filter(user=self.user_2).update(full_name='Test User 2', bio='Hi!I\'m test user 2')
        self.post = Post.objects.create(
            user=self.user_1,
            image='https://res.cloudinary.com/dkpmlltlh/image/upload/v1617642447/fqdfojw0ave5mhozuc3r.png',
            description='My test post'
        )
        self.follower = Follower.objects.create(user_id=self.user_2, following_user_id=self.user_1)


class ModelTestCase(BasicTestCase):

    def test_user_model_has_profile(self):
        user = User(
            username='user_user_test',
            email='user_user_test@user.com',
            password='user_user_1234'
        )
        user.save()
        self.assertTrue(hasattr(user, 'profile'))

    def test_models(self):
        test_user = User.objects.get(username='test_user_1')
        self.assertEqual(test_user.username, 'test_user_1')
        self.assertEqual(test_user.email, 'testemail_1@test.com')

        test_profile = Profile.objects.get(user=test_user)
        self.assertEqual(test_profile.full_name, 'Test User 1')
        self.assertEqual(test_profile.bio, 'Hi!I\'m test user 1')

        test_post = Post.objects.filter(user=test_user).first()
        self.assertEqual(test_post.description, 'My test post')

        test_user_2 = User.objects.get(username='test_user_2')
        test_follower = Follower.objects.filter(user_id=test_user_2).first()
        self.assertEqual(test_follower.following_user_id.username, 'test_user_1')


class ViewTestCase(BasicTestCase):

    def test_unauthorized_redirect(self):
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 302)

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_main_view(self):
        response = self.client.get(reverse('main'), {'username': 'test_user_1', 'password': 'password_1'}, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_login_post(self):
        response = self.client.post(reverse('login'), {'username': 'test_user_1', 'password': 'password_1'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user_1.is_authenticated)

    def test_register_post(self):
        response = self.client.post(
            reverse('register'),
            {'username': 'test_user_2', 'email': 'test_email_2@test.com', 'password': 'password_2'}
        )
        self.assertEqual(response.status_code, 200)

    def test_profile_view(self):
        response = self.client.get(reverse('profile', args=['test_user_1', ]), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_new_post(self):
        response = self.client.post(
            reverse('new_post'),
            {'user': self.user_2,
             'image': SimpleUploadedFile('Image', content=b'', content_type='image/jpg'),
             'description': 'My test post'},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)

    def test_following_view(self):
        response = self.client.get(reverse('followers', args=['test_user_2', ]), follow=True)
        self.assertEqual(response.status_code, 200)
        follower = Follower.objects.get(user_id=self.user_2, following_user_id=self.user_1)
        self.assertEqual(follower.following_user_id.username, 'test_user_1')

    def test_follower_view(self):
        response = self.client.get(reverse('following', args=['test_user_1', ]), follow=True)
        self.assertEqual(response.status_code, 200)
        follower = Follower.objects.get(user_id=self.user_2, following_user_id=self.user_1)
        self.assertEqual(follower.user_id.username, 'test_user_2')
