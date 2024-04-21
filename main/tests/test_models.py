# self.assertFalse(response.context["user"].is_authenticated)
# print(response.context["user"])
# # self.assertTrue(response.context["user"].is_authenticated)
from django.test import TestCase
from main.models import Post, User





class PostModelTests(TestCase):

    @classmethod
    def setUp(self):
        user = User.objects.create(name='test_user')
        Post.objects.create(title="Test title", body="Test content", user=user)
        Post.objects.create(title="Test title2", body="Test content2", user=user)

    @classmethod
    def tearDown(self):
        Post.objects.all().delete()
        User.objects.all().delete()


    def test_post_creation(self):
        pass

    def test_post_count(self):
        posts_qty = Post.objects.count()
        self.assertEqual(posts_qty, 2)

        Post.objects.create(title="Test title", body="Test content", user=User.objects.get(id=1))
        posts_qty = Post.objects.count()
        self.assertEqual(posts_qty, 3)

    def test_name_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'Имя пользователя')

    def test_first_name_max_length(self):
        user = User.objects.get(id=1)
        max_length = user._meta.get_field('name').max_length
        self.assertEqual(max_length, 32)