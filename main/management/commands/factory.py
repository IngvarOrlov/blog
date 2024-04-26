from datetime import datetime

from django.core.management.base import BaseCommand
import factory
from factory.fuzzy import FuzzyInteger

from main.models import *
from main.slug import make_unique_slug


class Command(BaseCommand):
    help = "Learn factory boy"

    def handle(self, *args, **options):
        class UserFactory(factory.django.DjangoModelFactory):
            class Meta:
                model = User

            username = factory.Faker('name')
            password = factory.Faker('password')
            email = factory.Faker('email')

        class PostFactory(factory.django.DjangoModelFactory):
            class Meta:
                model = Post

            def __init__(self, author):
                self.author = author

            title = factory.Faker('text', max_nb_chars=15)
            body = factory.Faker('paragraph')
            # author=factory.SubFactory(UserFactory)
            # author = self.author
            # slug = factory.Faker('slug')

        #     age = FuzzyInteger(1, 10)

        # animal_1.kind_id
        # animal_1.kind
        # animal_1 = AnimalFactory.build()
        # animal_1 =animal_1 AnimalFactory.create(name='Abcde')
        # post = PostFactory.build()

        # post = PostFactory.create_batch(2)
        author = UserFactory.create()
        for _ in range(2):
            post = PostFactory.build(author=author)
            slug = str(post.title)
            post.slug = make_unique_slug(slug)
            post.save()
