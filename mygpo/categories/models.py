import random
import string

from django.db import models
from django.utils.text import slugify

from mygpo.core.models import UpdateInfoModel
from mygpo.podcasts.models import Podcast

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class CategoryManager(models.Manager):
    def get_by_natural_key(self, title_slug):
        return self.get(title_slug=title_slug)


class Category(UpdateInfoModel):
    """A category of podcasts"""

    title = models.CharField(max_length=1000, null=False, blank=False, unique=True)
    # Need clean title for directory listing
    title_slug = models.SlugField(max_length=1000, editable=False, blank=False, unique=True)

    num_entries = models.IntegerField()

    # Override default manager
    objects = CategoryManager()

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

        index_together = [("modified", "num_entries")]

    # Use natural key for initial data fixture usage. Don't rely on integer pk
    def natural_key(self):
        return (self.title_slug,)

    def save(self, *args, **kwargs):
        self.num_entries = self.entries.count()
        if not self.pk or not self.title_slug:
            self.title_slug = self._generate_unique_title_slug(self.title)

        super(Category, self).save(*args, **kwargs)

    @property
    def podcasts(self):
        return self.entries.prefetch_related("podcast", "podcast__slugs")

    @property
    def clean_title(self):
        return self.title.replace("\n", " ")

    @property
    def tag(self):
        return self.tags.first().tag

    def _generate_unique_title_slug(self, text):
        new_slug = slugify(text)
        unique_slug = new_slug

        def _generate_queryset():
            test_query = Category.objects.filter(title_slug=unique_slug)
            if self.pk:
                test_query = test_query.exclude(id=self.pk)

            return test_query

        test_query = _generate_queryset()
        slug_exists = test_query.exists()
        while slug_exists:
            unique_slug = "{}-{}".format(unique_slug, random_string_generator(size=4))
            test_query = _generate_queryset()
            slug_exists = test_query.exists()

        return unique_slug


class CategoryEntry(UpdateInfoModel):
    """A podcast in a category"""

    category = models.ForeignKey(
        Category, related_name="entries", on_delete=models.CASCADE
    )

    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE)

    class Meta:
        unique_together = [("category", "podcast")]

        index_together = [("category", "modified")]


class CategoryTagManager(models.Manager):
    def get_by_natural_key(self, tag):
        return self.get(tag=tag)


class CategoryTag(models.Model):

    tag = models.SlugField(unique=True)

    category = models.ForeignKey(
        Category, related_name="tags", on_delete=models.CASCADE
    )

    # Override default manager
    objects = CategoryTagManager()

    # Use natural key for initial data fixture usage. Don't rely on integer pk
    def natural_key(self):
        return (self.tag,)
