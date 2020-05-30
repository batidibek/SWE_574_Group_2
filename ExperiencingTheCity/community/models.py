from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField


class Community(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    creation_date = models.DateTimeField('date published')
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    geolocation = JSONField(default="")
    tags = JSONField(default="")

    def __str__(self):
        return self.name


class PostType(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    creation_date = models.DateTimeField('date published')
    formfields = JSONField(default="")
    community_id = models.ForeignKey(
        Community, default="", on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    complaint = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    def __str__(self):
        return self.name


class Post(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    creation_date = models.DateTimeField('date published')
    form_fields = JSONField(default="")
    community_id = models.ForeignKey(Community, default="", on_delete=models.CASCADE)
    posttype_id = models.ForeignKey(PostType, default="", on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    complaint = models.BooleanField(default=False)
    complaint_status = models.CharField(max_length=100)
    inappropriate = models.BooleanField(default=False)
    tags = JSONField(default="")
    active = models.BooleanField(default=True)


class SemanticTags(models.Model):
    community_id = models.ForeignKey(
        Community, default="", on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, default="", on_delete=models.CASCADE)
    tag_info = JSONField()


class MemberShip(models.Model):
    community_id = models.ForeignKey(
        Community, default="", on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class Comments(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, default="", on_delete=models.CASCADE)
    comment_body = JSONField(default="")
    comment_media = JSONField(default="")
    creation_date = models.DateTimeField('date published')


class InappropriatePosts(models.Model):
    post_id = models.ForeignKey(Post, default="", on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    inappropriate = models.BooleanField()


class Notification(models.Model):
    # type enum?
    community_id = models.ForeignKey(
        Community, default="", on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, default="", on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    url = models.CharField(max_length=300)
    creation_date = models.DateTimeField('date published')


class UserAdditionalInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.URLField(max_length=600, blank=True)

    # geolocation
    def __str__(self):
        return self.user.username


class Followership(models.Model):
    follows = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='follows')
    # discuss further
    # models.ManyToManyField(User)
    followed = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, related_name="followed")

    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} follows {}'.format(self.follows, self.followed)


User.add_to_class('following',
                  models.ManyToManyField('self',
                                         through=Followership,
                                         related_name='followers',
                                         symmetrical=False))
