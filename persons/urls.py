from django.urls import path
from . import views

app_name = 'persons'


urlpatterns = [
    path('', views.home, name='home'),
    path('<int:year>/<int:month>/<int:day>/<str:person>/',
         views.person_detail,
         name='person_detail'),
]
