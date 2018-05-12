"""nutellove URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

from products import views as product_views
from . import views

urlpatterns = [
    # homepage
    path('', TemplateView.as_view(template_name="index.html"), name="index"),
    path('users/', include('users.urls', namespace="users")),
    path('products/', include('products.urls', namespace="products")),
    path(
        'legals/',
        TemplateView.as_view(template_name="legals.html"),
        name="legals"),
    path('admin/', admin.site.urls),
    path('search/', product_views.Search.as_view(), name='search'),
    # path('favorites/', views.UserFavoritesView.as_view(), name='favorites'),
]


if settings.DEBUG:  # pragma: no cover
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns