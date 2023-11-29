"""
URL configuration for weather_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# urls.py

from django.urls import path
from db.views import TariListCreateView, TariUpdateDestroyView, OraseListCreateView, \
    OraseByCountryView, OraseUpdateDeleteView, TemperaturiListCreateView, \
    TemperaturiRetrieveUpdateDestroyView, TemperaturiByCountryView, TemperaturiByCityView

urlpatterns = [
    path('api/countries', TariListCreateView.as_view(), name='countries-list-create'),
    path('api/countries/<id>', TariUpdateDestroyView.as_view(), name='countries-detail'),
    path('api/cities', OraseListCreateView.as_view(), name='cities-list-create'),
    path('api/cities/country/<id_Tara>', OraseByCountryView.as_view(), name='cities-by-country-list'),
    path('api/cities/<id>', OraseUpdateDeleteView.as_view(), name='cities-detail'),
    path('api/temperatures', TemperaturiListCreateView.as_view(), name='temperatures-list-create'),
    path('api/temperatures/cities/<id_oras>', TemperaturiByCityView.as_view(), name='temperatures-by-city-list'),
    path('api/temperatures/countries/<id_tara>', TemperaturiByCountryView.as_view(), name='temperatures-by-country-list'),
    path('api/temperatures/<id>', TemperaturiRetrieveUpdateDestroyView.as_view(), name='temperatures-detail'),
    # Add similar paths for other models
]
