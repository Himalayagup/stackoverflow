import string
import random

from django.utils.text import slugify


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))

def unique_slug_generator_using_title(instance, new_slug=None):
    """
    it assumes instance will always have a model
    with a slug field and a title character (char) field
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug, randstr=random_string_generator(size=8)
        )
        return unique_slug_generator_using_title(instance, new_slug=new_slug)
    return slug
