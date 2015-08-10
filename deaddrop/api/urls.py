from django.conf.urls import url, include
from rest_framework import routers
from views import SecretCreate, SecretDecrypt


# url router
router = routers.DefaultRouter()
router.add_api_view("create-view",
                    url(r'^create/$',
                    SecretCreate.as_view(),
                    name='create-view'))

router.add_api_view("decrypt-view",
                    url(r'^decrypt/(?P<uid>\w+)/$',
                    SecretDecrypt.as_view(),
                    name='decrypt-view'))


urlpatterns = [
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # url(r'^', include('rest_framework_swagger.urls')),
    # url(r'^', include('djoser.urls')),
    url(r'^', include(router.urls)),
]
