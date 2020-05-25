from django.db import models
from django.utils.text import slugify


class Author(models.Model):
    auth_id = models.AutoField(primary_key=True)
    author_name = models.CharField(max_length=50)
    Qualifications = models.TextField(max_length=500)
    Skills = models.TextField(max_length=500)
    currently_working_as = models.CharField(max_length=50)
    About = models.TextField(max_length=1000)
    img = models.ImageField(upload_to='author/images')
    slug = models.SlugField(blank=True, null=True)

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.author_name)
        super(Author, self).save(*args, **kwargs)

    def __str__(self):
        return self.author_name
