from django.conf.urls import url, include
from django.contrib.auth import get_user_model
from django.urls import path
from rest_framework import routers, serializers, viewsets
from UserApp import urls as userapp
# from UserApp.views import RentListSet
User = get_user_model()

# router = routers.DefaultRouter()
# router.register(r'renter/renter_list', RentListSet, basename='name')

# urlpatterns = router.urls
urlpatterns = [
    path('', include(userapp)),
    # path('', include(router.urls))
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
