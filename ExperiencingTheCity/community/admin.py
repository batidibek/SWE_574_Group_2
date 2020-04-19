from django.contrib import admin

# Register your models here.
from .models import Community, PostType, Post, SemanticTags, MemberShip, Comments, InappropriatePosts, Notification, UserAdditionalInfo, Followership, City

admin.site.register(Community)
admin.site.register(PostType)
admin.site.register(Post)
admin.site.register(SemanticTags)
admin.site.register(MemberShip)
admin.site.register(Comments)
admin.site.register(InappropriatePosts)
admin.site.register(Notification)
admin.site.register(UserAdditionalInfo)
admin.site.register(Followership)
admin.site.register(City)