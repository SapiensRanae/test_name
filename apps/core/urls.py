from django.urls import path
from apps.core import views as core_views

urlpatterns = [

    path('about/', core_views.about_view, name='home'),
    path('', core_views.welcome_view, name='welcome' ),

]