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


#Post                   -->  Batı        : 19.03.2020 23.00
#SemanticTags           -->  Batı        : 19.03.2020 23.00
#MemberShip             -->  Batı        : 19.03.2020 23.00
#comments               -->  Burcu       : 20.03.2020 23.00
#Inappropriate Posts    -->  Burcu       : 20.03.2020 23.00
#Notification           -->  Adil        : 19.03.2020 12.00
#UserAdditionalInfo     -->  Adil        : 19.03.2020 12.00
#Followership           -->  Adil        : 19.03.2020 12.00


# + Burcu DB oluşturacak : 20.03.2020 23.00




