from django.contrib.auth import get_user
from django.test import TestCase
from django.urls import reverse

from users.models import CustomUser

class RegistrationTestCase(TestCase):
    def test_user_account_is_created(self):
        self.client.post(
            reverse("users:register"),
            data={
                "username": "mardon",
                "first_name": "Mardon",
                "last_name": "Mustafaqulov",
                "email": "nik63290@gmail.com",
                "password": "somepassword"
            }

        )

        user= CustomUser.objects.get(username="mardon")

        self.assertEqual(user.first_name, "Mardon")
        self.assertEqual(user.last_name, "Mustafaqulov")
        self.assertEqual(user.email, "nik63290@gmail.com")
        self.assertNotEqual(user.password, "somepassword")
        self.assertTrue(user.check_password("somepassword"))

    def test_required_fields(self):
        response = self.client.post(
            reverse("users:register"),
            data={
                "first_name": "Mardon",
                "email": "nik63290@gmail.com",
            }
        )
        form = response.context["form"]
        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 0)
        self.assertFormError(form, "username", "This field is required.")
        self.assertFormError(form, "password", "This field is required.")

    def test_invalid_email(self):
        response = self.client.post(
            reverse("users:register"),
            data={
                "username": "mardon",
                "first_name": "Mardon",
                "last_name": "Mustafaqulov",
                "email": "invalid-email",
                "password": "somepassword"
            }
        )
        form = response.context["form"]
        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 0)
        self.assertFormError(form, "email", "Enter a valid email address.")

    def test_unique_username(self):
        user = CustomUser.objects.create(username="mardon")
        user.set_password("somepassword")
        user.save()

        response = self.client.post(
            reverse("users:register"),
            data={
                "username": "mardon",
                "first_name": "Mardon",
                "last_name": "Mustafaqulov",
                "email": "invalid-email",
                "password": "somepassword"
            }
        )
        form = response.context["form"]
        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 1)
        self.assertFormError(form, "username", "A user with that username already exists.")

class LoginTestCase(TestCase):

     def setUp(self):
         self.db_user = CustomUser.objects.create(username="mardon")
         self.db_user.set_password("somepass")
         self.db_user.save()

     def test_successful_login(self):

         self.client.post(
             reverse("users:login"),
             data={
                 "username": "mardon",
                 "password": "somepass"
             }
         )

         user = get_user(self.client)
         self.assertEqual(user.  is_authenticated, True )

     def test_wrong_credentials(self):

         self.client.post(
             reverse("users:login"),
             data={
                 "username": "wrong-username",
                 "password": "somepass"
             }
         )

         user = get_user(self.client)
         self.assertFalse(user.is_authenticated)

         self.client.post(
             reverse("users:login"),
             data={
                 "username": "mardon",
                 "password": "wrong-password"
             }
         )

         user = get_user(self.client)
         self.assertFalse(user.is_authenticated)

     def test_logout(self):

         self.client.login(username="mardon", password="somepass")

         self.client.get(reverse("users:logout"))

         user = get_user(self.client)
         self.assertFalse(user.is_authenticated)


class ProfileTestCase(TestCase):
    def test_login_required(self):
       response = self.client.get(reverse("users:profile"))

       self.assertEqual(response.status_code, 302)
       # /css/ so'zini /users/ ga almashtiring yoki reverse ishlating
       self.assertEqual(response.url, reverse("users:login") + "?next=/users/profile/")

    def test_profile_details(self):
        user = CustomUser.objects.create(
            username="mardon",
            first_name="Mardon",
            last_name="Mustafaqulov",
            email="nik63290@gmail.com"
         )
        user.set_password("somepass")
        user.save()

        self.client.login(username="mardon", password="somepass")

        response = self.client.get(reverse("users:profile"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)

    def test_update_profile(self):
        user = CustomUser.objects.create(
            username="mardon",
            first_name="Mardon",
            last_name="Mustafaqulov",
            email="nik63290@gmail.com"
        )
        user.set_password("somepass")
        user.save()
        self.client.login(username='mardon', password="somepass")

        response = self.client.post(
            reverse("users:profile-edit"),
            data={
                "username": "mardon",
                "first_name": "Mardon",
                "last_name": "Done",
                'email': 'nik43290@gmail.com'
            }
        )
        user.refresh_from_db()

        self.assertEqual(user.last_name, "Done")
        self.assertEqual(user.email, "nik43290@gmail.com")
        self.assertEqual(response.url, reverse("users:profile"))
    
