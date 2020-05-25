from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils.timezone import now
from about.models import Author
# Create your models here.


CATEGORY_CHOICES = (
    ('Technology', 'TECHNOLOGY'),
    ('Culture', 'CULTURE'),
    ('Business', 'BUSINESS'),
    ('Politics', 'POLITICS'),
    ('Opinion', 'OPINION'),
    ('Food', 'FOOD'),
    ('Education', 'EDUCATION'),
    ('Science', 'SCIENCE'),
    ('Health', 'HEALTH'),
    ('Style', 'STYLE'),
    ('Travel', 'TRAVEL'),
    ('Others', 'OTHERS'),
)


class Blog(models.Model):
    blg_id = models.AutoField(primary_key=True)
    blog_name = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=20)
    blog_description_1 = models.TextField(max_length=5000)
    blog_description_2 = models.TextField(max_length=5000)
    sub_heading_optional = models.CharField(
        max_length=50, blank=True, null=True)
    blog_description_optional = models.TextField(
        max_length=5000, blank=True, null=True)
    views_count = models.IntegerField(default=0)
    pub_date = models.DateField()
    link_optional = models.URLField(blank=True, null=True)
    link_name_optional = models.CharField(
        max_length=70, blank=True, null=True)
    img = models.ImageField(upload_to='content/images')
    slug = models.SlugField(blank=True, null=True)

    class Meta:
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.blog_name)
        super(Blog, self).save(*args, **kwargs)

    def __str__(self):
        return self.blog_name+" by " + str(self.author)


class URL_update(models.Model):
    update_name = models.CharField(max_length=100)
    url_embed = models.URLField()

    class Meta:
        verbose_name = 'URL_update'
        verbose_name_plural = 'URL_updates'

    def __str__(self):
        return self.update_name


class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70)
    mob = models.CharField(max_length=50)
    textarea = models.TextField(max_length=10000, default="")

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

    def __str__(self):
        return self.name+str(self.msg_id)


class BlogComment(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(default=now)

    class Meta:
        verbose_name = 'BlogComment'
        verbose_name_plural = 'BlogComments'

    def __str__(self):
        return self.comment[0:13]+"..."+" by "+self.user.username
