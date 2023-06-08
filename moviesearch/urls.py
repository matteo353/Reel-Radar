from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('Recommendations', views.recommend, name='recommend'),
    path('search_movies/', views.search_movies, name='search_movies')

]