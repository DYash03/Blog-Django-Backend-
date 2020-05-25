from django.contrib import admin
from .models import Blog, Contact, URL_update, BlogComment
# Register your models here.
admin.site.register((Blog, BlogComment))
admin.site.register(Contact)
admin.site.register(URL_update)
