from django.db import IntegrityError
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

UserModel = get_user_model()


class TestUserModel(TestCase):

    def test__valid_str_method__returns_username(self):

        username = 'TestUser'
        user = UserModel.objects.create_user(
            email='test@email.com',
            username=username,
            password='TestPassword!23',
        )

        self.assertEqual(username, str(user))

    def test__valid_rating__returns_between_1_and_10(self):
        user = UserModel.objects.create_user(
            email='test@test.com',
            username='TestUser',
            password='TestPassword!23',
            rating=5
        )

        self.assertEqual(user.rating, 5)

        try:
            user.full_clean()  # Should not raise
        except Exception as e:
            self.fail(f"Valid rating raised an unexpected error: {e}")


    def test__invalid_rating__raises_error(self):
        with self.assertRaises(BaseException):
            user = UserModel.objects.create_user(
                email='test@test.com',
                username='TestUser',
                password='TestPassword!23',
                rating= 11
            )
            with self.assertRaises(ValidationError):
                user.full_clean()


    def test__invalid_rating_below_minimum__raises_error(self):
        with self.assertRaises(IntegrityError):
            UserModel.objects.create_user(
                email='test@test.com',
                username='TestUser',
                password='TestPassword!23',
                rating=-2
            )


    def test__invalid_rating__zero_rises_error(self):
        user = UserModel.objects.create_user(
            email='test@test.com',
            username='TestUser',
            password='TestPassword!23',
            rating=0
        )
        with self.assertRaises(ValidationError):
            user.full_clean()


    def test__valid_rating__defaults_to_10(self):
        user = UserModel(
            email='default@example.com',
            username='TestUser',
            password='TestPassword!23',
        )
        user.full_clean()
        self.assertEqual(user.rating, 10)
