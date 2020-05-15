import datetime

from django.test import TestCase
from community.models import Community, PostType, User


# Create your tests here.

class CommunityTestCase(TestCase):
    def setUp(self, request):
        lat ="41.083077715863794"
        lon = "29.04949948657304"
        geolocation = {"location": []}
        wiki_tags = {}
        for i in range(len(lat)):
            geolocation["location"].append({"lat": lat[i], "lon": lon[i]})
        user = User.objects.get(id=1)
        Community.objects.create(name="Test Community",
                                 description="A community to perform unit test",
                                 # geolocation=geolocation,
                                 active=True,
                                creation_date= datetime.datetime.now(),
                                owner = user.id
                                 )
        def getCommunityTest(self):
            community = Community.objects.get(name = "Test Community" )
            print(community)
