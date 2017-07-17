from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^index$', views.index, name='index'),
    url(r'^recommender$', views.recommender, name='recommender'),
    url(r'^test$', views.test, name='test'),
    url(r'^upload_data$', views.upload_data, name='upload_data')
]
