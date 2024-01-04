"""
URL configuration for mcda project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from mcda import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("problem", views.ProblemListApiView.as_view()),
    path("problem/<problem_id>", views.ProblemDetailApiView.as_view()),
    path("criterion", views.CriterionListApiView.as_view()),
    path("criterion/<problem_id>", views.CriterionDetailApiView.as_view()),
    path("option", views.OptionListApiView.as_view()),
    path("option/<problem_id>", views.OptionDetailApiView.as_view()),
    path("crit-option", views.CriterionOptionListApiView.as_view()),
    path("crit-option/<problem_id>", views.CriterionOptionDetailApiView.as_view()),
]
