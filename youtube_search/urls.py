from django.contrib import admin
from django.urls import path
from search import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view,name='home'),
]
