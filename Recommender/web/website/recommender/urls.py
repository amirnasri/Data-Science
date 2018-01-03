from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^recommender$', views.recommender, name='recommender'),
    url(r'^test$', views.test, name='test'),
    url(r'^upload_data$', views.upload_data, name='upload_data'),
    url(r'^get_movie_data$', views.get_movie_data, name='get_movie_data'),
    url(r'^load_movie_data$', views.load_movie_data, name='load_movie_data'),
]
