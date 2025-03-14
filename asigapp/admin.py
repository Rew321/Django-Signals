from django.contrib import admin

from asigapp.models import BlogPost, Post

# Register your models here.
admin.site.register(BlogPost)
admin.site.register(Post)