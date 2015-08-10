from django.conf.urls import url, include
from rest_framework import routers

# url router
router = routers.DefaultRouter()


urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include('rest_framework_swagger.urls')),
    url(r'^', include('djoser.urls')),
    url(r'^', include(router.urls)),
]
