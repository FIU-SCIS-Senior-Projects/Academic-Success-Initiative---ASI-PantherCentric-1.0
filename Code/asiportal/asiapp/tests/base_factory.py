import factory
from django.contrib.auth.models import User

class AmbassadorUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    first_name = 'Foo'
    last_name = 'Bar'
    username = factory.Sequence(lambda n: 'foo%d' % n)

class TuteeUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    first_name = 'Bar'
    last_name = 'Foo'
    username = factory.Sequence(lambda n: 'bar%d' % n)
