from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^index$', views.index, name='index'),
    url(r'^recommander$', views.recommander, name='recommander'),
    url(r'^test$', views.test, name='test'),
]
