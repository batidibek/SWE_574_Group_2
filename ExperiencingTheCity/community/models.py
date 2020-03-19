from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
# Create your models here.

#Community              -->  Mina        : 18.03.2020 23.00
class Community(models.Model):
    name            = models.CharField(max_length=100)
    description     = models.CharField(max_length=200)
    creation_date   = models.DateTimeField('date published')
    active          = models.BooleanField(default=True)
    owner           = models.ForeignKey(User)
    # geolocation = models.CharField


#PostType               -->  Mina        : 18.03.2020 23.00
class PostType(models.Model):
    name            = models.CharField(max_length=100)
    description     = models.CharField(max_length=200)
    creation_date   = models.DateTimeField('date published')
    formfields      = JSONField(default="")
    community_id    = models.ForeignKey(Community, default="", on_delete=models.CASCADE)
    owner           = models.ForeignKey(User)
    complaint       = models.BooleanField(default=False)


#Post
class Post(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank = True)
    creation_date = models.DateTimeField('date published')
    form_fields = JSONField()
    community_id = models.ForeignKey(Community, default="", on_delete=models.CASCADE)
    posttype_id = models.ForeignKey(PostType, default="", on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    complaint = models.BooleanField(default=False)
    complaint_status = models.CharField(max_length=100)
    inappropriate = models.BooleanField(default=False)

#SemanticTags 
class SemanticTags(models.Model):
    community_id = models.ForeignKey(Community, default="", on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, default="", on_delete=models.CASCADE)
    tag_info = JSONField()

#MemberShip
class MemberShip(models.Model):
    community_id = models.ForeignKey(Community, default="", on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    
#comments               -->  Burcu       : 20.03.2020 23.00
#Inappropriate Posts    -->  Burcu       : 20.03.2020 23.00

#Notification           -->  Adil        : 19.03.2020 12.00
class Notification(models.Model):
    #type enum?
    community_id    = models.ForeignKey(Community, default="")
    post_id         = models.ForeignKey(Post, default="")
    user_id         = models.ForeignKey(User)
    description     = models.CharField(max_length=200)
    url             = models.CharField(max_length=300)
    creation_date   = models.DateTimeField('date published')

#UserAdditionalInfo     -->  Adil        : 19.03.2020 12.00
class UserAdditionalInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.URLField(max_length=600, blank=True)
    #geolocation

#Followership           -->  Adil        : 19.03.2020 12.00
class Followership(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    #discuss further
    follower = models.ManyToManyField(User)

# + Burcu DB oluşturacak : 20.03.2020 23.00




