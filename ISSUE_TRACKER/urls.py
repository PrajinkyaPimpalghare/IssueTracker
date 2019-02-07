"""ISSUE_TRACKER URL Configuration

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
from django.contrib import admin
from django.views.generic import TemplateView
from issue_updater import views
from django.urls import path, include

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('admin/', admin.site.urls,),
    path('accounts/', include('django.contrib.auth.urls')),
    path('index/', views.index),
    path('dashboard/', views.dashboard),
    path('contact/', views.contact),
    path('issue_history/', views.issue_history),
    path('issue_page/', views.issue_page),
    path('issue_report/', views.issue_report),
    path('issue_update/', views.issue_update),
    path('issue_search/', views.issue_search),
    path('signup/',views.signup),
    path('wrong_turn/', views.custom_exception),
]
