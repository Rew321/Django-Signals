from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User
#signals
from django.dispatch import receiver
from django.db.models.signals import (
    pre_save,
    post_save,
    pre_delete,
    post_delete,
    m2m_changed,
)

User = settings.AUTH_USER_MODEL

@receiver(pre_save, sender=User)
def user_pre_save_receiver(sender,instance, *args, **kwargs):
    """
    This function will be called before saving a new user.
    It will create a new profile for the user if one does not exist."""
    
    print(instance.username, instance.id) #None
    # trigger pre-save
     # DONT DO THIS -> instance.save()
    #trigger post-save
@receiver(post_save, sender=User)
def user_post_save_receiver(sender, instance, created,*args, **kwargs):
    """
    This function will be called after saving a new user.
    It will create a new profile for the user if one does not exist."""
    
    if created:
        print("send email to", instance.username)
        # trigger pre-save
        instance.save()
        #trigger post-save
    else:
        print(instance.username, "was just saved")    
       

#post_save.connect(user_created_handler, sender=User)

class Post(models.Model):
    name = models.CharField(max_length=200)
    

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    liked = models.ManyToManyField(User, related_name='liked_posts', blank=True, null=True)
    notify_users = models.BooleanField(default=False)
    notify_users_timestamp = models.DateTimeField(null=True, blank=True, auto_now_add=False)
    active = models.BooleanField(default=True)
    
@receiver(pre_save, sender=BlogPost)  
def blog_post_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title) #This is my title -> this-is-my-title
    
        
@receiver(post_save, sender=BlogPost)  
def blog_post_post_save(sender, instance, created, *args, **kwargs):
    if instance.notify_users:
        print('notify users')
        instance.notify_users = False
        #celery worker task -> offload
        instance.notify_users_timestamp = timezone.now()
        instance.save()    
        
        
        
@receiver(pre_delete, sender=BlogPost)  
def blog_post_pre_delete(sender, instance, *args, **kwargs):
    #move or make a backup of this data
    print(f"{instance.id} is about to be deleted")
#pre_delete.delete.connect(blog_post_pre_delete, sender=BlogPost)        
@receiver(post_delete, sender=BlogPost)  
def blog_post_post_delete(sender, instance, *args, **kwargs):
    # celery worker task -> offload time & Task
    print(f"{instance.id} has been removed")
    
#post_delete.delete.connect(blog_post_pre_delete, sender=BlogPost)    

@receiver(m2m_changed, sender=BlogPost.liked.through)
def blog_post_liked_changed(sender, instance, action, *args, **kwargs):
    #print(args, kwargs)   
    print(action) 
    if action == 'pre_add':
        print("was added successfully")
        qs = kwargs.get("model").objects.filter(pk__in=kwargs.get("pk_set"))
        print(qs.count())
