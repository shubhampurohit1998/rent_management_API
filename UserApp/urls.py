from django.conf.urls import url, include
from django.urls import path
from .views import *
from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'rent_list', RentListViewSet, basename="rent_list_create")
router.register(r'rent_detail', RentDetailViewSet, basename="rent_detail")


urlpatterns = [
    path('user_list/', UserList.as_view()),
    path('user_detail/<int:pk>/', UserDetail.as_view()),
    path('property_list/', PropertyList.as_view()),
    path('property_detail/<int:pk>', PropertyDetail.as_view()),
    # path('rent_list/', RentList.as_view()),
    # path('rent_detail/<int:pk>', RentDetail.as_view()),
    path('user_property/<int:pk>', UserPropertyList.as_view()),
    path('rent_property/<int:pk>', PropertyRentDetail.as_view()),
    # path('api/', include(router.urls)),
]

urlpatterns += router.urls
